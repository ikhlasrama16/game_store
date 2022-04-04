from odoo import api, fields, models


class Game(models.Model):
    _name = 'game.game'
    _description = 'New Description'

    name = fields.Char(string='Name')
    tipe = fields.Selection(string='Type', selection=[('PS1', 'PS1'), ('PS2', 'PS2'),])
    description = fields.Char(string='Deskripsi')
    stock = fields.Char(string='Stok')
    price = fields.Char(string='Harga')
    
    
    
    
