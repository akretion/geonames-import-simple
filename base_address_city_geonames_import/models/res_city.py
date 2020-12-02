# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResCity(models.Model):
    _inherit = "res.city"

    def name_get(self):
        if not self.env.context.get("helper_search_city"):
            return super().name_get()
        res = []
        for city in self:
            name = [city.name]
            if city.zipcode:
                name.append(city.zipcode)
            if city.state_id:
                name.append(city.state_id.name)
            if city.country_id:
                name.append(city.country_id.name)
            res.append((city.id, ", ".join(name)))
        return res

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        self = self.with_context(helper_search_city=True)
        if args is None:
            args = []
        if name and operator == 'ilike':
            recs = self.search(
                [('zipcode', '=', name)] + args, limit=limit)
            if recs:
                return recs.name_get()
        return super(ResCity, self).name_search(name=name, args=args, operator=operator, limit=limit)
