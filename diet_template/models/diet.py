# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class DietList(models.Model):
    """New model for creating diet Task."""

    _name = 'diet.list'
    _description = 'Information of task,interval and food items in task.'

    name = fields.Char('Name')
    sequence = fields.Integer("Sequence")
    diet_id = fields.Many2one('diet.master', 'Diet Line')
    food_item_ids = fields.One2many('diet.plan.lines', 'diet_list_id', 'Food')


class DietMaster(models.Model):
    """Information about diet plan and task in the plan and total
    days of task.
    """

    _name = 'diet.master'
    _description = 'Diet Master'

    name = fields.Char("Goal")
    diet_task_ids = fields.One2many('diet.list', 'diet_id', 'Diet')
    total_days = fields.Integer(
        compute="_compute_calculate_total_days",
        string="Total Days Of Diet Plan")
    diet_plan_ids = fields.Many2many('diet.list', 'master_list_rel',
                                     'master_id', 'diet_list_id',
                                     string="Diet Task")

    @api.depends('diet_plan_ids')
    def _compute_calculate_total_days(self):
        """Calculating total days of PLan."""
        for diet_master_rec in self:
            diet_master_rec.total_days = \
                len(diet_master_rec.diet_plan_ids.ids)


class DietPlanLines(models.Model):
    _inherit = 'diet.plan.lines'

    diet_list_id = fields.Many2one('diet.list', 'project task list')
    diet_plan_id = fields.Many2one('project.task', 'Diet plan in task')
