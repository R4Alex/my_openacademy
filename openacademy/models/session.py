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
    instructor_id = fields.Many2one('res.partner', domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', 'Teacher')])

    course_id = fields.Many2one(
        'openacademy.course', 
        ondelete="cascade", 
        string="Course", 
        required=True,
    )

    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    taken_seats = fields.Float(compute="_taken_seats", store=True);

    # to make a kanbam view 
    color = fields.Float()

    # To use in graph
    attendees_count = fields.Integer(compute="_get_attendees_count", store=True)

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

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for record in self:
            record.attendees_count = len(record.attendee_ids)


    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        for record in self:
            if record.seats < 0:
                record.active = False
                return {
                    'warning': {
                        'title': "Incorrect 'seats' value",
                        'message': "The number of availible seats may not be negative",
                    }
                }

            if record.seats < len(record.attendee_ids):
                record.active = True
                return {
                    'warning': {
                        'title': "To many attendees",
                        'message': "Increse seats or remove excess attendees",
                    }
                }

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for record in self.filtered('instructor_id'):
            if record.instructor_id in record.attendee_ids:
                raise exceptions.ValidationError(
                        "A session's instructor can't be an attendee")
