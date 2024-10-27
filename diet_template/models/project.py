# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Project(models.Model):
    """Inherited Project model for creating diet project."""

    _inherit = 'project.project'

    product_id = fields.Many2one('product.product', string='Client Product')
    type = fields.Selection([('workout', 'Workout'), ('diet', 'Diet')], 'Type')


class Task(models.Model):
    """Inherited Project Task model for creating diet project."""

    _inherit = "project.task"
    _order = 'schedule_date asc'
    _description = 'Details of task in diet plan.'

    diet_plan_ids = fields.One2many(
        'diet.plan.lines', 'diet_plan_id', 'Diet Plan')
