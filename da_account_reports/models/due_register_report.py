# Copyright (C) 2025-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Andrea Barbato <abarbato@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import format_date
from collections import OrderedDict

class DueRegisterReport(models.AbstractModel):
    _name = "report.da_account_reports.due_register_report_a4"
    _description = "Due Register Report"

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
            order=f"partner_id, date_maturity, {order}",
        )

        suppliers = OrderedDict()

        for line in move_lines:
            partner = line.partner_id

            if partner.id not in suppliers:
                suppliers[partner.id] = {
                    "partner": partner,
                    "lines": [],
                    "net": 0.0,
                    "refund": 0.0,
                    "gross": 0.0,
                }

            suppliers[partner.id]["lines"].append(line)

            if line.move_type == "in_invoice":
                suppliers[partner.id]["gross"] += abs(line.amount_residual)
            elif line.move_type == "in_refund":
                suppliers[partner.id]["refund"] -= line.amount_residual

            suppliers[partner.id]["net"] = (
                    suppliers[partner.id]["gross"]
                    + suppliers[partner.id]["refund"]
            )

        return {
            "doc_ids": docids,
            "doc_model": "account.move",
            "docs": move_lines,
            "suppliers": suppliers,
            "date_at": date_at,
            "company": self.env.company,
        }
