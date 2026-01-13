# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, models, fields
from odoo.exceptions import UserError

class PickingBorderoWizardInherit(models.TransientModel):
    _inherit = 'picking.bordero.wizard'

    def check_specific_transport_carrier(self, picking_ids):
        res = super(PickingBorderoWizardInherit, self).check_specific_transport_carrier(picking_ids)
        if res and res[0].transport_carrier_id.carrier == 'gls':
            for picking in res:
                if not picking.validation_done or not picking.status_shipping_gls or picking.status_shipping_gls and picking.status_shipping_gls != 'closed':
                    raise UserError('Select only pickings done and with status shipping GLS closed')
        return res

    def prepare_data_picking_bordero(self, pick):
        res = super(PickingBorderoWizardInherit, self).prepare_data_picking_bordero(pick)
        if pick.transport_carrier_id.carrier == 'gls':
            date_done = pick.date_done.strftime('%d/%m/%y')
            res['number_shipping'] = pick.tc_shipping_id
            res['bda'] = pick.id
            res['pesovolume'] = round(pick.pesovolume, 2)
            res['date_done'] = date_done
            res['pricelist_code_gls'] = pick.pricelist_code_gls
        return res
