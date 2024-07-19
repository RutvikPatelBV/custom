{
    'name': 'custom web sale order search popup',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'This module defines for popup functionality for search sale_order',
    'description': """
        This module defines for popup functionality for search sale_order
    """,
    'author': 'Rutvik Patel',
    'depends': ['base', 'sale', 'website'],
    'data': [
        "views/search_popup_button_view.xml",
        # "views/search_popup_view.xml"
    ],
    'assets': {
        'web.assets_frontend': [
            'custom_web_sale_order_search_popup/static/src/js/search_model.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
