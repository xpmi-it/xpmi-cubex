# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': "Report Bordero",
    'summary': "Report Bordero",
    'description': """Report Bordero""",
    'author': 'Dinamiche Aziendali srl',
    'license': 'OPL-1',
    'website': 'www.dinamicheaziendali.it',
    'category': 'DA Tools (Stock)',
    'version': '18.0.1.0.1',
    'depends': [
        'base',
        'stock',
        'delivery',
        'transport_carrier_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_view.xml',
        'views/transport_carrier_view.xml',
        'views/bordero_template_view.xml',
        'report/paper_format.xml',
        'report/bordero_layout.xml',
        'report/report_bordero.xml',
        'wizard/wizard_bordero.xml',
    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'active': False,
    'installable': True
}