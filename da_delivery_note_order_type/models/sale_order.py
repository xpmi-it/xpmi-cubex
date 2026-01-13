# Copyright (C) 2018-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models
from odoo.exceptions import UserError


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        if not all(
            order.type_id.warehouse_id.id == order.warehouse_id.id for order in self
        ):
            msg = self.env._("Warehouse must be same as order type.")
            raise UserError(msg)
        return super().action_confirm()
