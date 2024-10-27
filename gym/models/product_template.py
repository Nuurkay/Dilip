# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class GymEquipments(models.Model):
    """Inherited product model for creating Equipment."""

    _inherit = 'product.template'

    is_equipment = fields.Boolean(string='Is Equipment',
                                  default=lambda self: self.env.context.
                                  get('equipments_default', False))
    exercise_ids = fields.Many2many('exercise.type',
                                    string='Exercise Type',
                                    help='This Equipment is For which '
                                         'Type of Exercise')
    state = fields.Selection([('working', 'Working'),
                              ('maintenance', 'Maintenance'),
                              ('repair', 'Repair'),
                              ('out_of_service', 'Out Of Service')], 'State',
                             help='States of the Equipment', default='working')
    note = fields.Text('Note')
    company = fields.Char('Company Name')
    purchase_date = fields.Date('Purchase Date')
    is_service = fields.Boolean(string='Is Service',
                                default=lambda self: self.env.context.
                                get('service_default', False))
    is_food = fields.Boolean(string='Is Food?')
    unit_id = fields.Many2one('uom.uom', string="Unit of Measure",
                              help='Measurement Unit for Food item')
    quantity = fields.Char('Quantity')
    calorie = fields.Float('Calories')
    protein = fields.Float('Protein')
    carbohydrates = fields.Float('Carbohydrates')
    fat = fields.Float(string='Fat')
    fibres = fields.Float('Fibres')
    sodium = fields.Float('Sodium')
    is_membership = fields.Boolean(string='Is Membership ?',
                                   help='Check if the product is eligible '
                                        'for membership.')

    def sts_work(self):
        for equipment_rec in self:
            equipment_rec.state = 'working'
            cr, uid, context, su = self.env.args
            context = dict(context)
            template_id = self.env.ref('gym.equipement_repair_template')
            to_mail_id = []
            employee_ids = self.env['hr.employee'].search(
                [('active', '=', True)])
            for employee_id in employee_ids:
                if employee_id.user_id and \
                        employee_id.user_id.partner_id.email:
                    to_mail_id.append(
                        employee_id.user_id.email)

            to_mail_ids = ','.join(to_mail_id)
            body_html = """<![CDATA[<div style="font-family: 'Lucica Grande',
                Ubuntu, Arial, Verdana, sans-serif; font-size: 14px;
                color: rgb(34, 34, 34); background-color: #FFF; ">
                <p>Hello <b>Trainer</b>,</p>
                <p>It is to be informed that <b>${object.name}</b>
                 is working.<p/>
            """
            user_id = self.env['res.users'].browse(uid)
            if to_mail_ids:
                template_id.write(
                    {'body_html': body_html,
                     'subject': 'Equipment is Working.',
                     'email_from': str(user_id.email),
                     'email_to': to_mail_ids,
                     'lang': 'lang' in context and
                     context.get('lang', 'en_US')})
                template_id.send_mail(self.id, force_send=True)

    def sts_maintan(self):
        for equipment_rec in self:
            equipment_rec.state = 'maintenance'
            cr, uid, context, su = self.env.args
            context = dict(context)
            template_id = self.env.ref('gym.equipement_repair_template')
            to_mail_id = []
            employee_ids = self.env['hr.employee'].search(
                [('active', '=', True)])
            for employee_id in employee_ids:
                if employee_id.user_id and \
                        employee_id.user_id.partner_id.email:
                    to_mail_id.append(
                        employee_id.user_id.email)

            to_mail_ids = ','.join(to_mail_id)
            body_html = """<![CDATA[<div style="font-family: 'Lucica Grande',
                Ubuntu, Arial, Verdana, sans-serif; font-size: 14px;
                color: rgb(34, 34, 34); background-color: #FFF; ">
                <p>Hello <b>Trainer</b>,</p>
                <p>It is to be informed that <b>${object.name}</b>
                 is under maintenance.<p/>
            """
            user_id = self.env['res.users'].browse(uid)
            if to_mail_ids:
                template_id.write(
                    {'body_html': body_html,
                     'subject': 'Equipment is under maintenance.',
                     'email_from': str(user_id.email),
                     'email_to': to_mail_ids,
                     'lang': 'lang' in context and
                     context.get('lang', 'en_US')})
                template_id.send_mail(self.id, force_send=True)

    def sts_rpr(self):
        for equipment_rec in self:
            equipment_rec.state = 'repair'
            cr, uid, context, su = self.env.args
            context = dict(context)
            template_id = self.env.ref('gym.equipement_repair_template')
            to_mail_id = []
            employee_ids = self.env['hr.employee'].search(
                [('active', '=', True)])
            for employee_id in employee_ids:
                if employee_id.user_id and \
                        employee_id.user_id.partner_id.email:
                    to_mail_id.append(
                        employee_id.user_id.email)

            to_mail_ids = ','.join(to_mail_id)
            body_html = """<![CDATA[<div style="font-family: 'Lucica Grande',
                Ubuntu, Arial, Verdana, sans-serif; font-size: 14px;
                color: rgb(34, 34, 34); background-color: #FFF; ">
                <p>Hello <b>Trainer</b>,</p>
                <p>It is to be informed that<b>${object.name}</b>
                 is under repair.<p/>
            """
            user_id = self.env['res.users'].browse(uid)
            if to_mail_ids:
                template_id.write(
                    {'body_html': body_html,
                     'subject': 'Equipment is under repairing.',
                     'email_from': str(user_id.email),
                     'email_to': to_mail_ids,
                     'lang': 'lang' in context and
                     context.get('lang', 'en_US')})
                template_id.send_mail(self.id, force_send=True)

    def sts_out(self):
        for equipment_rec in self:
            equipment_rec.state = 'out_of_service'
