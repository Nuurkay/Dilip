# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProjectTask(models.Model):
    """Inherited project task model for giving the task type whether the task
    is of workout or Diet."""

    _inherit = "project.task"
    _order = 'schedule_date asc'

    schedule_date = fields.Date('Schedule Date',
                                help='Start date and Stop date of the Task')
    reviewer_id = fields.Many2one('res.users', 'Specialist',
                                  help='Reviewer of the Task')
    task_type = fields.Selection([('workout', 'Workout'), ('diet', 'Diet')],
                                 string='Type',
                                 help='Type of the Task [workout]-If task is '
                                      'of Workout Plan [diet]-If task is of '
                                      'Diet Plan')


class ProjectProject(models.Model):
    """Inherited project model for giving the project type whether the task
    is of workout or Diet."""
    _inherit = 'project.project'

    type = fields.Selection([('workout', 'Workout'), ('diet', 'Diet')], 'Type',
                            default=lambda self: self.env.context.
                            get('workout_default', False) or False,
                            help='Type of the Project [workout] '
                                 '-If project is of Workout Plan [diet]-If '
                                 'project is of Diet Plan')
