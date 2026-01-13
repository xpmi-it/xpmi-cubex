from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    feed_feature_ids = fields.Many2many(
        comodel_name='product.data.feed.feature.value',
        string='Features',
        compute='_compute_feed_feature_ids',
        inverse='_inverse_feed_feature_ids',
        store=True,
    )

    @api.depends('product_variant_ids.feed_feature_ids')
    def _compute_feed_feature_ids(self):
        self._compute_template_field_from_variant_field('feed_feature_ids')

    def _inverse_feed_feature_ids(self):
        self._set_product_variant_field('feed_feature_ids')
