# See LICENSE file for full copyright and licensing details.

from odoo import models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def _lead_create_contact(self, name, is_company, parent_id=False):
        res = super(CrmLead, self)._lead_create_contact(name, is_company,
                                                        parent_id=parent_id)
        for lead in res:
            lead.customer = True
            lead.is_member = True
        return res
