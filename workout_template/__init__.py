# See LICENSE file for full copyright and licensing details.

from . import models
from . import wizard

from odoo import api, SUPERUSER_ID


def _post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    project_record_rule_id = env.ref('project.task_visibility_rule')
    project_record_rule_id.write({'active': False})
