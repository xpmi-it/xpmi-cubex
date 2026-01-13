# Copyright (C) 2024-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockPickingInherit(models.Model):
    _inherit = "stock.delivery.note"

    def action_invoice(self, invoice_method=False):
        res = super().action_invoice(invoice_method)
        for delivery_note in self:
            invoice_ids = delivery_note.mapped("invoice_ids")
            for invoice in invoice_ids:
                invoice.narration = delivery_note.note
        return res
