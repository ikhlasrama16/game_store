from odoo import api, fields, models


class playstation(models.Model):
    _name = 'game.playstation'
    _description = 'New Description'

    name = fields.Char(string='Nama')
    description = fields.Char(string='Deskripsi')
    controller = fields.Boolean(string='With Controller')
    stock = fields.Integer(string='Stok')
    price = fields.Char(string='Harga')
    
    
    
