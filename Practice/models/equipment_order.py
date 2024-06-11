from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EquipmentOrder(models.Model):
    _name = 'practice.equipment.order'
    _description = 'Equipment Order Model'

    seq = fields.Char(default=lambda self: _('New'), copy=False, readonly=True, required=True)
    name_of_equipment = fields.Many2one('practice.equipment')
    company_name = fields.Many2one('practice.company')
    qty = fields.Integer(string="Quantity")
    price_per_unit = fields.Integer(string="Price per unit", related="name_of_equipment.price_per_unit")
    grand_total = fields.Integer(string="Order Total", compute="_compute_total")
    order_status = fields.Selection([('initial', 'Initiated'), ('delivery', 'Confirm (Delivery)')],string="Order Status",default="initial")


    def create(self, vals):
        if vals.get('seq', _("New")) == _("New"):
            vals['seq'] = self.env['ir.sequence'].next_by_code('equipment.order.seq') or _("New")
        res = super(EquipmentOrder, self).create(vals)
        return res

    @api.depends('qty')
    def _compute_total(self):
        self.env['practice.equipment'].with_context(amount=True)
        for rec in self:
            if rec.qty:
                rec.grand_total = rec.qty * rec.price_per_unit

            else:
                rec.grand_total = 0

    @api.onchange('qty')
    def check_qty(self):
        for rec in self:
            if rec.qty > rec.name_of_equipment.qty:
                raise ValidationError(_(f"{rec.name_of_equipment.name} is Only {rec.name_of_equipment.qty} available"))

    def action_confirm(self):
        if self.order_status=="initial":
            vals = {
                'equipment_name': self.name_of_equipment.name,
                'name_company': self.company_name.name,
                'qty': self.qty,
                'price_per_unit': self.price_per_unit,
                'grand_total': self.grand_total,
            }
            print(vals)
            delivery_obj=self.env['practice.equipment.delivery']
            delivery_obj.create(vals)
            self.order_status="delivery"
        else:
            pass

