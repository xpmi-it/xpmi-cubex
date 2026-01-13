# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from odoo import api, fields, models

from odoo.addons.product_data_feed_energy_class.models.product_product import \
    ENERGY_EFFICIENCY_CLASSES
from .product_product import GMC_AGE_GROUPS, GMC_PAUSE_STATES


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # flake8: noqa: E501
    feed_gmc_identifier_exists = fields.Boolean(
        string='Identifier Exists',
        compute='_compute_feed_gmc_identifier_exists',
        inverse='_inverse_feed_gmc_identifier_exists',
        store=True,
    )
    feed_gmc_for_adult = fields.Boolean(
        string='For Adult',
        help='Indicate that the product are for adults only.',
        compute='_compute_feed_gmc_for_adult',
        inverse='_inverse_feed_gmc_for_adult',
        store=True,
    )
    feed_gmc_size_type_ids = fields.Many2many(
        comodel_name='product.data.feed.gmc_size_type',
        string='Size Types',
        compute='_compute_feed_gmc_size_type_ids',
        inverse='_inverse_feed_gmc_size_type_ids',
        store=True,
    )
    feed_gmc_multipack = fields.Integer(
        string='Pcs in Multipack',
        help="Indicate that you’ve grouped multiple identical products "
             "for sale as one product. To use in the \"multipack\" feed column.",
        compute='_compute_feed_gmc_multipack',
        inverse='_inverse_feed_gmc_multipack',
        store=True,
    )
    feed_gmc_is_bundle = fields.Boolean(
        string='Is bundle',
        help="Indicate that you’ve created this bundle "
             "(so it is not manufacturer-created bundle).",
        compute='_compute_feed_gmc_is_bundle',
        inverse='_inverse_feed_gmc_is_bundle',
        store=True,
    )
    feed_gmc_min_energy_efficiency_class = fields.Selection(
        selection=ENERGY_EFFICIENCY_CLASSES,
        string='Minimum EEI',
        help='Minimum Energy Efficiency Class.',
        compute='_compute_feed_gmc_min_energy_efficiency_class',
        inverse='_inverse_feed_gmc_min_energy_efficiency_class',
        store=True,
    )
    feed_gmc_max_energy_efficiency_class = fields.Selection(
        selection=ENERGY_EFFICIENCY_CLASSES,
        string='Maximum EEI',
        help='Maximum Energy Efficiency Class.',
        compute='_compute_feed_gmc_max_energy_efficiency_class',
        inverse='_inverse_feed_gmc_max_energy_efficiency_class',
        store=True,
    )
    feed_gmc_age_group = fields.Selection(
        selection=GMC_AGE_GROUPS,
        compute='_compute_feed_gmc_age_group',
        inverse='_inverse_feed_gmc_age_group',
        store=True,
    )
    feed_gmc_ads_redirect_url = fields.Char(
        string='Ads Redirect',
        help='Fill in this URL to specify additional landing page parameters on your product page on Google Shopping ads.',
        compute='_compute_feed_gmc_ads_redirect_url',
        inverse='_inverse_feed_gmc_ads_redirect_url',
        store=True,
    )
    feed_gmc_pause = fields.Selection(
        selection=GMC_PAUSE_STATES,
        string='Pause',
        help='Use the "pause" attribute to tell Google when you want to temporarily '
             'stop products from showing in all ads or Shopping destinations for up to 14 days.',
        compute='_compute_feed_gmc_pause',
        inverse='_inverse_feed_gmc_pause',
        store=True,
    )
    feed_gmc_shopping_ads_excluded_country = fields.Many2many(
        comodel_name='res.country',
        relation='feed_gmc_shopping_ads_excluded_res_country_rel',
        string='Excluded countries for Shopping ads',
        help='Use the excluded countries for Shopping ads attribute to control the '
             'different countries where your Shopping ads products are advertised. '
             'You can use this attribute when you need to override the feed country '
             'settings for some products in the feed.',
    )
    feed_gmc_included_destination_ids = fields.Many2many(
        comodel_name='product.data.feed.gmc_destination',
        relation='product_template_data_feed_gmc_included_destination_rel',
        string='Included destinations',
    )
    feed_gmc_excluded_destination_ids = fields.Many2many(
        comodel_name='product.data.feed.gmc_destination',
        relation='product_template_data_feed_gmc_excluded_destination_rel',
        string='Excluded destinations',
    )
    feed_gmc_external_seller_id = fields.Many2one(
        comodel_name='res.partner',
        string='External seller',
        ondelete='set null',
    )

    @api.depends('product_variant_ids', 'product_variant_ids.feed_gmc_identifier_exists')
    def _compute_feed_gmc_identifier_exists(self):
        unique_variants = self.filtered(lambda tmpl: len(tmpl.product_variant_ids) == 1)
        for template in unique_variants:
            template.feed_gmc_identifier_exists = template.product_variant_ids.feed_gmc_identifier_exists
        for template in (self - unique_variants):
            template.feed_gmc_identifier_exists = False

    def _inverse_feed_gmc_identifier_exists(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.feed_gmc_identifier_exists = template.feed_gmc_identifier_exists

    @api.depends('product_variant_ids', 'product_variant_ids.feed_gmc_for_adult')
    def _compute_feed_gmc_for_adult(self):
        unique_variants = self.filtered(lambda tmpl: len(tmpl.product_variant_ids) == 1)
        for template in unique_variants:
            template.feed_gmc_for_adult = template.product_variant_ids.feed_gmc_for_adult
        for template in (self - unique_variants):
            template.feed_gmc_for_adult = False

    def _inverse_feed_gmc_for_adult(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.feed_gmc_for_adult = template.feed_gmc_for_adult

    @api.depends('product_variant_ids', 'product_variant_ids.feed_gmc_size_type_ids')
    def _compute_feed_gmc_size_type_ids(self):
        unique_variants = self.filtered(lambda t: len(t.product_variant_ids) == 1)
        for tmpl in unique_variants:
            tmpl.feed_gmc_size_type_ids = tmpl.product_variant_ids.feed_gmc_size_type_ids
        for tmpl in (self - unique_variants):
            tmpl.feed_gmc_size_type_ids = False

    def _inverse_feed_gmc_size_type_ids(self):
        for tmpl in self:
            if len(tmpl.product_variant_ids) == 1:
                tmpl.product_variant_ids.feed_gmc_size_type_ids = tmpl.feed_gmc_size_type_ids

    @api.depends('product_variant_ids', 'product_variant_ids.feed_gmc_multipack')
    def _compute_feed_gmc_multipack(self):
        unique_variants = self.filtered(lambda tmpl: len(tmpl.product_variant_ids) == 1)
        for template in unique_variants:
            template.feed_gmc_multipack = template.product_variant_ids.feed_gmc_multipack
        for template in (self - unique_variants):
            template.feed_gmc_multipack = False

    def _inverse_feed_gmc_multipack(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.feed_gmc_multipack = template.feed_gmc_multipack

    @api.depends('product_variant_ids', 'product_variant_ids.feed_gmc_is_bundle')
    def _compute_feed_gmc_is_bundle(self):
        unique_variants = self.filtered(lambda tmpl: len(tmpl.product_variant_ids) == 1)
        for template in unique_variants:
            template.feed_gmc_is_bundle = template.product_variant_ids.feed_gmc_is_bundle
        for template in (self - unique_variants):
            template.feed_gmc_is_bundle = False

    def _inverse_feed_gmc_is_bundle(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.feed_gmc_is_bundle = template.feed_gmc_is_bundle

    @api.depends('product_variant_ids', 'product_variant_ids.feed_gmc_min_energy_efficiency_class')
    def _compute_feed_gmc_min_energy_efficiency_class(self):
        unique_variants = self.filtered(lambda tmpl: len(tmpl.product_variant_ids) == 1)
        for template in unique_variants:
            template.feed_gmc_min_energy_efficiency_class = template.product_variant_ids.feed_gmc_min_energy_efficiency_class
        for template in (self - unique_variants):
            template.feed_gmc_min_energy_efficiency_class = False

    def _inverse_feed_gmc_min_energy_efficiency_class(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.feed_gmc_min_energy_efficiency_class = template.feed_gmc_min_energy_efficiency_class

    @api.depends('product_variant_ids', 'product_variant_ids.feed_gmc_max_energy_efficiency_class')
    def _compute_feed_gmc_max_energy_efficiency_class(self):
        unique_variants = self.filtered(lambda tmpl: len(tmpl.product_variant_ids) == 1)
        for template in unique_variants:
            template.feed_gmc_max_energy_efficiency_class = template.product_variant_ids.feed_gmc_max_energy_efficiency_class
        for template in (self - unique_variants):
            template.feed_gmc_max_energy_efficiency_class = False

    def _inverse_feed_gmc_max_energy_efficiency_class(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.feed_gmc_max_energy_efficiency_class = template.feed_gmc_max_energy_efficiency_class

    @api.depends('product_variant_ids', 'product_variant_ids.feed_gmc_age_group')
    def _compute_feed_gmc_age_group(self):
        unique_variants = self.filtered(lambda tmpl: len(tmpl.product_variant_ids) == 1)
        for template in unique_variants:
            template.feed_gmc_age_group = template.product_variant_ids.feed_gmc_age_group
        for template in (self - unique_variants):
            template.feed_gmc_age_group = False

    def _inverse_feed_gmc_age_group(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.feed_gmc_age_group = template.feed_gmc_age_group

    @api.depends('product_variant_ids', 'product_variant_ids.feed_gmc_ads_redirect_url')
    def _compute_feed_gmc_ads_redirect_url(self):
        unique_variants = self.filtered(lambda tmpl: len(tmpl.product_variant_ids) == 1)
        for template in unique_variants:
            template.feed_gmc_ads_redirect_url = template.product_variant_ids.feed_gmc_ads_redirect_url
        for template in (self - unique_variants):
            template.feed_gmc_ads_redirect_url = False

    def _inverse_feed_gmc_ads_redirect_url(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.feed_gmc_ads_redirect_url = template.feed_gmc_ads_redirect_url

    @api.depends('product_variant_ids', 'product_variant_ids.feed_gmc_pause')
    def _compute_feed_gmc_pause(self):
        unique_variants = self.filtered(lambda tmpl: len(tmpl.product_variant_ids) == 1)
        for template in unique_variants:
            template.feed_gmc_pause = template.product_variant_ids.feed_gmc_pause
        for template in (self - unique_variants):
            template.feed_gmc_pause = False

    def _inverse_feed_gmc_pause(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.feed_gmc_pause = template.feed_gmc_pause
