# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HrEmployee(models.Model):
    """Inherited this model for trainer's information."""

    _inherit = 'hr.employee'

    workout_with_trainee = fields.Integer(
        "Workout with Trainee", compute='_compute_workout_with_trainee')

    def _compute_workout_with_trainee(self):
        for rec in self:
            rec.workout_with_trainee = \
                self.env['calendar.event'].search_count(
                    [('trainer_id', '=', rec.id)])

    def get_trainer_session(self):
        session_obj = self.env['calendar.event']
        for rec in self:
            session_ids = session_obj.search([('trainer_id.id','=',rec.id)])
            return {
            'type': 'ir.actions.act_window',
            'name': 'Trainer Booking',
            'view_mode': 'tree,form',
            'res_model': 'calendar.event',
            'domain': [('id', 'in', session_ids.ids)]
        }
