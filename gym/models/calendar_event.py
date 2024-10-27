# See LICENSE file for full copyright and licensing details.

from odoo import api, models


class CalendarEvent(models.Model):

    _inherit = 'calendar.event'

    @api.model
    def inactive_rule(self):
        rule_rec = self.env.ref('calendar.calendar_event_rule_employee',
                                raise_if_not_found=False)
        if rule_rec and rule_rec.active:
            rule_rec.active = False
