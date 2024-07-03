from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DuplicateSaleOrder(models.Model):
    _name = 'practice.duplicate.sale.order'
    _description = 'Duplicate sale order model'
    name = fields.Char(string="Name", required=True)
