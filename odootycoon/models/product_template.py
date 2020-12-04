
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _description = '''  '''
    
    unlockcost = fields.Float('Unlock Cost', default=750)
    unlocked = fields.Boolean('Unlocked', default=False)

    def unlockproduct(self):
        gamemanager = self.env['odootycoon.gamemanager'].search([('id', '=', 1)])
        if gamemanager.cash >= self.unlockcost:
            self.unlocked = True
            gamemanager.cash -= self.unlockcost
        else:
            raise Warning('You do not have engough money to by the {}'.format(self.name))
