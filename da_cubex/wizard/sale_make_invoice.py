# Copyright (C) 2018-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleAdvancePaymentInvInherit(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        self._check_amount_is_positive()
        invoices = self.env["account.move"]
        for partner_shipping_id in self.mapped("sale_order_ids.partner_shipping_id"):
            sale_orders = self.sale_order_ids.filtered(
                lambda s: s.partner_shipping_id.id == partner_shipping_id.id
            )
            invoices |= self._create_invoices(sale_orders)
        return self.sale_order_ids.action_view_invoice(invoices=invoices)
