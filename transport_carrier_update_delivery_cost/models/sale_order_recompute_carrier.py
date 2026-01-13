# -*- coding: utf-8 -*-
# Copyright (C) 2022-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from datetime import datetime
from odoo import api, models, fields


class SaleOrderRecomputeCarrierInherit(models.TransientModel):
    _inherit = 'sale.order.recompute.carrier'
    _description = 'Recompute Carrier on Sale Order'

    def recompute_carrier(self):
        res = super(SaleOrderRecomputeCarrierInherit, self).recompute_carrier()
        model_sale = self.env['sale.order']
        sale_ids = model_sale.browse(self._context['active_ids'])
        for sale_order in sale_ids:
            sale_order.update_delivery_cost()
        return res
