# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class GymSkills(models.Model):
    _name = 'gym.skills'
    _description = "Gym Skills"

    name = fields.Char('Skill', required=True)
    code = fields.Char('Code')
