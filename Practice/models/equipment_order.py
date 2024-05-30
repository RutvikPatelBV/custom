from odoo import models, fields, api, _

class EquipmentOrder(models.Model):
    _name = 'practice.equipment.order'
    _description = 'Equipment Order Model'

    seq = fields.Char(default=lambda self: _('New'), copy=False, readonly=True, required=True)
    name=fields.Char(string="name")
    qty=fields.Integer(string="Quantity")
    price_per_unit=fields.Integer(string="Price per unit")
