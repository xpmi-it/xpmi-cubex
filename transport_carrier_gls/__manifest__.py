# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': "Transport Carrier Gls ",
    'summary': "",
    'description': """Transport Carrier Gls
    . Dinamiche Aziendali srl""",
    'author': 'Gianmarco Conte <gconte@dinamicheaziendali.it> ',
    'license': 'OPL-1',
    'website': 'www.dinamicheaziendali.it',
    'category': '',
    'version': '18.0.1.0.1',
    'depends': [
        'base',
        'stock',
        'transport_carrier_base',
        'account',
        'da_report_bordero_base',
    ],
    'data': [
        'security/da_gls_group.xml',
        'security/ir.model.access.csv',
        'data/transport_carrier_gls_data.xml',
        'views/account_incoterm_view.xml',
        'views/transport_carrier_view.xml',
        'views/transport_condition.xml',
        'views/stock_picking_view.xml',
        'views/report_label_template.xml',
        'views/report_bordero_gls_template.xml',
        'report/paperformat_view.xml',
        'report/report_label.xml',
    ],
    "external_dependencies": {
        "python": ["pdf2image", "bs4"],
    },
    'demo': [],
    'active': False,
    'installable': True
}
