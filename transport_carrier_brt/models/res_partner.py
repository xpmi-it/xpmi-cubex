# -*- coding: utf-8 -*-
# Copyright (C) 2019-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import models, fields


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    departure_depot_brt = fields.Char(string='Departure Depot BRT')
