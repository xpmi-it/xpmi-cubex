# Copyright (C) 2025-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class OverdueInvoiceReport(models.AbstractModel):
    _name = "report.da_overdue_invoice_report.overdue_inv_report_template"
    _description = "Overdue Invoice Report"

    def _get_report_values(self, docids, data=None):
        return {
            "doc_ids": docids,
            "doc_model": "account.move",
            "docs": self.env["account.move"].browse(docids),
            "invoices": self.env["account.move"].browse(
                data.get("context", {}).get("active_ids")
            ),
            "partner": self.env["res.partner"].browse(data.get("partner")),
            "date_today": data.get("date_today"),
            "date_due": fields.Date.today(),
            "data": data,
        }
