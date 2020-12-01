# Copyright 2014-2016 Akretion (Alexis de Lattre
#                     <alexis.delattre@akretion.com>)
# Copyright 2014 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
#                <contact@eficent.com>
# Copyright 2018 Aitor Bouzas <aitor.bouzas@adaptivecity.com>
# Copyright 2016-2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import csv
import io
import logging
import os
import tempfile
import zipfile

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


class ResCityGeonamesImport(models.TransientModel):
    _name = "res.city.geonames.import"
    _description = "Import City Zips from Geonames"

    country_ids = fields.Many2many("res.country", string="Countries")

    letter_case = fields.Selection(
        [("unchanged", "Unchanged"), ("title", "Title Case"), ("upper", "Upper Case")],
        string="Letter Case",
        default="unchanged",
        help="Converts retreived city and state names to Title Case "
        "(upper case on each first letter of a word) or Upper Case "
        "(all letters upper case).",
    )
    create_states = fields.Boolean(default=True)

    def row2rowdict(self, row, country):
        return {
            'state_name': row[country["geonames_state_name_column"] or 3],
            'state_code': row[country["geonames_state_code_column"] or 4],
            'country_code': row[0],
            'city_name': row[2],
            'zip': row[1],
            }

    @api.model
    def prepare_state(self, rowdict, country):
        return {
            "name": rowdict['state_name'],
            "code": rowdict['state_code'],
            "country_id": country["id"],
        }

    @api.model
    def prepare_city(self, rowdict, country, state_id, letter_case):
        city_name = rowdict['city_name']
        if letter_case == "title":
            city_name = city_name.title()
        elif letter_case == "upper":
            city_name = city_name.upper()
        vals = {
            "name": city_name,
            "state_id": state_id,
            "country_id": country["id"],
            "zipcode": rowdict["zip"],
        }
        return vals

    @api.model
    def get_and_parse_csv(self, country):
        country_code = country['code']
        config_url = self.env["ir.config_parameter"].get_param(
            "geonames.url", default="http://download.geonames.org/export/zip/%s.zip"
        )
        url = config_url % country_code
        logger.info("Starting to download %s" % url)
        res_request = requests.get(url)
        if res_request.status_code != requests.codes.ok:
            raise UserError(
                _("Got an error %d when trying to download the file %s.")
                % (res_request.status_code, url)
            )

        f_geonames = zipfile.ZipFile(io.BytesIO(res_request.content))
        tempdir = tempfile.mkdtemp(prefix="odoo")
        f_geonames.extract("%s.txt" % country_code, tempdir)

        data_file = open(
            os.path.join(tempdir, "%s.txt" % country_code), "r", encoding="utf-8"
        )
        data_file.seek(0)
        reader = csv.reader(data_file, delimiter="	")
        parsed_csv = [row for i, row in enumerate(reader)]
        data_file.close()
        logger.info("The geonames zipfile has been decompressed")
        return parsed_csv

    def _create_states(self, parsed_csv, country):
        state_dict = {}
        state_model = self.env["res.country.state"]
        # for states, we only use the code to match
        existing_states_read = state_model.search_read([
            ('code', '!=', False),
            ('country_id', '=', country["id"])], ['code'])
        for state in existing_states_read:
            state_dict[state['code']] = state['id']
        if self.create_states:
            for row in parsed_csv:
                rowdict = self.row2rowdict(row, country)
                state_code = rowdict.get('state_code')
                if state_code and state_code not in state_dict:
                    state_vals = self.prepare_state(rowdict, country)
                    state = state_model.create(state_vals)
                    state_dict[state_vals['code']] = state.id
        return state_dict

    def _create_cities(self, parsed_csv, state_dict, country):
        city_model = self.env['res.city']
        letter_case = self.letter_case
        city_vals_list = []
        old_city_dict = {}  # key = (name, zip, state_id)
        new_city_dict = {}  # key = (name, zip, state_id)
        cities_read = city_model.search_read([
            ('zipcode', '!=', False),
            ('country_id', '=', country["id"]),
            ], ['name', 'zipcode', 'state_id', 'country_id'])
        for city in cities_read:
            key = (
                city['name'],
                city['zipcode'],
                city['state_id'] and city['state_id'][0] or False)
            old_city_dict[key] = city['id']
        for row in parsed_csv:
            rowdict = self.row2rowdict(row, country)
            state_id = False
            if rowdict['state_code']:
                state_id = state_dict.get(rowdict['state_code'], False)
            # First we transform, and THEN we compare
            city_vals = self.prepare_city(rowdict, country, state_id, letter_case)
            key = (city_vals['name'], city_vals['zipcode'], state_id)
            if key in old_city_dict:
                new_city_dict[key] = old_city_dict[key]
            else:
                if city_vals not in city_vals_list:
                    city_vals_list.append(city_vals)
        ctx = dict(self.env.context)
        ctx.pop("lang", None)  # make sure no translation is added
        created_cities = city_model.with_context(ctx).create(city_vals_list)
        for i, vals in enumerate(city_vals_list):
            key = (vals['name'], vals['zipcode'], vals['state_id'])
            new_city_dict[key] = created_cities[i].id
        return new_city_dict

    def run_import(self):
        for country in self.country_ids:
            country_dict = {
                'id': country.id,
                'code': country.code,
                'name': country.name,
                'geonames_state_name_column': country.geonames_state_name_column,
                'geonames_state_code_column': country.geonames_state_code_column,
                'record': country,
                }
            parsed_csv = self.get_and_parse_csv(country_dict)
            self._process_csv(parsed_csv, country_dict)
        action = self.env.ref('base_address_city.action_res_city_tree').read()[0]
        return action

    def _process_csv(self, parsed_csv, country):
        city_model = self.env["res.city"]
        # Store current record list
        old_cities = set(city_model.search([("country_id", "=", country['id'])]).ids)
        logger.info("Starting to create the cities and/or city zip entries")
        # Pre-create states and cities
        state_dict = self._create_states(parsed_csv, country)
        city_dict = self._create_cities(parsed_csv, state_dict, country)
        old_cities -= set(city_dict.values())
        if old_cities:
            logger.info("removing city entries")
            city_model.browse(list(old_cities)).unlink()
            logger.info(
                "%d res.city entries deleted for country %s"
                % (len(old_cities), country['name'])
                )
        logger.info(
            "The wizard to create cities and/or city zip entries from "
            "geonames has been successfully completed."
        )
        return True
