{
    'name': 'crud task in website',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'This module defines for crud opration in website',
    'description': """
        This module defines for crud opration in website
    """,
    'author': 'Rutvik Patel',
    'depends': ['base', 'sale', 'website'],
    'data': [
        "security/ir.model.access.csv",
        "views/portal_lead_menu.xml",
        "views/lead_list.xml",
        "views/lead_form.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'crud_task_in_website/static/src/scss/lead_style.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
