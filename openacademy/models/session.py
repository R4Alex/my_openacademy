# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OpenAcademySession(models.Model):
    _name = 'openacademy.session'
    _description = '''Open Academy Session'''

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6,2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one('res.partner', string='instructor')

    course_id = fields.Many2one(
        'openacademy.course', 
        ondelete="cascade", 
        string="Course", 
        required=True)

    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    taken_seats = fields.Float(compute="_taken_seats");
    active = fields.Boolean(default=True)

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for record in self:
            if not record.seats:
                record.taken_seats = 0
            else:
                record.taken_seats = 100.0 * len(record.attendee_ids) / record.seats
