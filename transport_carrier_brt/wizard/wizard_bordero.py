# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, models, fields
from odoo.exceptions import UserError


class PickingBorderoWizardBRT(models.TransientModel):
    _inherit = 'picking.bordero.wizard'

    def check_specific_transport_carrier(self, picking_ids):
        res = super(PickingBorderoWizardBRT, self).check_specific_transport_carrier(picking_ids)
        if res and res[0].transport_carrier_id.carrier == 'brt':
            for picking in res:
                if not picking.validation_done:
                    raise UserError('Select only pickings done and with Validation Done')
        return res

    #New in v18
    def prepare_data_picking_bordero(self, pick):
        res = super(PickingBorderoWizardBRT, self).prepare_data_picking_bordero(pick)
        if pick.transport_carrier_id.carrier == 'brt':
            res['tipo_porto'] = pick.tipo_porto.code_brt
            res['amount_insurance'] = pick.amount_insurance
            res['type_collection_cod'] = pick.type_collection_cod if pick.type_collection_cod else ' '
            res['amount_cash_on_delivery'] = pick.amount_cash_on_delivery
            res['pricing_condition_code'] = pick.pricing_condition_code
            res['label_from'] = pick.get_label_from()
            res['label_to'] = pick.get_label_to()
        return res