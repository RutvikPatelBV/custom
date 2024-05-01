from odoo import models,fields,api


class order(models.Model):
    _name='inventory.order'
    _description='Orders Details'
    product=fields.Many2one('inventory.product',string='Product',required=True)
    order_date=fields.Date(string='Order Date',default=lambda self:fields.Datetime.now())
    order_quantity=fields.Integer(string='Order Quantity',required=True)


