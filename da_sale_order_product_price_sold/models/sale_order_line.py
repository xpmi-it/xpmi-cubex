# Copyright (C) 2024-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models


class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    def show_product_sold(self):
        self.ensure_one()

        action = {
            "name": self.env._("Sales Order(s)"),
            "type": "ir.actions.act_window",
            "res_model": "sale.order.line",
            "target": "current",
            "view_mode": "list,form",
        }
        if self.product_id:
            action["domain"] = [
                ("product_id", "=", self.product_id.id),
                ("order_partner_id", "=", self.order_partner_id.id),
                ("state", "in", ["sale", "done"]),
                ("order_id", "!=", self.order_id.id),
            ]
        else:
            action["domain"] = []
        return action
