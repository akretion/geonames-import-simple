# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResCity(models.Model):
    _inherit = "res.city"

    @api.model
    def _search_display_name(self, operator, value):
        if operator == "ilike" and value and isinstance(value, str) and value.isdigit():
            domain = [('zipcode', '=like', value + '%')]
        else:
            domain = super()._search_display_name(operator, value)
        return domain
