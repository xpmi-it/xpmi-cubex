# -*- coding: utf-8 -*-
# Copyright (C) 2022-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import models, fields, api

#prima i campi erano su product.packaging, ora su stock.package.type
#override field che diventano FLOAT da INT
class StockPackageTypeInherit(models.Model):
    _inherit = 'stock.package.type'

    height = fields.Float('Height')
    width = fields.Float('Width')
    packaging_length = fields.Float('Length')
