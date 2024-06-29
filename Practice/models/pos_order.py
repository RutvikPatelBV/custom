from odoo import fields, models, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    new_note = fields.Char(string='New Note')

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['new_note'] = ui_order.get('new_note')
        return order_fields

