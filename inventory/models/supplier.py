from odoo import models,fields,api


class supplier(models.Model):
    _name='inventory.supplier'
    _description='Supplier Details'
    supplier_name=fields.Char(string='Supplier Name',required=True)
    supplier_contact=fields.Char(string='Supplier Contact')
    supplier_email=fields.Char(string='Supplier Email',required=True)
