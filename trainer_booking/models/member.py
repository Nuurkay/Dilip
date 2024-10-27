# See LICENSE file for full copyright and licensing details.

from odoo import api, models


class BodyMeasurement(models.Model):

    _inherit = 'body.measurement'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self.env.user.has_group('gym.group_gym_trainer'):
            partner_list = []
            calendar_event_ids = self.env['calendar.event'].search(
                [('trainer_id.user_id', '=', self.env.user.id)])
            for rec in calendar_event_ids:
                partner_list += rec.partner_ids.ids
            args.append(('partner_id', 'in', partner_list))
        return super(BodyMeasurement, self).search(args)
