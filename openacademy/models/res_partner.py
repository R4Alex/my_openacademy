# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean()
    sessions_ids = fields.Many2many('openacademy.session', string="Attended Sessions")
    student = fields.Boolean(default=True)
