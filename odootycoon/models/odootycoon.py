# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning
from random import randint


class OdooTycoon(models.Model):
    _name = "odootycoon.gamemanager"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = '''  '''
    

    name = fields.Char("Game Name", default="New Game")
    day = fields.Integer("Current Day", default=1)
    cash = fields.Float("Cash", default=5000)
    
    lines = fields.One2many('odootycoon.gamemanager.line', 'manager_id')

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
        regular_costs = self.get_regular_costs()
        purchase_costs = self.get_purchase_costs()

        for line in self.lines:
            numsold = randint(0, line.quantity)
            line.quantity -= numsold
            cash += line.product_id.list_price * numsold
        
        self.write({'day': self.day + 1, 'cash': self.cash + cash - regular_costs - purchase_costs})
        self.lines.write({"lets_buy": False})


    def skip5days(self):
        for i in range(5):
            self.nextday()
            
    def skip30days(self):
        for i in range(30):
            self.nextday()

    def reset(self):
        self.write({'day': 1, 'cash': 5000})
        self.env['product.template'].search([('unlocked','=',True)]).write({'unlocked':False})
        self.lines.unlink()

    def get_regular_costs(self):
        cost = 500
        for line in self.lines:
            cost += line.product_id.standard_price * randint(0, 5) * line.quantity
        return cost
    
    def get_purchase_costs(self):
        # for line in self.lines:
        #     if not line.lets_buy:
        #         continue
        cost = 0
        for line in self.lines.filtered(lambda l: l.lets_buy == True):
            new_quantities = randint(0, 5)
            line.quantity += new_quantities
            cost += line.product_id.standard_price * new_quantities
        return cost

    def refresh_products(self):
        product_obj = self.env['odootycoon.gamemanager.line']
        products = self.env['product.template'].search([('unlocked', '=', True)])
        
        manager_products = self.lines.mapped("product_id")

        for product_id in products:
            if product_id not in manager_products:
                product_obj.create({
                    'product_id': product_id.id,
                    'quantity': 5,
                    'manager_id': self.id
                })
        self.lines.write({"lets_buy": False})

class OdooTycoonLine(models.Model):
    _name = "odootycoon.gamemanager.line"
    _description = '''  '''

    name = fields.Char(related="product_id.name")
    manager_id = fields.Many2one("odootycoon.gamemanager")
    product_id = fields.Many2one('product.template', readonly=True, required=True)
    quantity = fields.Integer(readonly=True)
    lets_buy = fields.Boolean()
