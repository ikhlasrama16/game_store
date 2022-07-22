from odoo import api, fields, models


class nintendo(models.Model):
    _name = 'game.nintendo'
    _description = 'New Description'

    name = fields.Char(string='Nama')
    description = fields.Char(string='Deskripsi')
    controller = fields.Boolean(string='With Controller')
    stock = fields.Integer(string='Stok')
    price = fields.Char(string='Harga')
