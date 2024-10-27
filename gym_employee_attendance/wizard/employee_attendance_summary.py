# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EmployeeAttendanceWizard(models.TransientModel):

    _name = "employee.attendance.summary.wizard"
    _description = "Employee Attendance Summary Wizard"

    summary_type = fields.Selection(
        [("weekly", "Weekly"), ("monthly", "Monthly")],
        string="Summary Type",
        default="weekly",
        required=True,
    )
    from_date = fields.Date(
        string="From Date", default=fields.Date.context_today, required=True
    )
    employee_ids = fields.Many2many(
        "hr.employee", string="Trainers", domain=[("is_trainer", "=", True)]
    )

    def print_report(self):
        context = self.env.context
        data = self.read()[0]
        datas = {
            "ids": [],
            "model": "employee.attendance",
            "data_form": data,
            "form": data,
        }
        return (
            self.env.ref("gym_employee_attendance.action_employee_report")
            .with_context(context)
            .report_action([], data=datas)
        )
