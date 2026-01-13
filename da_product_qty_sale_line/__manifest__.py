# Copyright (C) 2024-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    "name": "DA - Show qty available of product in sale order line",
    "version": "18.0.1.0.1",
    "category": "DA Tools/Stock",
    "summary": "Mostrare quantità disponibile prodotto su ordine",
    "author": "Dinamiche Aziendali srl",
    "website": "https://www.dinamicheaziendali.it/",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "product",
    ],
    "data": [
        "views/sale_order.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
}
