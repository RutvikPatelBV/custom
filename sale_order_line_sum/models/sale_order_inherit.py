from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    sum_of_order_line=fields.Float(string='Sum Of Order',compute = "_compute_sum_of_order_line")

    @api.depends('order_line')
    def _compute_sum_of_order_line(self):
        for res in self:
            service_lines = [line for line in
                             res.order_line.filtered(lambda x:  x.product_id.type == 'service')]
            total_sum = sum(line.product_uom_qty for line in service_lines)
            res.sum_of_order_line = total_sum
