# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ExerciseLines(models.Model):
    """Information about body parts and exercise."""

    _name = 'exercise.lines'
    _description = "Exercise Lines"

    exercise_name_id = fields.Many2one('exercise.exercise', 'Exercise name')
    sets = fields.Integer('Sets')
    reps_ids = fields.Many2many('repeat.repeat', 'exercise_repeat_rel',
                                string="Repetition")
    sequence = fields.Integer('Sequence')


class RepeatRepeat(models.Model):
    _name = 'repeat.repeat'
    _description = "Repeated"

    name = fields.Integer('Reps', required=1)


class ExerciseExercise(models.Model):
    """Information about Exercise and Equipment."""

    _name = 'exercise.exercise'
    _description = "Exercise Exercise"

    name = fields.Char('Name')
    exercise_type_ids = fields.Many2many(
        'exercise.type', string='Exercise For')
    equipment_id = fields.Many2one('product.template', 'Equipment')
    exercise_images_ids = fields.Many2many('ir.attachment', string='Images')
    exercise_images_ids = fields.One2many(
        'ir.attachment',
        'exercise_id',
        string='Attachment',
    )

    benefits = fields.Text('Benefits of Exercise')
    steps = fields.Text('Steps To Follow')
    exercise_video_ids = fields.One2many(
        'exercise.videos', 'exercise_id', 'Videos')


class Attachment(models.Model):
    _inherit = 'ir.attachment'
    _description = 'Ir Attachment'

    exercise_id = fields.Many2one(
        'exercise.exercise',
        string='Exercise',
    )

    # @api.onchange('datas')
    # def _onchange_datas(self):
    #     self.name = self.datas


class ExerciseType(models.Model):
    _name = 'exercise.type'
    _description = "Exercise Type"

    name = fields.Char('Name', required=1)


class ExerciseVideos(models.Model):
    """Model for Exercise Videos."""

    _name = 'exercise.videos'
    _description = "Exercise Videos"

    name = fields.Char('Name', required=True)
    link = fields.Char('Link', required=True)
    exercise_id = fields.Many2one('exercise.exercise', 'Exercises')
