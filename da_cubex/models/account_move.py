# Copyright (C) 2023-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.tools import float_compare
from odoo.tools.misc import format_amount


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    #todo test
    def summary_invoices_paid(self):
        invoices = self.env["account.move"].search([
            ("state", "=", "posted"),
            ("move_type", "in", self.get_invoice_types(include_receipts=True)),
            ("payment_state", "in", ["paid", "partial"]),
        ])
        summary_invoices = self.env["account.move"]
        for invoice in invoices:
            if float_compare(
                invoice.amount_total,
                invoice.amount_residual,
                precision_digits=invoice.currency_id.decimal_places
            ) != 0:
                reconciled_payments = invoice._get_reconciled_payments()
                if max(reconciled_payments.mapped("date")) >= fields.Date.today():
                    summary_invoices |= invoice
        if summary_invoices:
            body_template = _("""
                <div style="margin: 0px; padding: 0px;">
                    <p style="margin: 0px; padding: 0px; font-size: 13px;">
                        Dear,
                        <br /><br />
                        Here is summary invoices paid today
                        <br /><br />
                        <table class="table">
                            <thead>
                                <th>Number</th>
                                <th>Total</th>
                                <th>Total Paid</th>
                                <th>Amount Due</th>
                            </thead>
                            <tbody>
                                {invoice_info}
                            </tbody>
                        </table>
                    </p>
                </div>
            """)
            invoice_info = "".join(
                f"""
                    <tr>
                        <td>{invoice.name}</td>
                        <td>{format_amount(self.env, invoice.amount_total, invoice.currency_id)}</td>
                        <td>{format_amount(self.env, invoice.amount_total - invoice.amount_residual, invoice.currency_id)}</td>
                        <td>{format_amount(self.env, invoice.amount_residual, invoice.currency_id)}</td>
                    </tr>
                """
                for invoice in summary_invoices
            )
            body = body_template.format(invoice_info=invoice_info)
            self.env["mail.mail"].sudo().create({
                "body_html": body,
                "subject": _("Summary Invoices Paid"),
                "email_to": "a.cutarelli@cubexprofessional.it",
                "auto_delete": False,
            }).send()
