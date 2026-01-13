# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, models

class TransportCarrierWizard(models.TransientModel):
    _name = 'transport.carrier.action.wizard'
    _description = 'Transport Carrier Wizard'

    def carrier_create_label(self):
        model_picking = self.env['stock.picking']
        picking_ids = model_picking.browse(self._context['active_ids'])
        for picking in picking_ids:
            picking.get_number_of_package()
        model_picking.action_carrier(picking_ids, True, False, False, False)
        return

    def carrier_delete_shipping(self):
        model_picking = self.env['stock.picking']
        picking_ids = model_picking.browse(self._context['active_ids'])
        model_picking.action_carrier(picking_ids, False, True, False, False)
        return

    def carrier_validate_shipping(self):
        model_picking = self.env['stock.picking']
        picking_ids = model_picking.browse(self._context['active_ids'])
        model_picking.action_carrier(picking_ids, False, False, True, False)
        return

    def carrier_get_tracking_shipping(self):
        model_picking = self.env['stock.picking']
        picking_ids = model_picking.browse(self._context['active_ids'])
        model_picking.action_carrier(picking_ids, False, False, False, True)
        return
