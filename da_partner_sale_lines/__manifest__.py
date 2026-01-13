# Copyright (C) 2024-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    "name": "DA - Sale Order Lines from Partner",
    "version": "18.0.1.0.1",
    "category": "DA Tools/Sales",
    "summary": "Aggiungere smart button su contatto per vedere ordini di vendita",
    "author": "Dinamiche Aziendali srl",
    "website": "https://www.dinamicheaziendali.it/",
    "license": "AGPL-3",
    "depends": [
        "base",
        "sale",
    ],
    "data": [
        "views/res_partner_view.xml",
        "views/sale_order_line_view.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
}
