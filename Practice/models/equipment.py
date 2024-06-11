from odoo import models, fields, api, _

class Equipment(models.Model):
    _name = 'practice.equipment'
    _description = 'Equipment Model'

    seq = fields.Char(default=lambda self: _('New'), copy=False, readonly=True, required=True)
    name=fields.Char(string="name")
    qty=fields.Integer(string="Quantity")
    price_per_unit=fields.Integer(string="Price per unit")


    def create(self, vals):
        if vals.get('seq', _("New")) == _("New"):
            vals['seq'] = self.env['ir.sequence'].next_by_code('equipment.seq') or _("New")
        res = super(Equipment, self).create(vals)
        print(self.env.context.get('amount'))
        return res

    # def check(self):
    #     products = self.env['product.product'].search_read([('list_price', '>', 100)], ['name', 'list_price'])
    #     print(len(products))