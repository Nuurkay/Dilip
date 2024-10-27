# See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PartnerAttendance(models.Model):
    _name = "partner.attendance"
    _description = "Partner Attendance"
    _order = "check_in desc"
    _rec_name = "partner_id"

    partner_id = fields.Many2one(
        "res.partner", string="Partner", ondelete="cascade", index=True,
    )
    check_in = fields.Datetime(
        string="Check In", default=fields.Datetime.now, required=True
    )
    check_out = fields.Datetime(string="Check Out")
    worked_hours = fields.Float(
        string="Worked Hours", compute="_compute_worked_hours", store=True
    )

    def name_get(self):
        result = []
        for attendance in self:
            partner_name = attendance.partner_id.name
            if not attendance.check_out:
                result.append(
                    (
                        attendance.id,
                        _("%(partner_name)s from %(check_in)s")
                        % {
                            "partner_name": partner_name,
                            "check_in": fields.Datetime.to_string(
                                fields.Datetime.context_timestamp(
                                    attendance,
                                    fields.Datetime.from_string(attendance.check_in),
                                )
                            ),
                        },
                    )
                )
            else:
                result.append(
                    (
                        attendance.id,
                        _("%(partner_name)s from %(check_in)s to %(check_out)s")
                        % {
                            "partner_name": partner_name,
                            "check_in": fields.Datetime.to_string(
                                fields.Datetime.context_timestamp(
                                    attendance,
                                    fields.Datetime.from_string(attendance.check_in),
                                )
                            ),
                            "check_out": fields.Datetime.to_string(
                                fields.Datetime.context_timestamp(
                                    attendance,
                                    fields.Datetime.from_string(attendance.check_out),
                                )
                            ),
                        },
                    )
                )
        return result

    @api.depends("check_in", "check_out")
    def _compute_worked_hours(self):
        for attendance in self:
            if attendance.check_out:
                dt_diff = attendance.check_out - attendance.check_in
                attendance.worked_hours = dt_diff.total_seconds() / 3600.0

    @api.constrains("check_in", "check_out")
    def _check_validity_check_in_check_out(self):
        """Verify if check_in is earlier than check_out."""
        for attendance in self:
            if (
                attendance.check_in
                and attendance.check_out
                and attendance.check_out < attendance.check_in
            ):
                raise ValidationError(
                    _('"Check Out" time cannot be earlier than "Check In" ' "time.")
                )

    @api.constrains("check_in", "check_out", "partner_id")
    def _check_validity(self):
        """Verify the validity of the attendance record compared to the
        others from the same partner. For the same partner we must have :
        * maximum 1 "open" attendance record (without check_out)
        * no overlapping time slices with previous partner records
        """
        for attendance in self:
            # we take the latest attendance before our check_in time and check
            # it doesn't overlap with ours
            last_attendance_before_check_in_recs = self.search(
                [
                    ("partner_id", "=", attendance.partner_id.id),
                    ("check_in", "<=", attendance.check_in),
                    ("id", "!=", attendance.id),
                ],
                order="check_in desc",
                limit=1,
            )
            if (
                last_attendance_before_check_in_recs
                and last_attendance_before_check_in_recs.check_out
                and last_attendance_before_check_in_recs.check_out
                >= attendance.check_in
            ):
                raise ValidationError(
                    _(
                        "Cannot create new attendance record"
                        " for %(partner_name)s, the partner was already"
                        " checked in on %(datetime)s"
                    )
                    % {
                        "partner_name": attendance.partner_id.name,
                        "datetime": fields.Datetime.to_string(
                            fields.Datetime.context_timestamp(
                                self, fields.Datetime.from_string(attendance.check_in)
                            )
                        ),
                    }
                )
            if not attendance.check_out:
                # if our attendance is "open" (no check_out), we verify there
                # is no other "open" attendance
                no_check_out_attendances = False
                no_check_out_attendances = self.search(
                    [
                        ("partner_id", "=", attendance.partner_id.id),
                        ("check_out", "=", False),
                        ("id", "!=", attendance.id),
                    ],
                    limit=1,
                )
                if no_check_out_attendances:
                    raise ValidationError(
                        _(
                            "Cannot create new attendance"
                            " record for %(partner_name)s,"
                            " the partner hasn't"
                            " checked out since"
                            " %(datetime)s"
                        )
                        % {
                            "partner_name": attendance.partner_id.name,
                            "datetime": fields.Datetime.to_string(
                                fields.Datetime.context_timestamp(
                                    self,
                                    fields.Datetime.from_string(
                                        no_check_out_attendances.check_in
                                    ),
                                )
                            ),
                        }
                    )

            else:
                # we verify that the latest attendance with check_in time
                # before our check_out time
                # is the same as the one before our check_in time computed
                # before, otherwise it overlaps
                last_attendance_before_check_out_recs = self.search(
                    [
                        ("partner_id", "=", attendance.partner_id.id),
                        ("check_in", "<=", attendance.check_out),
                        ("id", "!=", attendance.id),
                    ],
                    order="check_in desc",
                    limit=1,
                )
                if (
                    last_attendance_before_check_out_recs
                    and last_attendance_before_check_in_recs
                    != last_attendance_before_check_out_recs
                ):
                    raise ValidationError(
                        _(
                            "Cannot create new attendance"
                            " record for %(partner_name)s,"
                            " the partner was"
                            " already checked in on"
                            " %(datetime)s"
                        )
                        % {
                            "partner_name": attendance.partner_id.name,
                            "datetime": fields.Datetime.to_string(
                                fields.Datetime.context_timestamp(
                                    self,
                                    fields.Datetime.from_string(
                                        last_attendance_before_check_out_recs.check_in
                                    ),
                                )
                            ),
                        }
                    )
