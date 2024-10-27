# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AttendanceSummaryWizard(models.TransientModel):

    _name = "attendance.summary.wizard"
    _description = "Attendance Summary Wizard"

    summary_type = fields.Selection(
        [("weekly", "Weekly"), ("monthly", "Monthly")],
        string="Summary Type",
        default="weekly",
        required=True,
    )
    from_date = fields.Date(
        string="From Date", default=fields.Date.context_today, required=True
    )
    partner_ids = fields.Many2many("res.partner", string="Partner")

    def print_report(self):
        context = self.env.context
        data = self.read()[0]
        datas = {
            "ids": [],
            "model": "partner.attendance",
            "data_form": data,
            "form": data,
        }
        return (
            self.env.ref("scs_partner_attendance.action_attendance_report")
            .with_context(context)
            .report_action([], data=datas)
        )
