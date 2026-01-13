# Copyright (C) 2025-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Andrea Barbato <abarbato@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import format_date
from collections import OrderedDict

class DueRegisterReport(models.AbstractModel):
    _name = "report.da_account_reports.date_due_report_a4"
    _description = "Due Date Report"

    def _get_report_values(self, docids, data=None):
        if not data:
            data = {}

        date_at = data.get("date_at")
        supplier_ids = data.get("suppliers", [])
        order = data.get("order")

        domain = [
            ("move_type", "in", ["in_invoice", "in_refund"]),
            ("parent_state", "=", "posted"),
            ("date_maturity", "<=", date_at),
            ("amount_residual", "!=", 0),
        ]

        if supplier_ids:
            domain.append(("partner_id", "in", supplier_ids))

        move_lines = self.env["account.move.line"].search(
            domain,
            order=f"date_maturity asc, {order}",
        )

        date_due = OrderedDict()

        for line in move_lines:
            date_maturity = line.date_maturity

            if date_maturity not in date_due:
                date_due[date_maturity] = {
                    "partner": line.partner_id,
                    "date_maturity": date_maturity,
                    "lines": [],
                    "net": 0.0,
                    "refund": 0.0,
                    "gross": 0.0,
                }

            date_due[date_maturity]["lines"].append(line)

            if line.move_type == "in_invoice":
                date_due[date_maturity]["gross"] += abs(line.amount_residual)
            elif line.move_type == "in_refund":
                date_due[date_maturity]["refund"] -= line.amount_residual

            date_due[date_maturity]["net"] = (
                    date_due[date_maturity]["gross"]
                    + date_due[date_maturity]["refund"]
            )

        return {
            "doc_ids": docids,
            "doc_model": "account.move",
            "docs": move_lines,
            "date_due": date_due,
            "date_at": date_at,
            "company": self.env.company,
        }
