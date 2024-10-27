# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class PartnerAttendance(models.Model):
    _inherit = "partner.attendance"

    @api.model
    def default_get(self, fields):
        res = super(PartnerAttendance, self).default_get(fields)
        user_id = self.env["res.users"].browse(self.env.uid)
        if user_id.partner_id.is_member:
            res["is_member"] = True
        return res

    is_member = fields.Boolean("Is member")
