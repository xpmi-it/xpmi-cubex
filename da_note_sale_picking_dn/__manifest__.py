# Copyright (C) 2024-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "DA - Note in Sale Picking DN",
    "version": "18.0.1.0.1",
    "category": "DA Tools/Stock",
    "summary": "Portare le note da ordine di vendita in picking, DdT, fattura",
    "author": "Dinamiche Aziendali srl",
    "website": "https://www.dinamicheaziendali.it/",
    "license": "AGPL-3",
    "depends": [
        "sale_stock",
        "stock",
        "l10n_it_delivery_note",
    ],
    "data": [
        "reports/report_deliveryslip_document.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
}
