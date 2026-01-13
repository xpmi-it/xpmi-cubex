# Copyright (C) 2023-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso (gborruso@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    "name": "DA - Utility per importare i listini",
    "version": "18.0.1.0.0",
    "category": "DA Tools/Import",
    "summary": "Permette di importare i listini",
    "author": "Dinamiche Aziendali srl",
    "license": "AGPL-3",
    "website": "https://www.dinamicheaziendali.it/",
    "depends": [
        "sale",
        "da_import",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/da_tools_listino.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
}
