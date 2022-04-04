from odoo import api, fields, models


class Controller(models.Model):
    _name = 'game.controller'
    _description = 'New Description'

    name = fields.Char(string='Nama')
    color = fields.Char(string='Warna')
    description = fields.Char(string='Deskripsi')
    stock = fields.Integer(string='Stok')
    price = fields.Char(string='Harga')