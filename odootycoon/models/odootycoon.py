# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning
from random import randint


class OdooTycoon(models.Model):
    _name = "odootycoon.gamemanager"
    _description = '''  '''

    name = fields.Char("Game Name", default="New Game")
    day = fields.Integer("Current Day", default=1)
    cash = fields.Float("Cash", default=5000)

    def nextday(self):
        '''
        for game in self:
            game.day = game.day + 1
            game.cash = game.cash - 100
        
        This code has a problem, it makes some queries to the database
        So when we work with a lot of records odoo does a lot of queries 
        that takes processor power, in a few records is ok.
        
        Otherwise we can use the method write. With this method odoo just
        does one update query, so is more efficient'''
        #self.write({'day': self.day + 1, 'cash': self.cash - 100})

        # Process Unlocked Products
        products = self.env['product.template'].search([('unlocked', '=', True)])
        cash = 0

        for product in products:
            numsold = randint(5, 25)
            cash += product.list_price * numsold
        
        self.write({'day': self.day + 1, 'cash': self.cash + cash})


    def skip5days(self):
        for i in range(5):
            self.nextday()
            
    def skip30days(self):
        for i in range(30):
            self.nextday()

    def reset(self):
        self.write({'day': 1, 'cash': 5000})
        self.env['product.template'].search([('unlocked','=',True)]).write({'unlocked':False})