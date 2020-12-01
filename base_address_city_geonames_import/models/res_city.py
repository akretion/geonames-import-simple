# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResCity(models.Model):
    _inherit = "res.city"

    @api.model
    def name_search(
            self, name='', args=None, operator='ilike', limit=80):
        if args is None:
            args = []
        if name and operator == 'ilike':
            recs = self.search(
                [('zipcode', '=', name)] + args, limit=limit)
            if recs:
                return recs.name_get()
        return super().name_search(
            name=name, args=args, operator=operator, limit=limit)
