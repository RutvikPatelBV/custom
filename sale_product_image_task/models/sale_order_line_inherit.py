from odoo import models, fields, api, _

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    product_image = fields.Binary(string="Product Image", related='product_id.image_1920', depends=['product_id'])

    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLineInherit, self)._prepare_procurement_values(group_id)
        values.update({
            'product_image': self.product_image,
        })
        return values

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLineInherit, self)._prepare_invoice_line(**optional_values)
        res.update({
            'product_image': self.product_image
        })
        return res

class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        fields = super(StockRule, self)._get_custom_move_fields()
        fields += ['product_image']
        return fields

class StockMoveInherit(models.Model):
    _inherit = 'stock.move'

    product_image = fields.Binary(string="Product Image")

class AccountMoveInherit(models.Model):
    _inherit = 'account.move.line'

    product_image = fields.Binary(string="Product Image")
