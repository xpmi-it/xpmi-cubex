# -*- coding: utf-8 -*-
# Copyright (C) 2022-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def update_delivery_cost(self):
        for order in self:
            if order.transport_carrier_id and order.carrier_cost:
                order.check_delivery_order_line()

    def check_delivery_order_line(self):
        for order in self:
            if order.order_line:
                delivery_line = order.order_line.filtered(lambda dl: dl.is_delivery)
                if delivery_line:
                    delivery_line[0].purchase_price = order.carrier_cost

    @api.onchange('carrier_id', 'partner_id', 'order_line')
    def recompute_transport_carrier_onchange(self):
        res = super(SaleOrderInherit, self).recompute_transport_carrier_onchange()
        if self:
            self.update_delivery_cost()
        return res