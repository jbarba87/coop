# -*- coding: utf-8 -*-
{
    'name': "coopecan",

    'summary': """
        Modulo de coopecan""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Coopecan",
    'website': "http://www.coopecan.pe",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'board', 'mail', 'hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
        'views/view_socio.xml',
        'views/view_cabana.xml',
        'views/view_asociacion.xml',
        'views/view_parcela.xml',
        'views/view_potrero.xml',
        'views/view_camelido_andino.xml',
        'views/view_historial.xml',
        'views/view_tablero.xml',
        'views/view_emp.xml',
        'views/templates_prueba.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
 #       'demo/demo.xml',
    ],
    'application': True,
}
