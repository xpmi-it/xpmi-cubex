# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models, _


class StockPickingTypeInherit(models.Model):
    _inherit = 'stock.picking.type'

    dropshipping = fields.Boolean(string='Dropshipping')
