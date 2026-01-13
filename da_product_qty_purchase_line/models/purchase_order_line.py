# Copyright (C) 2024-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, fields, models


class PurchaseOrderLineInherit(models.Model):
    _inherit = "purchase.order.line"

    qty_available = fields.Float(
        compute="_compute_qty_available",
        string="Qty available",
    )

    @api.depends("product_id")
    def _compute_qty_available(self):
        for line in self:
            line.qty_available = line.product_id.with_company(
                line.company_id.id
            ).qty_available
