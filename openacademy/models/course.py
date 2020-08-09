# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OpenAcademyCourse(models.Model):
    _name = 'openacademy.course'
    _description = '''Open Academy Course'''

    name = fields.Char(string="Title", required=True)
    description = fields.Text()

    responsible_id = fields.Many2one(
        'res.users', 
        string="Responsible", 
        index=True, 
        ondelete='set null',
        default=lambda self, *a: self.env.uid
    )

    session_ids = fields.One2many('openacademy.session', 'course_id')
