# Copyright (C) 2024-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    "name": "DA - Shipping Address related to Customer in Sale Order",
    "version": "18.0.1.0.1",
    "category": "DA Tools/Sales",
    "summary": "Vedere solo indirizzi di spedizione legati al cliente dell'ordine",
    "author": "Dinamiche Aziendali srl",
    "website": "https://www.dinamicheaziendali.it/",
    "license": "AGPL-3",
    "depends": [
        "base",
        "sale",
    ],
    "data": [
        "views/sale_order_view.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
}
