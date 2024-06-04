from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EquipmentDelivery(models.Model):
    _name = 'practice.equipment.delivery'
    _description = 'Equipment Order Delivery Model'

    equipment_name = fields.Char(string='Name Of Equipment')
    name_company=fields.Char(string='Company Name')
    qty=fields.Integer(string="Quantity")
    price_per_unit=fields.Integer(string="Price per unit")
    grand_total=fields.Integer(string="Order Total")
