from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    pricing_measure = fields.Integer(
        string='Pricing Measure',
        help='Product unit measure, for example: 150ml.',
    )
    pricing_base_measure = fields.Integer(
        string='Pricing Base Measure',
        help='Product unit base measure, for example: 100ml.',
    )
