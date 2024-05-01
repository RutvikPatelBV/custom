from odoo import models,fields,api


class Shipment(models.Model):
    _name='inventory.shipment'
    _description='Shipment Detiels'
    shipment_date=fields.Date(string='Shipment Date',required=True,default=lambda self:fields.Datetime.now())
    shipment_status=fields.Selection([('panding','Panding'),('on_the_way','On The Way'),('completed','Completed')],string='Shipment Status')
