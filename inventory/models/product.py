from odoo import models,fields,api


class Product(models.Model):
    _name = 'inventory.product'
    _description = 'product details'
    _rec_name = 'product_name'

    product_name=fields.Char(string="Product Name",required=True)
    product_description=fields.Char(string="Description")
    product_price=fields.Integer(string="Price")
    product_quantity=fields.Integer(string="Quantity")
    product_category=fields.Selection([('digital','Digital'),('notdigital','Not Digital'),('other','Other')],string="Category")