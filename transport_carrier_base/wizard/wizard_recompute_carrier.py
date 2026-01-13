# -*- coding: utf-8 -*-
# Copyright (C) 2019-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from datetime import datetime
from odoo import api, models, fields


class SaleOrderRecomputeCarrier(models.TransientModel):
    _name = 'sale.order.recompute.carrier'
    _description = 'Recompute Carrier on Sale Order'

    def recompute_carrier(self):
        self.ensure_one()
        model_sale = self.env['sale.order']
        sale_list = self._context['active_ids']
        sale_ids = []
        for sale in sale_list:
            sale_ids.append(model_sale.browse(sale))
        for sale_order in sale_ids:
            sale_order.recompute_carrier_sale()
