# See LICENSE file for full copyright and licensing details.

import pytz
from datetime import datetime, timedelta
import calendar
from odoo.http import request
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, ustr
from odoo.exceptions import ValidationError


def _get_datetime_based_timezone(src_dt, context={}):
    dt = False
    if src_dt:
        timezone = pytz.timezone(
            request.env['res.users'].with_user(request.env.user).browse([int(
                request.env.user)]).tz or 'UTC')
        dt = pytz.UTC.localize(fields.Datetime.from_string(src_dt))
        dt = dt.astimezone(timezone)
        dt = datetime.strptime(ustr(dt).split('+')[0],
                               DEFAULT_SERVER_DATETIME_FORMAT)
    return dt


class CalendarEvent(models.Model):
    """Inherited this model for Trainer booking."""

    _inherit = 'calendar.event'

    def _get_datatime(self, date):
        user = self.env.user
        local_tz = pytz.timezone(user.tz or 'UTC')
        display_date = datetime.strftime(pytz.utc.localize(
            datetime.strptime(str(date),
                              DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(
            local_tz), "%d/%m/%Y %H:%M:%S")
        return display_date

    name = fields.Char('Training Subject', required=True,)

    trainer_id = fields.Many2one('hr.employee', string='Trainer',
                                 default=lambda self: self.env.context.get(
                                     'traienr_default', False))
    is_trainer_booking = fields.Boolean(
        string='Is Trainer Booking ?',
        default=lambda self: self.env.context.get(
            'booking_default', False))

    @api.model
    def create(self, vals):
        return super(CalendarEvent,
                     self.with_context(booking_default=True)).create(vals)

    @api.onchange('start', 'duration')
    def _onchange_duration(self):
        if self.start:
            start = self.start
            self.start = self.start

            self.stop = start + \
                timedelta(hours=self.duration) - timedelta(seconds=0)

    @api.constrains('start', 'stop', 'start_date',
                    'stop_date')
    def _check_closing_date(self):
        for meeting in self:
            if meeting.start and meeting.stop and\
                    meeting.stop < meeting.start:
                raise ValidationError(
                    _('The ending date and time cannot be earlier than the'
                        ' starting date and time.') + '\n' +
                    _("Meeting '%s' starts '%s' and ends '%s'") % (
                        meeting.name, self._get_datatime(
                            meeting.start),
                        self._get_datatime(meeting.stop))
                )
            if meeting.start_date and meeting.stop_date and\
                    meeting.stop_date < meeting.start_date:
                raise ValidationError(
                    _('The ending date cannot be earlier than the'
                        ' starting date.') + '\n' +
                    _("Meeting '%s' starts '%s' and ends '%s'") % (
                        meeting.name, meeting.start_date, meeting.stop_date)
                )

    @api.constrains('rrule_type', 'trainer_id', 'mo', 'tu', 'we', 'th',
                    'fr', 'sa', 'su', 'week_list', 'month_by', 'recurrency')
    def _check_dayofweek(self):
        dayofweek_list = list(calendar.day_name)
        days_name_list = []
        dayofweek = [res.dayofweek for res in
                     self.trainer_id.resource_calendar_id.attendance_ids]
        if self.recurrency and self.rrule_type == 'weekly':
            dayofweek = list(dict.fromkeys(dayofweek))
            if '0' not in dayofweek and self.mo:
                days_name_list.append(dayofweek_list[0])
            if '1' not in dayofweek and self.tu:
                days_name_list.append(dayofweek_list[1])
            if '2' not in dayofweek and self.we:
                days_name_list.append(dayofweek_list[2])
            if '3' not in dayofweek and self.th:
                days_name_list.append(dayofweek_list[3])
            if '4' not in dayofweek and self.fr:
                days_name_list.append(dayofweek_list[4])
            if '5' not in dayofweek and self.sa:
                days_name_list.append(dayofweek_list[5])
            if '6' not in dayofweek and self.su:
                days_name_list.append(dayofweek_list[6])
            self.with_context(sun=True)
        elif self.recurrency and self.rrule_type == 'monthly' and \
                self.month_by == 'day':
            week_list = [('MO', '0'), ('TU', '1'), ('WE', '2'), ('TH', '3'),
                         ('FR', '4'), ('SA', '5'), ('SU', '6')]
            if dict(week_list).get(self.week_list) not in dayofweek:
                days_name_list.append(
                    dayofweek_list[int(dict(week_list).get(self.week_list))])
        if days_name_list:
            raise ValidationError(
                "Trainer is not available during %s."
                % str(days_name_list[0:]))

    @api.constrains('start', 'stop', 'start_date',
                    'stop_date', 'partner_ids')
    def trainer_booking_datetime(self):
        """Constraint on hour wise booking of trainer(Datetime)."""
        curr_date = fields.Date.today()
        cale_event_obj = self.env['calendar.event']
        if self.is_trainer_booking:
            for event_rec in self:
                if event_rec.start and event_rec.start.date() < curr_date:
                    raise ValidationError(
                        "Booking date must be greater than today's date.")
                # Datetime
                time_ids = cale_event_obj.search([
                    ('trainer_id', '=', event_rec.trainer_id.id),
                    '|', '&',
                    ('start', '<=', event_rec.start),
                    '&', ('stop', '>=', event_rec.start),
                    ('start', '<', event_rec.stop),
                    '&', ('start', '<', event_rec.stop),
                    ('stop', '>', event_rec.start),
                    ('id', '!=', event_rec.id)
                ])

                cale_event_members_ids = cale_event_obj.search([
                    ('partner_ids', 'in', event_rec.partner_ids.ids),
                    '|', '&',
                    ('start', '<=', event_rec.start),
                    '&', ('stop', '>=', event_rec.start),
                    ('start', '<', event_rec.stop),
                    '&', ('start', '<', event_rec.stop),
                    ('stop', '>', event_rec.start),
                    ('id', '!=', event_rec.id)
                ])
                if time_ids:
                    raise ValidationError(
                        "Trainer Is booked, Please Choose Different Trainer.")
                if cale_event_members_ids:
                    member_list = []
                    for rec in cale_event_members_ids:
                        member_list +=\
                            [val.name for val in rec.partner_ids.filtered(
                                lambda val: val.id in event_rec.partner_ids.ids
                            )]
                    raise ValidationError(
                        "Member %s Is this time not available,"
                        "Please Choose Different time or "
                        "Member." % str(member_list[0:]))

    @api.constrains('start', 'stop', 'start_date',
                    'stop_date')
    def trainer_time(self):
        """Constraint for booking Between the Trainer's Working Schedule."""
        rec_cale_att_obj = self.env['resource.calendar.attendance']
        for event_rec in self:
            if event_rec.allday:
                raise ValidationError(
                    "You can't book the Trainer for the whole day.")
            else:
                if event_rec.trainer_id.resource_calendar_id:
                    if event_rec.is_trainer_booking:
                        trainer_timezone = event_rec.trainer_id.user_id.tz
                        start = _get_datetime_based_timezone(
                            event_rec.start, self._context)
                        stop = _get_datetime_based_timezone(
                            event_rec.stop, self._context)
                        resourc_calendar = event_rec.trainer_id.\
                            resource_calendar_id

                        # Searching in resource.calendar.attendance for
                        # matching the weekday with Start date and Stop date
                        working_schedule_ids = rec_cale_att_obj.search([
                            ('calendar_id', '=', resourc_calendar.id), '|',
                            ('dayofweek', '=', str(start.weekday())),
                            ('dayofweek', '=', str(stop.weekday()))
                        ])
                        # Time Zone of the trainer
                        if not trainer_timezone:
                            raise ValidationError(
                                "Please configure time zone of Trainer.")
                        else:
                            can_be_scheduled = False
                            # Looping on the Trainer Schedule to check if he is
                            # available
                            for attendance_recs in working_schedule_ids:
                                # Converting the start time in Datetime format
                                start_convert = '{0:02.0f}:{1:02.0f}'.format(
                                    *divmod(attendance_recs.hour_from * 60,
                                            60))
                                start_dt = datetime.strptime(
                                    str(event_rec.start.date()
                                        ) + ' ' +
                                    start_convert + ':00',
                                    DEFAULT_SERVER_DATETIME_FORMAT)
                                # Converting the End time in Datetime format
                                stop_convert = '{0:02.0f}:{1:02.0f}'.format(
                                    *divmod(attendance_recs.hour_to * 60, 60))
                                stop_dt = datetime.strptime(
                                    str(event_rec.stop.date()) +
                                    ' ' + stop_convert + ':00',
                                    DEFAULT_SERVER_DATETIME_FORMAT)
                                if start >= start_dt and \
                                        stop <= stop_dt:
                                    can_be_scheduled = True
                            if not can_be_scheduled:
                                raise ValidationError(
                                    "Trainer is not available during this"
                                    " time")

    @api.constrains('start', 'stop', 'start_date',
                    'stop_date')
    def trainer_leave(self):
        """Constraint when Trainer is on Leave."""
        hr_leave_obj = self.env['hr.leave']
        for event_rec in self:
            if event_rec.allday:
                # searchig in hr.leave for Date(allday=True)
                leave_date_ids = hr_leave_obj.search([
                    ('employee_id.id', '=', event_rec.trainer_id.id),
                    '|', '&', ('date_from', '<=', event_rec.start_date),
                    ('date_to', '>=', event_rec.start_date),
                    '&', ('date_from', '<=', event_rec.stop_date),
                    ('date_to', '>=', event_rec.start_date),
                    ('id', '!=', event_rec.id)
                ])
                if leave_date_ids:
                    raise ValidationError("Trainer Is on Leave on this date.")
            else:
                # Searching on hr.leave for Datetime
                leaves_ids = hr_leave_obj.search([
                    ('employee_id.id', '=', event_rec.trainer_id.id),
                    '|', '&', ('date_from', '<=', event_rec.start),
                    ('date_to', '>=', event_rec.start),
                    '&', ('date_from', '<=', event_rec.stop),
                    ('date_to', '>=', event_rec.start),
                    ('id', '!=', event_rec.id)
                ])
                if leaves_ids:
                    raise ValidationError("Trainer Is on Leave.")
        return True
