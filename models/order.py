from odoo import api, fields, models


class Order(models.Model):
    _name = 'game.order'
    _description = 'New Description'

    kode_order = fields.Char(string='Kode Order')

    
