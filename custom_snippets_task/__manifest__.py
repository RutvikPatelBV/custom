{
    'name': 'Custom Snippets Task',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'custom snippets task',
    'description': """
        This module defines a custom snippets
    """,
    'author': 'Rutvik Patel',
    'depends': ['base', 'sale', 'website'],
    'data': [
        "views/custom_snippet_one.xml",
        "views/custom_snippet_two.xml",
        "views/password_genarator_snippet.xml",
        "views/search_order_name_snippet.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            "custom_snippets_task/static/src/js/dynamic_table.js",
            "custom_snippets_task/static/src/js/password_genarator_snippet.js",
            "custom_snippets_task/static/src/js/search_order_name_snippet.js"
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
