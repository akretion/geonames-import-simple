# Copyright 2016-2019 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestBaseLocationGeonamesImport(common.TransactionCase):

    def test_import_country(self):
        country = self.env.ref('base.mc')
        # Create dumb res.city, to see if it's deleted
        city_to_del = self.env['res.city'].create({
            'name': 'Test base_address_extended_geonames_import',
            'zipcode': 'ZZ9988YYXX',
            'country_id': country.id})
        city_to_del_id = city_to_del.id
        wiz = self.env['res.city.geonames.import'].create({
            'country_ids': [(6, 0, [country.id])]})
        wiz.run_import()
        # Test deletion
        self.assertFalse(self.env["res.city"].search_count(
            [('id', '=', city_to_del_id)]))
        # Look if there are imported cities
        city_count = self.env["res.city"].search_count(
            [("country_id", "=", country.id)]
        )
        self.assertTrue(city_count)
        # Reimport again to see that there's no duplicates
        wiz.run_import()
        city_count2 = self.env["res.city"].search_count(
            [("country_id", "=", country.id)]
        )
        self.assertEqual(city_count, city_count2)
