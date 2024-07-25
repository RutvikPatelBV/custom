from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class CustomWebsiteSale(WebsiteSale):

    @http.route('/shop/cart/update_json', type='json', auth="public", website=True)
    def cart_update_json(self, **post):
        product_id = int(post.get('product_id', 0))
        if product_id:
            product = request.env['product.product'].sudo().browse(product_id)
            if product.virtual_available < 0:
                return {
                        'line_id': False,
                        'quantity': 0,
                        'option_ids': [],
                        'notification_info': {
                            'currency_id': request.website.currency_id.id,
                            'lines': False,
                            'warning': 'Product forecast quantity is less than zero.',
                        },
                        'cart_quantity': request.website.sale_get_order().cart_quantity,
                        'minor_amount': [],
                        'amount': 0.0,
                    }


        return super(CustomWebsiteSale, self).cart_update_json(**post)

