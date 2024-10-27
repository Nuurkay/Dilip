# See LICENSE file for full copyright and licensing details.

from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MembershipInvoice(models.TransientModel):
    """Membership Invoice Wizard."""

    _inherit = 'membership.invoice'

    product_id = fields.Many2one('product.product',
                                 string='Membership', help='Membership plan')
    membership_plan_id = fields.Many2one('product.template', 'Membership Plan',
                                         help='Selection of membership plan '
                                              'in membership invoice')


class MembershipPlanMain(models.Model):
    """Inherited Membership line object for membership records."""

    _inherit = 'membership.membership_line'

    membership_id = fields.Many2one('product.product',
                                    string="Membership Scheme",
                                    required=True)
    end_date = fields.Date('End Date', help='End date of the Membership')
    states = fields.Selection([('draft', 'Draft'),
                               ('confirm', 'Confirmed'),
                               ('expire', 'Expired'),
                               ('cancel', 'Cancelled')],
                              string='Status',
                              default='draft')
    plan_sequence = fields.Char('Plan ID',
                                help='Sequence of the Membership Plan')
    sale_order_id = fields.Many2one('sale.order', 'Order',
                                    readonly=True, copy=False,
                                    help='Store the Reference of the sale'
                                         ' order')
    paid_amount = fields.Float('Paid Amount', store=True,
                               compute='_compute_get_paid_amount')

    @api.depends('sale_order_id.invoice_ids.amount_residual')
    def _compute_get_paid_amount(self):
        for rec in self:
            amount_total = 0
            for inv in rec.sale_order_id.invoice_ids.filtered(
                    lambda inv: inv.state != 'draft'):
                amount_total += (inv.amount_total - inv.amount_residual)
            rec.paid_amount = amount_total

    @api.onchange('membership_id')
    def _onchange_membership_id(self):
        self.member_price = self.membership_id.list_price

    @api.constrains('date', 'end_date', 'partner', 'membership_id')
    def _check_time(self):
        """Start and End date validation."""
        if self.date and self.end_date and self.date >= self.end_date:
            raise ValidationError(_("End date must be greater "
                                    "than the start date."))
        membership_ids = self.search([
            ('partner', '=', self.partner.id),
            ('membership_id', '=', self.membership_id.id),
            '|', '&',
            ('date', '<=', self.date),
            '&', ('end_date', '>=', self.date),
            ('date', '<', self.end_date),
            '&', ('date', '<', self.end_date),
            ('end_date', '>', self.date),
            ('id', '!=', self.id)])
        if membership_ids:
            raise ValidationError(_("You can not create membership, This "
                                    "membership is already created."))

    @api.model
    def create(self, vals):
        """Sequence of Membership record."""
        if vals.get('partner'):
            vals['plan_sequence'] = self.env[
                'ir.sequence'].next_by_code('membership.membership_line')
        return super(MembershipPlanMain, self).create(vals)

    def unlink(self):
        for mem_rec in self:
            if mem_rec.states == 'confirm':
                raise ValidationError(
                    _("Sorry, you can't delete a confirmed membership."))
        return super(MembershipPlanMain, self).unlink()

    def copy(self, default=None):
        for mem_rec in self:
            if mem_rec.states == 'confirm':
                raise ValidationError(
                    _("Sorry, you can't duplicate a confirmed membership."))
        return super(MembershipPlanMain, self).copy(default)

    def action_draft(self):
        """Set the Membership to draft."""
        for mem_rec in self:
            mem_rec.states = "draft"

    def action_cancel(self):
        """Set the Membership to cancelled."""
        for mem_rec in self:
            mem_rec.states = "cancel"

    def action_confirm(self):
        """Set the Membership to confirmed."""
        for mem_rec in self:
            sale_order_id = self.env['sale.order'].with_context(
                is_membership_created=True).create(
                {'partner_id': mem_rec.partner.id,
                 'membership': True,
                 'start_date': mem_rec.date,
                 'end_date': mem_rec.end_date,
                 'order_line': [(0, 0,
                                 {'product_id': mem_rec.membership_id.id,
                                  'price_unit': mem_rec.member_price})]})
            sale_order_id.action_confirm()
            mem_rec.write({'states': 'confirm',
                           'sale_order_id': sale_order_id.id})

    def action_expire(self):
        """Set the Membership to expired."""
        for mem_rec in self:
            mem_rec.states = "expire"

    @api.model
    def check_membership_validity(self):
        """Method for calculating the remaining days of Membership and gives
        notification of membership Expiration.
        """
        user_rec = self.env.user
        curr_day = date.today()
        # searching on membership.membership_line
        membership_line = self.search(
            ['|', ('end_date', '<', curr_day), '&',
             ('end_date', '>=', curr_day),
             '&',
             ('end_date', '<=', curr_day + relativedelta(days=7)),
             ('states', 'in', ['confirm'])])
        # loop on membership.membership_line
        for membership_rec in membership_line:
            # fetching email of member.
            if membership_rec.partner.email:
                # template for email
                template = self.env.ref('gym.membership_expiration')
                end_dt = membership_rec.end_date
                remain_days = end_dt - curr_day
                due_days = str(max(0, remain_days.days))
                # Setting the membership state to expire if days are 0
                if remain_days.days <= 0:
                    membership_rec.action_expire()
                # Email content
                if template:
                    body = ''
                    body += "<p>Hello <b>" + membership_rec.partner.name + \
                            "</b>,</p></br>"
                    body += "<p>This email is to inform you that your " \
                            "membership will be expiring in " \
                            + due_days + " days." "</p></br>"
                    body += "<p>For renewal, please contact the " \
                            "manager." "</p></br>"
                    body += "<p>Thank You." "</p></br>"
                    body += "<p>" + user_rec.company_id.name + "," " </p></br>"
                    body += "<p>" + user_rec.name + "." " </p></br>"
                    template.write({'body_html': body})
                    template.send_mail(membership_rec.partner.id,
                                       force_send=True)

    @api.depends('account_invoice_id.state',
                 'account_invoice_id.amount_residual',
                 'account_invoice_id.payment_state')
    def _compute_state(self):
        """Compute the state lines """
        if not self:
            return
        if self.account_invoice_id:
            self._cr.execute('''
                SELECT reversed_entry_id, COUNT(id)
                FROM account_move
                WHERE reversed_entry_id IN %s
                GROUP BY reversed_entry_id
            ''', [tuple(self.mapped('account_invoice_id.id'))])
        reverse_map = dict(self._cr.fetchall())
        for line in self:
            move_state = line.account_invoice_id.state
            payment_state = line.account_invoice_id.payment_state

            line.state = 'none'
            if move_state == 'draft':
                line.state = 'waiting'
            elif move_state == 'posted':
                if payment_state == 'paid':
                    if reverse_map.get(line.account_invoice_id.id):
                        line.state = 'canceled'
                    else:
                        line.state = 'paid'
                elif payment_state == 'in_payment':
                    line.state = 'paid'
                elif payment_state == 'not_paid':
                    line.state = 'invoiced'
            elif move_state == 'cancel':
                line.state = 'canceled'
