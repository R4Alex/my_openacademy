# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OpenAcademySession(models.Model):
    _name = 'openacademy.course'
    _description = '''Open Academy Session'''

    name = fields.Char(string="Title", required=True)
    description = fields.Text()

    responsible_id = fields.Many2one(
        'res.users', 
        string="Responsible", 
        index=True, 
        ondelete='set null'
    )

    session_ids = fields.One2many('openacademy.session', 'course_id')
