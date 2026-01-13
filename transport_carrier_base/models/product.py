# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, fields, models


class ProductInherit(models.Model):
    _inherit = 'product.product'

    number_package = fields.Integer(string='Number package',
                                    tracking=True)

class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    number_package = fields.Integer(inverse='_set_number_package',
                                    string='Number package',
                                    tracking=True,
                                    compute='_compute_number_package',
                                    store=True, default=1)

    @api.depends('product_variant_ids', 'product_variant_ids.number_package')
    def _compute_number_package(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.number_package = template.product_variant_ids.number_package
        for template in (self - unique_variants):
            template.number_package = ''

    def _set_number_package(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.number_package = self.number_package
