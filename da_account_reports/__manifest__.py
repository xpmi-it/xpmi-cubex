# Copyright (C) 2023-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Andrea Barbato (abarbato@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    "name": "DA - Reportistica Contabile",
    "version": "18.0.1.0.0",
    "category": "DA Tools/Accounting",
    "summary": "Reportistica per Contabilità",
    "author": "Dinamiche Aziendali srl",
    "website": "https://www.dinamicheaziendali.it/",
    "license": "GPL-3",
    "depends": [
        "base",
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "report/due_register_print_wizard.xml",
        "report/report_paperformat.xml",
        "report/due_register_report.xml",
        "report/date_due_report.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
}
