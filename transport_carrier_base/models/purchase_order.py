# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models, _


class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"


    def button_confirm(self):
        res = super(PurchaseOrderInherit, self).button_confirm()
        for purchase in self:
            picking_ids = purchase.picking_ids.filtered(lambda pick: pick.state in ('draft', 'waiting', 'confirmed', 'assigned'))
            if picking_ids:
                picking_id = picking_ids[0]
                if picking_id.picking_type_id.dropshipping:
                    pick_vals = {'carrier_cost': picking_id.carrier_cost,
                                 'carrier_base_cost': picking_id.carrier_base_cost,
                                 }
                    if picking_id.sale_id.carrier_id:
                        pick_vals.update({'carrier_id': picking_id.sale_id.carrier_id.id})
                    if picking_id.sale_id.transport_carrier_id:
                        pick_vals.update({'transport_carrier_id': picking_id.sale_id.transport_carrier_id.id,
                                          'amount_cash_on_delivery': picking_id.sale_id.return_amount_cod()})
                        picking_id.write(pick_vals)
        return res
