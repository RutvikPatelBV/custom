{
    'name': 'Custom Web Page Task',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Module to create sale orders through a custom controller',
    'description': """
        This module defines a custom controller to handle form submissions and create sale orders.
    """,
    'author': 'Rutvik Patel',
    'depends': ['base', 'sale', 'website'],
    'data': [
        "security/ir.model.access.csv",
        "views/custom_page.xml",
        "views/custom_menu.xml"
    ],
    'assets': {
        'web.assets_frontend': [
            'custom_web_page_task/static/src/scss/custom_page.scss',
            'custom_web_page_task/static/src/js/custom_public_widget.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
