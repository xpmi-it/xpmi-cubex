# Copyright (C) 2018-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Cubex - Customizations",
    "version": "18.0.1.0.1",
    "development_status": "Beta",
    "category": "Customizations/Cubex",
    "author": "Dinamiche Aziendali srl",
    "website": "https://www.dinamicheaziendali.it",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account",
        "sale",
        "l10n_it_delivery_note",
        "purchase_stock",
        "stock_picking_batch",
        "da_overdue_invoice_report",
    ],
    "data": [
        'data/ir_actions_server_data.xml',
        'data/ir_cron_data.xml',
        'reports/report_picking_batch.xml',
        'views/account_move_view.xml',
        # 'views/header_footer_view.xml', #TODO clean non esiste
        'views/purchase_report_template.xml',
        'views/report_delivery_note.xml',
        #'views/report_invoice.xml',
        'views/report_picking_batch_cubex.xml',
        'views/sale_order_view.xml',
        'views/sale_order_template_view.xml',
        'views/stock_move_line_view.xml',
    ],
    "installable": True,
}
