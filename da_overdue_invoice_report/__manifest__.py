# Copyright (C) 2025-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "DA - Overdue Invoice Report",
    "version": "18.0.1.0.0",
    "category": "DA Tools/Stock",
    "summary": "Consentire di stampare fatture scadute in base al contatto selezionato",
    "author": "Dinamiche Aziendali srl",
    "website": "https://www.dinamicheaziendali.it/",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account_followup",
    ],
    "data": [
        "reports/report_overdue_invoice.xml",
        "views/res_company_view.xml",
        "views/res_partner_view.xml",
        "views/report_overdue_invoice_template.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
}
