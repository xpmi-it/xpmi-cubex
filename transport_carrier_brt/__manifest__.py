# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': "Transport Carrier BRT",
    'summary': "",
    'description': """Transport Carrier BRT
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
        'data/transport_carrier_brt_data.xml',
        'data/automated_action.xml',
        'report/paper_format.xml',
        'views/transport_carrier_view.xml',
        'views/stock_picking_view.xml',
        'views/transport_condition.xml',
        'views/bordero_template_view.xml',
        'views/report_label_template.xml',
        'views/stock_warehouse_view.xml',
        'views/res_partner_view.xml',
        'report/report_label.xml',
    ],
    "external_dependencies": {
        "python": ["pdf2image"],
    },
    'demo': [],
    'active': False,
    'installable': True
#TODO da testare azioni automatiche (es: Update tracking);
#TODO test: validazione sped, get tracking;
}
