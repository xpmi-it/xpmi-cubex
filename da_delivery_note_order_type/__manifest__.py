# Copyright (C) 2018-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    "name": "DA - Sale Order Type - DDT",
    "version": "18.0.1.0.0",
    "category": "DA Tools/Sales",
    "summary": "DDT in tipo ordine di vendita",
    "author": "Dinamiche Aziendali srl",
    "website": "https://www.dinamicheaziendali.it/",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "sale_order_type",
        "l10n_it_delivery_note",
    ],
    "data": [
        "views/sale_order_type_view.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
}
