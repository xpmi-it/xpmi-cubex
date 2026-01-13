# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': "Transport Carrier integration with Amazon Module",
    'summary': "",
    'description': """Transport Carrier integration with Amazon Module 
    Dinamiche Aziendali srl""",
    'author': 'Gianmarco Conte <gconte@dinamicheaziendali.it> ',
    'license': 'OPL-1',
    'website': 'www.dinamicheaziendali.it',
    'category': '',
    'version': '18.0.1.0.1',
    'depends': [
        'transport_carrier_base',
        'amazon_ept',
    ],
    'data': [
        'views/transport_carrier.xml',
    ],
    'demo': [],
    'active': False,
    'installable': True
}
