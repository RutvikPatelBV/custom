from odoo import models, fields, api, _

class PosConfigLocation(models.Model):
    _name = 'practice.pos.config.location'
    _description = 'practice pos config location'

    name=fields.Char(string="name")