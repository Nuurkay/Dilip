# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Partner(models.Model):

    _inherit = 'res.partner'

    workout_with_trainer = fields.Integer(
        "Workout with Trainee", compute='_compute_workout_with_trainer')

    def _compute_workout_with_trainer(self):
        for rec in self:
            rec.workout_with_trainer = \
                self.env['calendar.event'].search_count(
                    [('partner_ids', '=', rec.id)])

    def schedule_meeting(self):
        action = super(Partner, self).schedule_meeting()
        action['context'].update({'default_is_trainer_booking': 1})
        return action

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self.env.user.has_group('gym.group_gym_trainer'):
            partner_list = []
            calendar_event_ids = self.env['calendar.event'].search(
                [('trainer_id.user_id', '=', self.env.user.id)])
            for rec in calendar_event_ids:
                partner_list += rec.partner_ids.ids
            args.append(('id', 'in', partner_list))
        return super(Partner, self).search(args)
