from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Order(models.Model):
    _name = 'game.order'
    _description = 'New Description'

    orderplaystation_ids = fields.One2many(comodel_name='game.orderplaystationdetail', inverse_name='orderp_id', string='Playstation')

    kode_order = fields.Char(string='Kode Order', required=True)
    tanggal_pesan = fields.Datetime('Tanggal Pemesanan',default=fields.Datetime.now())
    pemesan = fields.Many2one(
        comodel_name='res.partner', 
        string='Pemesan', 
        domain=[('is_customernya','=', True)],store=True)




class OrderPlaystationDetail(models.Model):
    _name = 'game.orderplaystationdetail'
    _description = 'New Description'

    orderp_id = fields.Many2one(comodel_name='game.order', string='Order')
    playstation_id = fields.Many2one(comodel_name='game.playstation', string='Playstation')
    

    name = fields.Char(string='Name')
    qty = fields.Integer(string='Quantity')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan', string='Harga Satuan')
    @api.depends('playstation_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.playstation_id.price

    harga = fields.Char(compute='_compute_harga', string='Harga')

    @api.depends('qty','harga_satuan')
    def _compute_harga(self):
        for record in self:
            record.harga = record.harga_satuan * record.qty

    @api.onchange('qty')
    def onchange_qty(self):
        for record in self:
            if record.qty > record.playstation_id.stock:
                raise ValidationError("Stok tidak cukup")
    
    @api.model
    def create(self,vals):
        record = super(OrderPlaystationDetail, self).create(vals) 
        if record.qty:
            self.env['game.playstation'].search([('id','=',record.playstation_id.id)]).write({'stock':record.playstation_id.stock-record.qty})
            return record



    
