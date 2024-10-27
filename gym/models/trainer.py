# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    """Inherited this model for trainer's information."""

    _inherit = 'hr.employee'

    is_trainer = fields.Boolean(string='Is Trainer ?')
    specialist_ids = fields.Many2many('gym.skills', 'trainer_skill_rel',
                                      'trainer_id', 'skill_id',
                                      string='Specialization')
    total_session = fields.Integer(
        compute='_compute_calculation_trainer_session',
        string='Total Session')
    user_id = fields.Many2one('res.users', 'User',
                              related='resource_id.user_id', store=True,
                              readonly=False, ondelete="cascade")

    def unlink(self):
        for rec in self:
            user_id = rec.user_id
            rec.user_id = False
            user_id.unlink()
        return super(HrEmployee, self).unlink()

    def _compute_calculation_trainer_session(self):
        """Trainer session count for session smart
        button in trainer form(hr.employee)."""
        for trainer_rec in self:
            trainer_rec.total_session = \
                self.env['calendar.event'].search_count([
                    ('trainer_id', '=', trainer_rec.id)])

    @api.constrains('work_email')
    def _check_work_email(self):
        rec = self.search([('work_email', '=', self.work_email),
                           ('id', '!=', self.id)])
        if rec:
            raise ValidationError(_("You can not have two users with the "
                                    "same login !"))

    @api.model
    def create(self, vals):
        """Method for creating User at trainer creation."""
        res = super(HrEmployee, self).create(vals)
        if not vals.get('user_id'):
            user = self.env['res.users'].create({
                'name': vals.get('name'),
                'login': vals.get('work_email', False),
                'password': self.env.company.default_password or '',
                'groups_id': [(6, 0, [self.env.ref(
                    'gym.group_gym_trainer').id])],
            })
            user.partner_id.write(
                {'email': vals.get('work_email', False)})
            res.write({'user_id': user and user.id or False})
        return res

    def copy(self, default=None):
        if self.is_trainer:
            raise ValidationError(_("Sorry, you can't duplicate a trainer. "))
        return super(HrEmployee, self).copy(default)
