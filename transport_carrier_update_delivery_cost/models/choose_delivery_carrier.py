# -*- coding: utf-8 -*-
# Copyright (C) 2022-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models, _


class ChooseDeliveryCarrierInherit(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    def button_confirm(self):
        res = super(ChooseDeliveryCarrierInherit, self).button_confirm()
        self.order_id.update_delivery_cost()
        return res
