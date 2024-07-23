from odoo import models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def get_forecasted_quantity(self, product_id):
        print(product_id)
        product = self.browse(int(product_id))
        product.ensure_one()
        return product.virtual_available
