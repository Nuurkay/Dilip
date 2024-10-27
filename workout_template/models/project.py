# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Project(models.Model):
    """Inherited this model for creating workout project."""

    _inherit = 'project.project'

    product_id = fields.Many2one('product.product', string='Client Product')


class Task(models.Model):
    """Details of Exercise task in workout plan."""

    _inherit = "project.task"
    _order = 'schedule_date asc'

    task_list_id = fields.Many2one('task.list', string='Task List')
    task_exercise_ids = fields.One2many('exercise.lines', 'task_exercise_id',
                                        string='Exercise')
    workout_master_id = fields.Many2one('workout.master',
                                        string='Workout Master')

    @api.constrains('schedule_date', 'date_deadline')
    def check_date(self):
        """Constraint on task date."""
        if self.schedule_date and self.date_deadline and \
                self.schedule_date > self.date_deadline:
            raise ValidationError(
                _("End time must be greater than the start time."))


class TaskList(models.Model):
    """Information of task,exercise in task and repetition of the task."""

    _name = 'task.list'
    _description = 'Task List'

    name = fields.Char(string="Workout Name")
    sequence = fields.Integer(string="Sequence")
    workout_id = fields.Many2one('workout.master', string='Workout Line')
    exercise_ids = fields.One2many('exercise.lines', 'special_exercises_id',
                                   string='Exercise')
    repeat_days = fields.Integer(string="Repetition", default=1)


class WorkoutMaster(models.Model):
    """Information about workout plan,parent workout plan and task in the plan.
    """

    _name = 'workout.master'
    _description = 'Workout Master'

    @api.depends('task_description_ids')
    def _cal_total_days(self):
        """Count of the total Repeat days."""
        for workout_rec in self:
            re_day = 0
            for repeat_day in workout_rec.task_description_ids:
                re_day += repeat_day.repeat_days
            workout_rec.repeat_days_of_task = re_day

    name = fields.Char(string="Goal")
    task_description_ids = fields.One2many('task.list', 'workout_id',
                                           string='Workout')
    parent_id = fields.Many2one('workout.master', string='Parent Plan')
    trainer_id = fields.Many2one('res.users', string='Specialist')
    skill_id = fields.Many2one('gym.skills', string="Specialist's Skill")
    repeat_days_of_task = fields.Integer(compute="_cal_total_days",
                                         string="No Of Days")


class ExerciseLines(models.Model):
    _inherit = 'exercise.lines'

    special_exercises_id = fields.Many2one('task.list',
                                           string='Project task list')
    task_exercise_id = fields.Many2one('project.task',
                                       string='Exercise in task')
