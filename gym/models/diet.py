# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class DietPlan(models.Model):
    """Model for creating diet plan."""

    _name = 'diet.plan'
    _description = "Model for creating diet plan"

    name = fields.Char('Name')
    diet_plans_ids = fields.One2many('diet.plan.lines', 'plan_id', 'Plans')


class DietPlanLines(models.Model):
    """Model for add interval and food item in diet plan."""

    _name = 'diet.plan.lines'
    _description = "Diet Plan Lines"

    interval = fields.Selection([('early_morning', 'Early Morning'),
                                 ('breakfast', 'Breakfast'),
                                 ('pre_lunch', 'Pre Lunch'),
                                 ('lunch', 'Lunch'),
                                 ('snack', 'Snack'),
                                 ('dinner', 'Dinner')],
                                'Interval',
                                help='Interval for Eating the food')
    plan_id = fields.Many2one('diet.plan', 'Plans')
    food_item_ids = fields.One2many('food.item', 'food_id', 'Food Items',
                                    help='Foods and interval')


class FoodItem(models.Model):
    """Model for adding food item in diet plan."""

    _name = 'food.item'
    _description = "Food Item"

    food_name_id = fields.Many2one('product.template', 'Food Item')
    quantity = fields.Integer(string='Qty', help='Quantity of Food Items')
    food_id = fields.Many2one('diet.plan.lines', 'Food Items',
                              help='Select Food Items')
    measure_unit_id = fields.Many2one('uom.uom', string='Measurement Unit',
                                      help='Measurement Unit for Food item')
