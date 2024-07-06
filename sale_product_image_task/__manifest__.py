{
    'name': 'Sale Product Image Task',
    'version': '1.0',
    'summary': 'Custom module for managing product images in sale orders.',
    'description': """
        This module adds functionality to manage product images within sale orders.
        It enhances the default sale order functionalities to display product images.
    """,
    'category': 'Sales',
    'author': 'Rutvik Patel',
    'website': '',
    'license': '',
    'depends': ['sale'],
    'data': ["views/sale_order_line_inherit_view.xml"],
    'installable': True,
}
