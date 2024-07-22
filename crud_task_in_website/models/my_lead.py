from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CrudLead(models.Model):
    _name = 'crud.lead'
    _description = 'crud lead'

    name = fields.Char(string="Name", required=True)
    phone=fields.Char(string="Phone No")
    email=fields.Char(string="email")
