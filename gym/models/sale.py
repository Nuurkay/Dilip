# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    """Imported sale order model."""

    _inherit = 'sale.order'

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    membership = fields.Boolean(string='Membership',
                                help='Check if the Customer Wants to Buy '
                                     'membership.')

    @api.model
    def create(self, values):
        rec = super(SaleOrder, self).create(values)
        if rec.membership and not rec.partner_id.is_member:
            rec.partner_id.is_member = True
        return rec

    def write(self, values):
        for rec in self:
            if values.get('partner_id'):
                partner_id =\
                    self.env['res.partner'].browse(values.get('partner_id'))
            else:
                partner_id = rec.partner_id
            if values.get('membership', rec.membership) and not \
                    partner_id.is_member:
                partner_id.is_member = True
        return super(SaleOrder, self).write(values)

    @api.constrains('order_line', 'membership')
    def _check_order_line_membership(self):
        """Membership product constraint."""
        if self.membership and len([rec for rec in self.order_line.filtered(
                lambda rec:
                rec.product_id.product_tmpl_id.is_membership)]) > 1:
            raise ValidationError(
                _("You can\'t select more than one membership product."))

    @api.constrains('start_date', 'end_date')
    def _check_date(self):
        """Membership date constraint."""
        if self.membership and self.start_date > self.end_date:
            raise ValidationError(
                _("End date must be greater than start date"))

    def action_confirm(self):
        """Create membership line when confirm sale order."""
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if order.membership and order.state == 'sale' and not \
                    order._context.get('is_membership_created'):
                for line_rec in order.order_line:
                    if line_rec.product_id.product_tmpl_id.is_membership:
                        membership_rec = \
                            self.env['membership.membership_line'].create({
                                'partner': order.partner_id.id,
                                'date': order.start_date,
                                'end_date': order.end_date,
                                'member_price': line_rec.price_subtotal,
                                'membership_id': line_rec.product_id.id,
                                'sale_order_id': order.id,
                            })
                        membership_rec.action_confirm()
        return res
