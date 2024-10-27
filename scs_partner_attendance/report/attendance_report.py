# See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta

import pytz

from odoo import api, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class PartnerAttendanceReport(models.AbstractModel):
    _name = "report.scs_partner_attendance.attendance_summary_report"
    _description = "Attendance Report"

    def get_next_date(self, from_date):
        next_month = from_date.replace(day=28) + timedelta(days=4)
        last_date = datetime.strftime(
            next_month - timedelta(days=next_month.day), DEFAULT_SERVER_DATE_FORMAT
        )
        return last_date

    def _get_data(self, context):
        res = {}
        attendance = {}
        from_date = datetime.strptime(
            context.get("from_date"), DEFAULT_SERVER_DATE_FORMAT
        )
        if context.get("summary_type") == "weekly":
            to_date = from_date + timedelta(weeks=1)
        else:
            to_date = self.get_next_date(from_date)
        for rec in context.get("partner_ids"):
            partner_attendance_ids = self.env["partner.attendance"].search(
                [
                    ("check_in", ">=", context.get("from_date")),
                    ("check_in", "<=", to_date),
                    ("partner_id", "=", rec),
                ]
            )
            partner_id = self.env["res.partner"].browse(rec)
            if partner_attendance_ids:
                attendance.update({partner_id: partner_attendance_ids})
        res.update({"to_date": to_date, "partner_attendance_ids": attendance})
        return res

    def _get_days_name(self, check_in_date):
        return check_in_date.strftime("%A")

    def _get_datatime(self, date):
        user = self.env.user
        local_tz = pytz.timezone(user.tz or "UTC")
        display_date = (
            date
            and datetime.strftime(
                pytz.utc.localize(
                    datetime.strptime(str(date), DEFAULT_SERVER_DATETIME_FORMAT)
                ).astimezone(local_tz),
                "%d/%m/%Y %H:%M:%S",
            )
            or ""
        )
        return display_date

    @api.model
    def _get_report_values(self, docids, data=None):
        context = self.env.context
        data = data if data is not None else {}
        report = self.env.ref("scs_partner_attendance.action_attendance_report")
        model = context.get("active_model")
        docs = self.env[model].browse(context.get("active_id"))
        return {
            "doc_ids": docids,
            "doc_model": report.model,
            "docs": docs,
            "data": data,
            "get_data": self._get_data(data.get("data_form")),
            "get_days_name": self._get_days_name,
            "get_datatime": self._get_datatime,
        }
