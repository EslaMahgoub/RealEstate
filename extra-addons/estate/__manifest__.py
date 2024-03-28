{
    'name': "A Real estate app",
    'version': '1.0',
    'depends': ['base', 'website', 'website_mail', 'product', 'sale'],
    'author': "Eslam Mahgoub",
    'category': 'Quantum Odoo',
    'description': """
    A Real estate app
    """,
    'license': "LGPL-3",
    # data files always loaded at installation
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_views.xml',
        'views/controller_views.xml',
        'views/success.xml',
        'views/estate_menus.xml',
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