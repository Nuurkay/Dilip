# See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class DietSchedule(models.TransientModel):
    """object for taking information about Diet schedule."""

    _name = 'diet.scheduling'
    _description = 'Diet Schedule'

    member_id = fields.Many2one('res.partner', string='Member')
    goal_id = fields.Many2one('diet.master', string='Goal')
    total_days = fields.Integer(string="Total Days Of Plan",
                                compute='_compute_total_days')
    start_date = fields.Date(string='Start Date',
                             default=datetime.strftime(
                                 datetime.now(), DEFAULT_SERVER_DATE_FORMAT))
    end_date = fields.Date(string='End Date')

    @api.onchange('goal_id', 'start_date')
    def _onchange_total_diet_plan_days(self):
        """Method for assign total days based on goal."""
        # End Date assign
        if not self.total_days:
            self.end_date = datetime.strftime(
                datetime.now(), DEFAULT_SERVER_DATE_FORMAT)
        elif self.start_date:
            self.end_date = \
                self.start_date + timedelta(days=self.total_days - 1)

    @api.depends('goal_id', 'start_date')
    def _compute_total_days(self):
        # Set the total Days
        self.total_days = self.goal_id.total_days

    def schedule_project(self):
        """Method for assign workout project to member."""
        project = self.env['project.project']
        project_task = self.env['project.task']
        user_obj = self.env['res.users']
        project_kanban = self.env.ref('project.view_project_kanban', False)
        for diet_schedule_rec in self:
            user_rec = user_obj.search(
                [('partner_id', '=', diet_schedule_rec.member_id.id)])
            if not user_rec:
                raise ValidationError(_('Please make the customer as user'))
            elif not diet_schedule_rec.total_days:
                raise ValidationError(_('You can\'t created diet schedule '
                                        'with total days of zero.'))
            else:
                # Creating the project
                val = {
                    'name': diet_schedule_rec.member_id.name + "'s " +
                    diet_schedule_rec.goal_id.name + ' Schedule',
                    'type': 'diet',
                    'partner_id': diet_schedule_rec.member_id.id
                }
            project_id = project.create(val)
            start_tm = diet_schedule_rec.start_date
            for task_rec in diet_schedule_rec.goal_id.diet_plan_ids:
                interval_list = []
                # loop on diet paln lines
                for diet_line in task_rec.food_item_ids:
                    food_list = []
                    # loop omn food items
                    for food_rec in diet_line.food_item_ids:
                        food_list.append((0, 0, {
                            'food_name_id': food_rec.food_name_id.id,
                            'quantity': food_rec.quantity
                        }))
                    interval_list.append((0, 0, {
                        'interval': diet_line.interval,
                        'food_item_ids': food_list
                    }))
                # creating task and assign it to project
                project_task.create({'name': task_rec.name + " Plan ",
                                     'project_id': project_id.id,
                                     'diet_plan_ids': interval_list,
                                     'schedule_date': start_tm,
                                     'user_id': user_rec.id,
                                     'sequence': task_rec.sequence,
                                     'task_type': 'diet'
                                     })
                start_tm = start_tm + timedelta(days=1)
        return {
            'type': 'ir.actions.act_window',
            'domain': [('id', '=', project_id.id)],
            'binding_view_types': 'form',
            'view_mode': 'kanban,tree,form',
            'res_model': 'project.project',
            'view_id': project_kanban.id,
            'views': [(project_kanban.id, 'kanban'), (False, 'form')],
            'context': dict(create=False),
            'target': 'new'
        }
