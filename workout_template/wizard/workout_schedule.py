# See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class TaskSchedule(models.TransientModel):
    """Information about goal,task start and stop for assign workout
    project."""

    _name = 'task.scheduling'
    _description = 'Task Scheduling'

    member_id = fields.Many2one('res.partner', string='Member')
    goal_id = fields.Many2one('workout.master', string='Goal')
    total_days = fields.Integer(string="Total Days Of Plan",
                                compute='_compute_total_days')
    start_date = fields.Date(string='Start Date',
                             default=datetime.strftime(
                                 datetime.now(), DEFAULT_SERVER_DATE_FORMAT))
    end_date = fields.Date(string='End Date')
    sub_plan_ids = fields.Many2many('workout.master', string='Sub Plan')

    @api.constrains('start_date', 'end_date')
    def _check_date(self):
        """Constrain on Start and End date."""
        if self.end_date and self.start_date and \
                self.start_date > self.end_date:
            raise ValidationError(_("End date must be greater than"
                                    " start date."))

    @api.onchange('goal_id')
    def _onchange_fill_parent_plans(self):
        """Sub plan changes based on goal."""
        for task_schedule_rec in self:
            current_plan = task_schedule_rec.goal_id
            plan_ids = []
            while current_plan.parent_id:
                current_plan = current_plan.parent_id
                plan_ids.append(current_plan.id)
            self.sub_plan_ids = plan_ids and [(6, 0, plan_ids)] or False
            return {'domain': {'sub_plan_ids': [('id', 'in', plan_ids)]}}

    @api.depends('start_date', 'goal_id', 'sub_plan_ids')
    def _compute_total_days(self):
        total_days = self.goal_id.repeat_days_of_task or 0
        for goal in self.sub_plan_ids:
            total_days = total_days + goal.repeat_days_of_task
        self.total_days = total_days

    @api.onchange('sub_plan_ids', 'goal_id', 'start_date')
    def _onchange_total_plan_days(self):
        """Method for assign total days based on goal."""
        # End Date assign
        if not self.total_days:
            self.start_date = self.end_date = datetime.strftime(
                datetime.now(), DEFAULT_SERVER_DATE_FORMAT)
        elif self.start_date:
            self.end_date = self.start_date + timedelta(
                days=self.total_days - 1)

    def schedule_project(self):
        """Method for automatically assign workout plan to member."""
        project = self.env['project.project']
        project_task = self.env['project.task']
        trainer = self.env['workout.master']
        user_obj = self.env['res.users']
        project_kanban = self.env.ref('project.view_project_kanban', False)
        goal_list = []
        project_list = []
        project_task_rec = project_task.search([
            ('workout_master_id', 'in',
             self.sub_plan_ids.ids + [self.goal_id.id]),
            ('partner_id', '=', self.member_id.id),
            ('schedule_date', '>=', self.start_date),
            ('schedule_date', '<=', self.end_date)])
        if project_task_rec:
            raise ValidationError(_('You can\'t create Workout schedule'
                                    ' task for this duration because'
                                    ' it\'s already created.'))
        for task_schedule_rec in self:
            user_rec = user_obj.search([('partner_id', '=',
                                         task_schedule_rec.member_id.id)],
                                       limit=1)
            if not user_rec:
                raise ValidationError(_('Please make the customer as user'))
            if not task_schedule_rec.total_days:
                raise ValidationError(_('You can\'t created workout schedule'
                                        ' with total days of zero.'))
            goal_list.append(task_schedule_rec.goal_id)
            start_tm = task_schedule_rec.start_date
            if task_schedule_rec.sub_plan_ids:
                for sub_plan_rec in task_schedule_rec.sub_plan_ids:
                    goal_list.append(sub_plan_rec)
            for task in goal_list:
                trainer_rec = trainer.search([('id', '=', task.id)])
                # Creating Project
                val = {
                    'name': task_schedule_rec.member_id.name +
                    "'s " + task.name + ' Schedule',
                    'type': 'workout',
                    'partner_id': task_schedule_rec.member_id.id,
                    'privacy_visibility': 'portal'
                }
                project_id = project.create(val)
                for sub_task in task.task_description_ids:
                    # Day wise assign task
                    for repeat_task in range(sub_task.repeat_days):
                        exercise_list = []
                        # assigning exercise in task
                        for exercise in sub_task.exercise_ids:
                            vals = {
                                'exercise_name_id':
                                    exercise.exercise_name_id.id,
                                'sets': exercise.sets,
                                'reps_ids': [(6, 0, exercise.reps_ids.ids)],
                            }
                            exercise_list.append((0, 0, vals))
                        # creating task and assign it to project
                        project_task.create({
                            'name': sub_task.name + " Plan ",
                            'project_id': project_id.id,
                            'task_exercise_ids': exercise_list,
                            'schedule_date': start_tm,
                            'user_id': user_rec.id,
                            'sequence': sub_task.sequence,
                            'reviewer_id': trainer_rec.trainer_id.id,
                            'workout_master_id': task.id,
                            'task_type': 'workout'
                        })
                        start_tm = start_tm + timedelta(days=1)
                        project_list.append(project_id.id)
        return {
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', project_list)],
            'view_type': 'form',
            'view_mode': 'kanban,tree,form',
            'res_model': 'project.project',
            'view_id': project_kanban.id,
            'views': [(project_kanban.id, 'kanban'), (False, 'form')],
            'context': {'create': False},
            'target': 'new'
        }
