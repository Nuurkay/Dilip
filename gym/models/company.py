# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    default_password = fields.Char('Password', default='gym',
                                   help="""This will be used as a
                                   default password when a
                                   user gets automatically created
                                   when an employee is created!""")
    default_umo_of_height_id = fields.Many2one('uom.uom',
                                               string='Unit of Height')
    default_umo_of_weight_id = fields.Many2one('uom.uom',
                                               string='Unit of Weight')
    default_umo_of_measure_id = fields.Many2one('uom.uom',
                                                string='Unit of Body Part '
                                                'Measurement')
