# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OpenAcademySession(models.Model):
    _name = 'openacademy.course'
    _description = '''Open Academy Session'''

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
