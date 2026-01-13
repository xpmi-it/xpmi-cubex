# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models


class AccessoriesServicesGls(models.Model):
    _name = 'accessories.services.gls'
    _description = 'Accessories Services Gls'

    name = fields.Char(string='Name Service', size=2)
    name_gls = fields.Char(string='Name Service for GLS')
