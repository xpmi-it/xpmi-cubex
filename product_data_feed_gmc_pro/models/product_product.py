# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.product_data_feed_energy_class.models.product_product import \
    ENERGY_EFFICIENCY_CLASSES

GMC_AGE_GROUPS = [
    ('adult', 'Adult (Typically teens or older. 13 years old or more)'),
    ('kids', 'Kids (5–13 years old)'),
    ('toddler', 'Toddler (1–5 years old)'),
    ('infant', 'Infant (3–12 months old)'),
    ('newborn', 'Newborn (0-3 months old)'),
]
GMC_PAUSE_STATES = [('ads', 'Ads'), ('all', 'All')]


class ProductProduct(models.Model):
    _inherit = "product.product"

    feed_gmc_identifier_exists = fields.Boolean(
        string='Identifier Exists',
        default=True,
    )
    feed_gmc_for_adult = fields.Boolean(
        string='For Adult',
        help='Indicate that the product are for adults only.',
        default=False,
    )
    feed_gmc_size_type_ids = fields.Many2many(
        comodel_name='product.data.feed.gmc_size_type',
        string='Size Types',
    )
    feed_gmc_multipack = fields.Integer(
        string='Pcs in Multipack',
        help="Indicate that you’ve grouped multiple identical products "
             "for sale as one product. To use in the \"multipack\" feed column.",
        default=0,
    )
    feed_gmc_is_bundle = fields.Boolean(
        string='Is bundle',
        help="Indicate that you’ve created this bundle "
             "(so it is not manufacturer-created bundle).",
    )
    feed_gmc_min_energy_efficiency_class = fields.Selection(
        selection=ENERGY_EFFICIENCY_CLASSES,
        string='Minimum EEI',
        help='Minimum Energy Efficiency Class.',
    )
    feed_gmc_max_energy_efficiency_class = fields.Selection(
        selection=ENERGY_EFFICIENCY_CLASSES,
        string='Maximum EEI',
        help='Maximum Energy Efficiency Class.',
    )
    feed_gmc_age_group = fields.Selection(selection=GMC_AGE_GROUPS)
    feed_gmc_pause = fields.Selection(
        selection=GMC_PAUSE_STATES,
        string='Pause',
        help='Use the "pause" attribute to tell Google when you want to temporarily '
             'stop products from showing in all ads or Shopping destinations '
             'for up to 14 days.',
    )
    feed_gmc_ads_redirect_url = fields.Char(
        string='Ads Redirect',
        help='Fill in this URL to specify additional landing page parameters on '
             'your product page on Google Shopping ads.',
    )

    @api.constrains('feed_gmc_size_type_ids')
    def _check_feed_gmc_size_type_ids(self):
        """Limit a count of linked records to two records,
        according Google requirements."""
        for product in self:
            if len(product.feed_gmc_size_type_ids) > 2:
                raise ValidationError(
                    _('You can set up to two size types to a product.'))
