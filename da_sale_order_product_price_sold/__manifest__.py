# Copyright (C) 2024-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    "name": "DA - Show product previous sale order line from sale order",
    "version": "18.0.1.0.1",
    "category": "DA Tools/Sales",
    "summary": "Mostrare precedente ordine di vendita del prodotto",
    "author": "Dinamiche Aziendali srl",
    "website": "https://www.dinamicheaziendali.it/",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "sale_stock",
    ],
    "data": [
        "views/sale_order.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
}
