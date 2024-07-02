from odoo import fields, models, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    new_note = fields.Char(string='New Note')
    discounted_order = fields.Boolean(string='Is Discounted Order',readonly=True)

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['new_note'] = ui_order.get('new_note')
        order_fields['discounted_order'] = ui_order.get('discounted_order')
        return order_fields

