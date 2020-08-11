# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions


class OpenAcademySession(models.Model):
    _name = 'openacademy.session'
    _description = '''Open Academy Session'''

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    end_date = fields.Date(store=True, compute="_get_end_date", inverse="_set_end_date")
    duration = fields.Float(digits=(6,2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one('res.partner', string='instructor')

    course_id = fields.Many2one(
        'openacademy.course', 
        ondelete="cascade", 
        string="Course", 
        required=True)

    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    taken_seats = fields.Float(compute="_taken_seats", store=True);
    active = fields.Boolean(default=True)


    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for record in self:
            if not record.seats:
                record.taken_seats = 0
            else:
                record.taken_seats = 100.0 * len(record.attendee_ids) / record.seats


    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for record in self.filtered('start_date'):
            record.end_date = record.start_date + timedelta(days=record.duration, seconds=-1)


    @api.depends('start_date', 'duration')
    def _set_end_date(self):
        for record in self.filtered('start_date'):
            record.duration = (record.end_date - record.start_date).days + 1