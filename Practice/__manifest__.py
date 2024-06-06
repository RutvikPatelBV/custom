{
    'name': 'Practice',
    'version': '1.1',
    'summary': 'For Practice',
    'sequence': 2,
    'description': 'For Practice Access Rights',
    'author': 'RP',
    'license': '',
    'depends': ['base', 'mail', 'web', 'hr_expense', 'purchase', 'website'],
    'data': ['security/ir.model.access.csv',
             'data/data.xml',
             'data/new_template.xml',
             "views/menu.xml",
             "views/practice_view.xml",
             "views/company_view.xml",
             "views/work_view.xml",
             "views/licenced_company_view.xml",
             "views/equipment_view.xml",
             "views/equipment_order_view.xml",
             "views/equipment_delivery_view.xml",
             "views/purchase_portal_sidebar_inherite.xml",
             "report/hr_expense_qweb_report.xml",
             ],
    'assets': {
        'web.assets_backend': [
            # 'Practice/static/src/**/*',
            'Practice/static/src/components/hr_expense_custom_button_action.js',
            'Practice/static/src/views/hr_expense_custom_button.xml',

        ],
        'web.assets_frontend': [
            'Practice/static/src/js/purchase_portal_sidebar_inheritance.js',
        ],
    },

    'demo': [''],
    'application': True,
    'installable': True,
}
