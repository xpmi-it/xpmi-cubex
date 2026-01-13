# Copyright (C) 2025-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import format_date


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    @api.model
    def _get_overdue_invoices_domain(self):
        return [
            ("partner_id", "child_of", self.id),
            ("move_type", "in", ["out_invoice", "out_refund"]),
            ("state", "=", "posted"),
            ("payment_state", "not in", ["paid", "in_payment"]),
            ("amount_residual", ">", 0),
        ]

    @api.model
    def _get_overdue_invoices(self):
        domain = self._get_overdue_invoices_domain()
        return self.env["account.move"].search(domain, order="invoice_date_due asc")

    def action_print_followup_letter(self):
        self.ensure_one()

        overdue_invoices = self._get_overdue_invoices()
        if not overdue_invoices:
            raise UserError(
                self.env._("No overdue invoices for partner %s.", self.display_name)
            )

        tz_date_str = format_date(
            self.env,
            fields.Date.today(),
            lang_code=self.lang or self.env.user.lang,
        )
        tz_date_str = tz_date_str.replace(".", "-")
        return (
            self.env.ref("da_overdue_invoice_report.action_overdue_invoice_report")
            .with_context(lang=self.lang or self.env.user.lang)
            .report_action(
                overdue_invoices.ids,
                data={"partner": self.id, "date_today": tz_date_str},
            )
        )
