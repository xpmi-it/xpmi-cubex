# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import api, fields, models
from .product_product import ENERGY_EFFICIENCY_CLASSES


class ProductTemplate(models.Model):
    _inherit = "product.template"

    energy_efficiency_class = fields.Selection(
        selection=ENERGY_EFFICIENCY_CLASSES,
        string='Energy Efficiency',
        compute='_compute_energy_efficiency_class',
        inverse='_inverse_energy_efficiency_class',
        help='Energy Efficiency Class.',
        store=True,
    )

    @api.depends('product_variant_ids.energy_efficiency_class')
    def _compute_energy_efficiency_class(self):
        self._compute_template_field_from_variant_field('energy_efficiency_class')

    def _inverse_energy_efficiency_class(self):
        self._set_product_variant_field('energy_efficiency_class')
