from odoo import fields, models, api


class warehouse(models.Model):
    _name = 'inventory.warehouse'
    _description = 'inventory warehouse details'
    warehouse_owner = fields.Char(string='Warehouse Owner Name', required=True)
    warehouse_location = fields.Char(string='Warehouse Location', required=True)
    warehouse_capacity = fields.Integer(string='Warehouse Capacity')
