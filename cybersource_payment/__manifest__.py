{
    'name': 'Cybersource payment',
    'version': '1.0',
    'summary': 'Custom module for integrating a custom payment gateway',
    'description': """
        This module provides integration with a custom payment gateway,
        allowing users to manage payments using the custom provider.
    """,
    'category': 'Accounting/Payment Providers',
    'author': 'Rutvik Patel',
    'license': 'LGPL-3',
    'depends': ['base', 'payment','sale'],
    'data': [
        'views/sale_order_button_view.xml',
        'views/cybersource_payment.xml',
        'data/payment_provider_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'installable': True,
    'application': False,
}
