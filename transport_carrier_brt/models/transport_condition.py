# -*- coding: utf-8 -*-
# Copyright (C) 2023-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models


class TransportConditionInherit(models.Model):
    _inherit = 'transport.condition'

    code_brt = fields.Char(string='Code BRT', help='This code is needed'
                                                   ' for Create shipment API call')
