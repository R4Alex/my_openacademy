# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OpenAcademySession(models.Model):
    _name = 'openacademy.session'
    _description = '''Openacademy Session'''

    name = fields.Char(required=True)
    description = fields.Text()

    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6,2), default=1.0, help="Duration in Days")
    seats = fields.Integer(string="Number of Seats", default=3)

    instructor_id = fields.Many2one('res.partner')

    course_id = fields.Many2one('openacademy.course', required=True, ondelete="cascade")

    attendee_ids = fields.Many2many('res.partner')

    taken_seats = fields.Integer(compute="_compute_taken_seats")

    @api.depends('attendee_ids', 'seats')
    def _compute_taken_seats(self):
        for record in self:
            if record.seats:
                record.taken_seats = 100 * len(record.attendee_ids) / record.seats
            else:
                record.taken_seats = 0
