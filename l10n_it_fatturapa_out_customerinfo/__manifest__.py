# Copyright (C) 2023-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Italy - E-invoicing - Codice prodotto cliente",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Codice prodotto cliente in fattura elettronica",
    "author": "Dinamiche Aziendali srl",
    "website": "https://www.dinamicheaziendali.it/",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_edi",
        "product_customerinfo_invoice",
    ],
    "data": [
        "data/invoice_it_template.xml",
    ],
    "installable": True,
    "auto_install": True,
}
