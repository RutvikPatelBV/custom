from odoo import http
from odoo.http import request

class CustomSnippets(http.Controller):

    @http.route('/get_table_data', type='json', auth='public', website=True)
    def get_table_data(self):
        data = [
            {'column1': 'Row 1 Column 1', 'column2': 'Row 1 Column 2', 'column3': 'Row 1 Column 3'},
            {'column1': 'Row 2 Column 1', 'column2': 'Row 2 Column 2', 'column3': 'Row 2 Column 3'},
            # Add more rows as needed
        ]
        return data

class SaleOrderSearch(http.Controller):

    @http.route('/sale_order_search', type='json', auth='public', methods=['POST'])
    def search_sale_order(self, search_query):
        SaleOrder = request.env['sale.order']
        sale_orders = SaleOrder.search([('name', 'ilike', search_query)])
        results = []
        for order in sale_orders:
            results.append({
                'name': order.name,
                'products': ', '.join(order.order_line.mapped('product_id.name')),
                'amount_total': order.amount_total,
                'tax': order.amount_tax,
                'portal_url': order.get_portal_url(),
            })
        return results
