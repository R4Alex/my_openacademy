# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OpenAcademySession(models.Model):
    _name = 'openacademy.session'
    _description = '''Open Academy Session'''

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6,2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
