# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models


class SaleOrderAmzInherit(models.Model):
    _inherit = 'sale.order'

    @staticmethod
    def amz_get_carrier_name_ept(picking):
        #override original method for put TC amazon code to amazon
        if picking.transport_carrier_id and picking.transport_carrier_id.amz_carrier_code:
            carrier_name = picking.transport_carrier_id.amz_carrier_code
        else:
            carrier_name = picking.transport_carrier_id.name
        if carrier_name:
            return carrier_name
        if picking.carrier_id and picking.carrier_id.amz_carrier_code:
            carrier_name = picking.carrier_id.amz_carrier_code
        else:
            carrier_name = picking.carrier_id.name
        return carrier_name