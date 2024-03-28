{
    'name': "A Real estate Report",
    'version': '1.0',
    'depends': ['estate'],
    'author': "Eslam Mahgoub",
    'category': 'Quantum Odoo',
    'description': """
    A Real estate app
    """,
    'license': "LGPL-3",
    # data files always loaded at installation
    'data': [
        'views/estate_property_report_views.xml',
        'security/ir.model.access.csv',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}