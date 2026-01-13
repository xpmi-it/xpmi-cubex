# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models


class TransportCarrierBorderoInherit(models.Model):
    _inherit = 'transport.carrier'

    sequence_bordero_id = fields.Many2one('ir.sequence', string='Sequence Bordero')
