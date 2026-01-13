# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models


class TransportCarrier(models.Model):
    _inherit = 'transport.carrier'
    _description = 'Transport Carrier'

    amz_carrier_code = fields.Char(string="Amazon Carrier Code")
