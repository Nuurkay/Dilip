# See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EmployeeAttendance(models.Model):
    _name = "employee.attendance"
    _description = "Employee Attendance"
    _order = "check_in desc"
    _rec_name = "employee_id"

    @api.model
    def default_get(self, fields):
        res = super(EmployeeAttendance, self).default_get(fields)
        user_id = self.env["res.users"].browse(self.env.uid)
        if user_id.has_group("gym.group_gym_operator") or user_id.has_group(
            "gym.group_gym_manager"
        ):
            res["is_manager"] = True
        return res

    check_in = fields.Datetime(
        string="Check In", default=fields.Datetime.now, required=True
    )
    check_out = fields.Datetime(string="Check Out")
    worked_hours = fields.Float(
        string="Worked Hours", compute="_compute_employee_worked_hours", store=True
    )
    employee_id = fields.Many2one(
        "hr.employee", string="Employee", ondelete="cascade", index=True
    )
    is_manager = fields.Boolean("Is Manager")

    def name_get(self):
        result = []
        for attendance in self:
            empl_name = attendance.employee_id.name
            if not attendance.check_out:
                result.append(
                    (
                        attendance.id,
                        _("%(empl_name)s from %(check_in)s")
                        % {
                            "empl_name": empl_name,
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
                        _("%(empl_name)s from %(check_in)s to %(check_out)s")
                        % {
                            "empl_name": empl_name,
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
    def _compute_employee_worked_hours(self):
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

    @api.constrains("check_in", "check_out", "employee_id")
    def _check_validity(self):
        """Verify the validity of the attendance record compared to the
           others from the same employee. For the same employee we must have :
           * maximum 1 "open" attendance record (without check_out)
           * no overlapping time slices with previous employee records
        """
        for attendance in self:
            # we take the latest attendance before our check_in time and check
            # it doesn't overlap with ours
            last_attendance_before_check_in = False

            last_attendance_before_check_in = self.search(
                [
                    ("employee_id", "=", attendance.employee_id.id),
                    ("check_in", "<=", attendance.check_in),
                    ("id", "!=", attendance.id),
                ],
                order="check_in desc",
                limit=1,
            )

            if (
                last_attendance_before_check_in
                and last_attendance_before_check_in.check_out
                and last_attendance_before_check_in.check_out >= attendance.check_in
            ):
                raise ValidationError(
                    _(
                        "Cannot create new attendance record "
                        "for %(empl_name)s, the employee was already"
                        " checked in on %(datetime)s"
                    )
                    % {
                        "empl_name": attendance.employee_id.name,
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
                        ("employee_id", "=", attendance.employee_id.id),
                        ("check_out", "=", False),
                        ("id", "!=", attendance.id),
                    ],
                    limit=1,
                )
                if no_check_out_attendances:
                    raise ValidationError(
                        _(
                            "Cannot create new attendance"
                            " record for %(empl_name)s,"
                            " the employee hasn't checked"
                            " out since %(datetime)s"
                        )
                        % {
                            "empl_name": attendance.employee_id.name,
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

                last_attendance_before_check_out = self.search(
                    [
                        ("employee_id", "=", attendance.employee_id.id),
                        ("check_in", "<=", attendance.check_out),
                        ("id", "!=", attendance.id),
                    ],
                    order="check_in desc",
                    limit=1,
                )

                if (
                    last_attendance_before_check_out
                    and last_attendance_before_check_in
                    != last_attendance_before_check_out
                ):
                    raise ValidationError(
                        _(
                            "Cannot create new attendance"
                            " record for %(empl_name)s,"
                            " the employee was already"
                            " checked in on %(datetime)s"
                        )
                        % {
                            "empl_name": attendance.employee_id.name,
                            "datetime": fields.Datetime.to_string(
                                fields.Datetime.context_timestamp(
                                    self,
                                    fields.Datetime.from_string(
                                        last_attendance_before_check_out.check_in
                                    ),
                                )
                            ),
                        }
                    )
