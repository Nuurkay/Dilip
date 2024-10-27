# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    """Users's detail."""

    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        return super(ResUsers,
                     self.with_context(is_create_user=True)).create(vals)


class MemberDetail(models.Model):
    """Member's detail."""

    _inherit = 'res.partner'

    is_member = fields.Boolean(string='Is member ?',
                               default=lambda self: self.env.context.
                               get('member_default', False))
    is_operator = fields.Boolean(string='Operator')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              string='Gender', default='male')
    occupation = fields.Char('Occupation')
    reg_no = fields.Char('Member ID', copy=False,
                         help='Registration Number of Member')
    member_measurement_ids = fields.One2many('body.measurement', 'partner_id',
                                             'Measurement History',
                                             help='Body Measurement History '
                                                  'of the Member')
    birthdate = fields.Date('Date of Birth')
    age = fields.Float(compute='_compute_calculate_age', string='Age')
    measurements = fields.Integer(compute="_compute_cal_total_measurement",
                                  string="Total measurement")
    membership = fields.Integer(compute="_compute_cal_total_membership",
                                string="Total membership")
    user_id = fields.Many2one('res.users', copy=False, string='User',
                              ondelete="cascade")
    email = fields.Char(copy=False)

    def unlink(self):
        for rec in self:
            user_id = rec.user_id
            rec.user_id = False
            user_id.unlink()
        return super(MemberDetail, self).unlink()

    @api.constrains('birthdate')
    def _check_birthdate(self):
        """Check birth date of Member."""
        if self.birthdate and self.birthdate >= date.today():
            raise ValidationError(_("Birth date must be less than today's"
                                    " date."))

    def _compute_cal_total_measurement(self):
        """Measurement history count."""
        for partner_rec in self:
            partner_rec.measurements = \
                partner_rec.member_measurement_ids and len(
                    partner_rec.member_measurement_ids.ids)

    def _compute_cal_total_membership(self):
        """Count no of membership of the member."""
        for partner_rec in self:
            partner_rec.membership = \
                partner_rec.member_lines and len(
                    partner_rec.member_lines.ids)

    def _compute_calculate_age(self):
        """Age calculation of member."""
        for partner_rec in self:
            partner_rec.age = \
                partner_rec.birthdate and \
                date.today().year - partner_rec.birthdate.year

    @api.model
    def create(self, vals):
        """Create sequence of member."""
        rec = super(MemberDetail, self).create(vals)
        if vals.get('name'):
            vals['reg_no'] = self.env[
                'ir.sequence'].next_by_code('res.partner')
        if not self.env['res.users']._context.get('is_create_user'):
            rec.user_id = self.env['res.users'].create({
                'name': rec.name,
                'login': rec.email,
                'partner_id': rec.id,
                'password': rec.company_id.default_password or '',
                'groups_id': [(6, 0, [self.env.ref(
                    'gym.group_gym_member').id])]
            }).id
        return rec

    def action_view_user(self):
        """
        This Method is used to Open User from member record.
        @param self: The object pointer
        """
        # Created res users in open
        return {
            'view_type': 'form',
            'view_id': self.env.ref('base.view_users_form').id,
            'view_mode': 'form',
            'res_model': 'res.users',
            'res_id': self.user_id.id,
            'type': 'ir.actions.act_window'
        }


class BodyMeasurement(models.Model):
    """Body Measurement of the Member."""

    _name = 'body.measurement'
    _description = "Body Measurement"
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', 'Member')
    date = fields.Date('Date', required=True)
    neck = fields.Float('Neck')
    umo_neck_id = fields.Many2one(
        'uom.uom', string='Measurement Unit',
        domain=lambda self: [('category_id', '=',
                              self.env.ref('uom.uom_categ_length').id)])
    chest = fields.Float('Chest')
    umo_chest_id = fields.Many2one(
        'uom.uom', string='Measurement Unit for Chest',
        domain=lambda self: [('category_id', '=',
                              self.env.ref('uom.uom_categ_length').id)])
    biceps = fields.Float('Biceps')
    umo_biceps_id = fields.Many2one(
        'uom.uom', string='Measurement Unit Biceps',
        domain=lambda self: [('category_id', '=',
                              self.env.ref('uom.uom_categ_length').id)])
    waist = fields.Float('Waist')
    umo_waist_id = fields.Many2one(
        'uom.uom', string='Measurement Unit Waist',
        domain=lambda self: [('category_id', '=',
                              self.env.ref('uom.uom_categ_length').id)])
    hips = fields.Float('Hips')
    umo_hips_id = fields.Many2one(
        'uom.uom', string='Measurement Unit Hips',
        domain=lambda self: [('category_id', '=',
                              self.env.ref('uom.uom_categ_length').id)])
    thigh = fields.Float('Thighs')
    umo_thigh_id = fields.Many2one(
        'uom.uom', string='Measurement Unit Thigh',
        domain=lambda self: [('category_id', '=',
                              self.env.ref('uom.uom_categ_length').id)])
    calf = fields.Float('Calf')
    umo_calf_id = fields.Many2one(
        'uom.uom', string='Measurement Unit Calf',
        domain=lambda self: [('category_id', '=',
                              self.env.ref('uom.uom_categ_length').id)])
    weight = fields.Float('Weight')
    umo_weight_id = fields.Many2one(
        'uom.uom', string='Measurement Unit Weight',
        domain=lambda self: [('category_id', '=',
                              self.env.ref('uom.product_uom_categ_kgm').id)])
    height = fields.Float('Height')
    umo_height_id = fields.Many2one(
        'uom.uom', string='Measurement Unit Height',
        domain=lambda self: [('category_id', '=',
                              self.env.ref('uom.uom_categ_length').id)])
    bmi = fields.Float(
        compute='_compute_bmi',
        string='BMI',
        default=0.0,
        help='Used for Body mass index Calculation')
    bmr = fields.Float(string='BMR', compute='_compute_bmr',
                       help='Used for Body  Metabolic rate Calculation')

    @api.model
    def default_get(self, fields):
        res = super(BodyMeasurement, self).default_get(fields)
        height_uom = self.env.company and\
            self.env.company.default_umo_of_height_id
        weight_uom = self.env.company and\
            self.env.company.default_umo_of_weight_id
        body_pary_uom = self.env.company and\
            self.env.company.default_umo_of_measure_id
        res.update({
            'umo_weight_id': weight_uom.id,
            'umo_height_id': height_uom.id,
            'umo_calf_id': body_pary_uom.id,
            'umo_thigh_id': body_pary_uom.id,
            'umo_hips_id': body_pary_uom.id,
            'umo_waist_id': body_pary_uom.id,
            'umo_biceps_id': body_pary_uom.id,
            'umo_chest_id': body_pary_uom.id,
            'umo_neck_id': body_pary_uom.id,
        })
        if self.env.user.has_group('gym.group_gym_member'):
            res.update({'partner_id': self.env.user.partner_id})
        return res

    @api.depends('height', 'weight')
    def _compute_bmi(self):
        """Calculation of the Body mass index."""
        bmi = 0
        for rec in self.filtered(
                lambda rec: rec.height and rec.weight):
            bmi = rec.weight / (rec.height * rec.height)
        self.bmi = bmi

    @api.depends('height', 'weight', 'partner_id.age')
    def _compute_bmr(self):
        """Calculation of the Basal metabolic rate."""
        bmr = 0
        for measurement_rec in self.filtered(
                lambda measurement_rec: measurement_rec.height and
                measurement_rec.weight):
            bmr = 66.47 + (13.75 * measurement_rec.weight) \
                + (5.0 * measurement_rec.height) \
                - (6.75 * measurement_rec.partner_id.age)
        self.bmr = bmr


class BodyPart(models.Model):
    _name = 'body.part'
    _description = "Body Part"

    name = fields.Char('Body part')


class PedoMeter(models.Model):
    """Model for pedo meter."""

    _name = 'pedo.meter'
    _description = "Pedo Meter"

    partner_id = fields.Many2one('res.partner', 'Pedometer')
    date = fields.Date('Date', required=True)
    steps = fields.Integer('Steps', required=True)
