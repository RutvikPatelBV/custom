{
    'name': 'Disable Add to Cart for Negative Forecast Quantity',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Disables Add to Cart button if forecasted quantity is less than zero',
    'description': """Restricts Add to Cart functionality when the forecasted quantity of the product is less than zero""",
    'author': 'Rutvik Patel',
    'depends': ['website_sale','website','stock','website_sale_wishlist'],
    'data': [
        # 'views/product_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'add_to_cart_restriction/static/src/js/forecast_restriction_product_details.js',
            'add_to_cart_restriction/static/src/js/whishlist.js',
        ],
    },
    'installable': True,
    'application': False,
}
