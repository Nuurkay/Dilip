# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    employee_attendance_ids = fields.One2many(
        "employee.attendance",
        "employee_id",
        help="list of attendances for the employee",
    )
    last_employee_attendance_id = fields.Many2one(
        "employee.attendance",
        compute="_compute_last_employee_attendance_id",
        store=True,
    )
    attendance_state = fields.Selection(
        string="Attendance Status",
        compute="_compute_employee_attendance_state",
        selection=[("checked_out", "Checked out"), ("checked_in", "Checked in")],
    )

    @api.depends("employee_attendance_ids")
    def _compute_last_employee_attendance_id(self):
        for employee in self:
            employee.last_employee_attendance_id = self.env[
                "employee.attendance"
            ].search([("employee_id", "=", employee.id)], limit=1)

    @api.depends(
        "last_employee_attendance_id.check_in",
        "last_employee_attendance_id.check_out",
        "last_employee_attendance_id",
    )
    def _compute_employee_attendance_state(self):
        for employee in self:
            att = employee.last_employee_attendance_id.sudo()
            employee.attendance_state = (
                att and not att.check_out and "checked_in" or "checked_out"
            )
