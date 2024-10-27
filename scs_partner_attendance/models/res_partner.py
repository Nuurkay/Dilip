# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_attendance_ids = fields.One2many(
        "partner.attendance", "partner_id", help="list of attendances for the partner"
    )
    last_partner_attendance_id = fields.Many2one(
        "partner.attendance", compute="_compute_last_attendance_id", store=True
    )
    attendance_state = fields.Selection(
        string="Attendance Status",
        compute="_compute_attendance_state",
        selection=[("checked_out", "Checked out"), ("checked_in", "Checked in")],
    )

    @api.depends("partner_attendance_ids")
    def _compute_last_attendance_id(self):
        for partner in self:
            partner.last_partner_attendance_id = self.env["partner.attendance"].search(
                [("partner_id", "=", partner.id)], limit=1
            )

    @api.depends(
        "last_partner_attendance_id.check_in",
        "last_partner_attendance_id.check_out",
        "last_partner_attendance_id",
    )
    def _compute_attendance_state(self):
        for partner in self:
            att = partner.last_partner_attendance_id.sudo()
            partner.attendance_state = (
                att and not att.check_out and "checked_in" or "checked_out"
            )
