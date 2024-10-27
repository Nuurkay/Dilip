# See LICENSE file for full copyright and licensing details.

from odoo import api, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.model
    def create(self, values):
        rec = super(SaleOrder, self).create(values)
        if self._context.get("is_diet_sale"):
            rec.action_confirm()
        return rec
