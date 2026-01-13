# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': "Transport Carrier Base ",
    'summary': "",
    'description': """Transport Carrier Base
    . Dinamiche Aziendali srl""",
    'author': 'Gianmarco Conte <gconte@dinamicheaziendali.it> ',
    'license': 'OPL-1',
    'website': 'www.dinamicheaziendali.it',
    'category': '',
    'version': '18.0.1.0.1',
    'depends': [
        'base',
        'stock',
        'sale_stock',
        'delivery', #todo, serve ancora?
        'stock_delivery',
        'purchase',
        'da_payment_term_cod',
        'product_dimension',
    ],
    'data': [
        'data/transport_carrier_data.xml',
        'security/transport_carrier_base_group.xml',
        'security/ir.model.access.csv',
        'views/account_incoterm_view.xml',
        'views/transport_carrier.xml',
        'views/sale_order.xml',
        'views/stock_picking.xml',
        'views/stock_picking_type.xml',
        'views/product_product.xml',
        'views/product_template.xml',
        'views/transport_condition.xml',
        'views/res_partner_view.xml',
        'wizard/transport_carrier_action_wizard.xml',
        'wizard/print_label_wizard.xml',
        'wizard/wizard_recompute_carrier.xml',
    ],
    "external_dependencies": {
        "python": ["unidecode"],
    },
    'demo': [],
    'active': False,
    'installable': True,
}
