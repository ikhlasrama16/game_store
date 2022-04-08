from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Order(models.Model):
    _name = 'game.order'
    _description = 'New Description'

    orderplaystation_ids = fields.One2many(comodel_name='game.orderplaystationdetail', inverse_name='orderp_id', string='Playstation')
    ordercontroller_ids = fields.One2many(comodel_name='game.ordercontrollerdetail', inverse_name='orderc_id', string='Controller')
    ordergame_ids = fields.One2many(comodel_name='game.ordergamedetail', inverse_name='orderg_id', string='Game')

    name = fields.Char(string='Kode Order', required=True)
    tanggal_pesan = fields.Datetime('Tanggal Pemesanan',default=fields.Datetime.now())
    pemesan = fields.Many2one(
        comodel_name='res.partner', 
        string='Pemesan', 
        domain=[('is_customernya','=', True)],store=True)

    total = fields.Integer(compute='_compute_total', string='Total')
    
    @api.depends('orderplaystation_ids')
    def _compute_total(self):
        for record in self:
            a = sum(self.env['game.orderplaystationdetail'].search([('orderp_id', '=', record.id)]).mapped('price'))
            b = sum(self.env['game.ordercontrollerdetail'].search([('orderc_id', '=', record.id)]).mapped('price'))
            c = sum(self.env['game.ordergamedetail'].search([('orderg_id', '=', record.id)]).mapped('price'))
            record.total = a + b +c

    sudah_dibayar = fields.Boolean(string='Sudah dibayar', default=False)

    def invoice(self):
        invoices = self.env['account.move'].create({
            'move_type': 'out_invoice',  
            'partner_id': self.pemesan,
            'invoice_date': self.tanggal_pesan,
            'date': fields.Datetime.now(),
            'invoice_line_ids': [(0, 0, {
                'product_id': 0,
                'name' :'xxx' ,
                'quantity': 1,
                'name': 'product test 1',
                'discount': 0,
                'price_unit': self.total,
                'price_subtotal': self.total,
            })]            
        })
        self.sudah_dibayar=True
        return invoices
        
class OrderPlaystationDetail(models.Model):
    _name = 'game.orderplaystationdetail'
    _description = 'New Description'

    orderp_id = fields.Many2one(comodel_name='game.order', string='Order')
    playstation_id = fields.Many2one(comodel_name='game.playstation', string='Playstation')
    

    name = fields.Char(string='Name')
    qty = fields.Integer(string='Quantity')
    unit_price = fields.Integer(compute='_compute_unit_price', string='Harga Satuan')
    @api.depends('playstation_id')
    def _compute_unit_price(self):
        for record in self:
            record.unit_price = record.playstation_id.price

    price = fields.Integer(compute='_compute_price', string='Harga')

    @api.depends('qty','unit_price')
    def _compute_price(self):
        for record in self:
            record.price = record.unit_price * record.qty

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
            

    
    
class OrderControllerDetail(models.Model):
    _name = 'game.ordercontrollerdetail'
    _description = 'New Description'

    orderc_id = fields.Many2one(comodel_name='game.order', string='Order Controller')
    controller_id = fields.Many2one(comodel_name='game.controller', string='controller')


        
    name = fields.Char(string='Name')
    qty = fields.Integer(string='Quantity')

    unit_price = fields.Integer(compute='_compute_unit_price', string='Harga Satuan')
    @api.depends('controller_id')
    def _compute_unit_price(self):
        for record in self:
            record.unit_price = record.controller_id.price

    price = fields.Integer(compute='_compute_price', string='Harga')
    @api.depends('qty','unit_price')
    def _compute_price(self):
        for record in self:
            record.price = record.unit_price * record.qty
        
    @api.onchange('qty')
    def onchange_qty(self):
        for record in self:
            if record.qty > record.controller_id.stock:
                raise ValidationError("Stok tidak cukup")
    
    @api.model
    def create(self,vals):
        record = super(OrderControllerDetail, self).create(vals) 
        if record.qty:
             self.env['game.controller'].search([('id','=',record.controller_id.id)]).write({'stock':record.controller_id.stock-record.qty})
             return record



class OrderGameDetail(models.Model):
    _name = 'game.ordergamedetail'
    _description = 'New Description'

    orderg_id = fields.Many2one(comodel_name='game.order', string='Game')
    game_id = fields.Many2one(comodel_name='game.game', string='Game')

    name = fields.Char(string='Name')
    qty = fields.Integer(string='Quantity')

    unit_price = fields.Integer(compute='_compute_unit_price', string='unit_price')
    
    @api.depends('game_id')
    def _compute_unit_price(self):
        for record in self:
            record.unit_price = record.game_id.price

    price = fields.Integer(compute='_compute_price', string='price')
    
    @api.depends('qty', 'unit_price')
    def _compute_price(self):
        for record in self:
            record.price = record.game_id.price * record.qty

    @api.onchange('qty')
    def onchange_qty(self):
        for record in self:
            if record.qty > record.game_id.stock:
                raise ValidationError("Stok tidak cukup")
    
    @api.model
    def create(self,vals):
        record = super(OrderGameDetail, self).create(vals) 
        if record.qty:
             self.env['game.game'].search([('id','=',record.game_id.id)]).write({'stock':record.game_id.stock-record.qty})
             return record

    
