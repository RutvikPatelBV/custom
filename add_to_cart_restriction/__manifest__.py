{
    'name': 'Disable Add to Cart for Negative Forecast Quantity',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Disables Add to Cart button if forecasted quantity is less than zero',
    'description': """Restricts Add to Cart functionality when the forecasted quantity of the product is less than zero""",
    'author': 'Rutvik Patel',
    'depends': ['website', 'sale', 'website_payment', 'website_mail', 'portal_rating', 'digest', 'delivery'],
    'data': [
    ],
    'assets': {
        'web.assets_frontend': [
        ],
    },
    'installable': True,
    'application': False,
}
