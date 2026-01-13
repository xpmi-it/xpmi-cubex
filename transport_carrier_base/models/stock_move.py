# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models


class StockMoveInh(models.Model):
    _inherit = 'stock.move'

    def _get_new_picking_values(self):
        vals = super(StockMoveInh, self)._get_new_picking_values()
        if self.sale_line_id.order_id.transport_carrier_id:
            vals['transport_carrier_id'] = self.sale_line_id.order_id.transport_carrier_id.id
            vals['amount_cash_on_delivery'] = self.sale_line_id.order_id.return_amount_cod()
        return vals
