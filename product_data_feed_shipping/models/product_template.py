# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from odoo import api, fields, models
from .product_product import SHIPPING_WEIGHT_UOM, SHIPPING_SIZE_UOM


class ProductTemplate(models.Model):
    _inherit = "product.template"

    feed_shipping_ids = fields.Many2many(
        comodel_name='product.data.feed.shipping',
        string='Shipping Costs',
    )
    feed_shipping_group_id = fields.Many2one(
        comodel_name='product.data.feed.shipping.group',
        string='Shipping Label',
        domain="[('type', '=', 'shipping_group')]",
        context="{'default_type': 'shipping_group'}",
        help='Allow grouping products together so that you can configure specific shipping rates.',
        compute='_compute_feed_shipping_group_id',
        inverse='_inverse_feed_shipping_group_id',
        store=True,
    )
    feed_shipping_weight = fields.Float(
        string='Shipping Weight',
        digits='Stock Weight',
        compute='_compute_feed_shipping_weight',
        inverse='_inverse_feed_shipping_weight',
        store=True,
    )
    feed_shipping_weight_uom = fields.Selection(
        selection=SHIPPING_WEIGHT_UOM,
        string='Shipping Weight UOM',
        compute='_compute_feed_shipping_weight_uom',
        inverse='_inverse_feed_shipping_weight_uom',
        store=True,
    )
    feed_shipping_length = fields.Float(
        string='Shipping Length',
        digits='Product Unit of Measure',
        compute='_compute_feed_shipping_size',
        inverse='_inverse_feed_shipping_length',
        store=True,
    )
    feed_shipping_width = fields.Float(
        string='Shipping Width',
        digits='Product Unit of Measure',
        compute='_compute_feed_shipping_size',
        inverse='_inverse_feed_shipping_width',
        store=True,
    )
    feed_shipping_height = fields.Float(
        string='Shipping Height',
        digits='Product Unit of Measure',
        compute='_compute_feed_shipping_size',
        inverse='_inverse_feed_shipping_height',
        store=True,
    )
    feed_shipping_size_uom = fields.Selection(
        selection=SHIPPING_SIZE_UOM,
        string='Size UOM',
        help='Unit of Measure for shipping.',
        compute='_compute_feed_shipping_size',
        inverse='_inverse_feed_shipping_size_uom',
        store=True,
    )
    feed_shipping_transit_time_group_id = fields.Many2one(
        comodel_name='product.data.feed.shipping.group',
        string='Transit Time Label',
        domain="[('type', '=', 'transit_time')]",
        context="{'default_type': 'transit_time'}",
        help='Use the transit time label in Merchant Center "Shipping settings" to def'
             'ine a specific transit time for each of the previously defined groups.',
        compute='_compute_feed_shipping_transit_time_group_id',
        inverse='_inverse_feed_shipping_transit_time_group_id',
        store=True,
    )
    feed_shipping_min_handling_time = fields.Integer(
        compute='_compute_feed_shipping_handling_time',
        inverse='_inverse_feed_shipping_min_handling_time',
        store=True,
    )
    feed_shipping_max_handling_time = fields.Integer(
        compute='_compute_feed_shipping_handling_time',
        inverse='_inverse_feed_shipping_max_handling_time',
        store=True,
    )
    feed_ships_from_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Ships From Country',
        ondelete='set null',
    )

    @api.depends('product_variant_ids.feed_shipping_group_id')
    def _compute_feed_shipping_group_id(self):
        self._compute_template_field_from_variant_field('feed_shipping_group_id')

    def _inverse_feed_shipping_group_id(self):
        self._set_product_variant_field('feed_shipping_group_id')

    @api.depends('product_variant_ids.feed_shipping_weight')
    def _compute_feed_shipping_weight(self):
        self._compute_template_field_from_variant_field('feed_shipping_weight')

    def _inverse_feed_shipping_weight(self):
        self._set_product_variant_field('feed_shipping_weight')

    @api.depends('product_variant_ids.feed_shipping_weight_uom')
    def _compute_feed_shipping_weight_uom(self):
        self._compute_template_field_from_variant_field('feed_shipping_weight_uom')

    def _inverse_feed_shipping_weight_uom(self):
        self._set_product_variant_field('feed_shipping_weight_uom')

    @api.depends(
        'product_variant_ids.feed_shipping_length',
        'product_variant_ids.feed_shipping_width',
        'product_variant_ids.feed_shipping_height',
        'product_variant_ids.feed_shipping_size_uom',
    )
    def _compute_feed_shipping_size(self):
        self._compute_template_field_from_variant_field('feed_shipping_length')
        self._compute_template_field_from_variant_field('feed_shipping_width')
        self._compute_template_field_from_variant_field('feed_shipping_height')
        self._compute_template_field_from_variant_field('feed_shipping_size_uom')

    def _inverse_feed_shipping_length(self):
        self._set_product_variant_field('feed_shipping_length')

    def _inverse_feed_shipping_width(self):
        self._set_product_variant_field('feed_shipping_width')

    def _inverse_feed_shipping_height(self):
        self._set_product_variant_field('feed_shipping_height')

    def _inverse_feed_shipping_size_uom(self):
        self._set_product_variant_field('feed_shipping_size_uom')

    @api.depends('product_variant_ids.feed_shipping_transit_time_group_id')
    def _compute_feed_shipping_transit_time_group_id(self):
        self._compute_template_field_from_variant_field('feed_shipping_transit_time_group_id')

    def _inverse_feed_shipping_transit_time_group_id(self):
        self._set_product_variant_field('feed_shipping_transit_time_group_id')

    @api.depends(
        'product_variant_ids.feed_shipping_min_handling_time',
        'product_variant_ids.feed_shipping_max_handling_time',
    )
    def _compute_feed_shipping_handling_time(self):
        self._compute_template_field_from_variant_field('feed_shipping_min_handling_time')
        self._compute_template_field_from_variant_field('feed_shipping_max_handling_time')

    def _inverse_feed_shipping_min_handling_time(self):
        self._set_product_variant_field('feed_shipping_min_handling_time')

    def _inverse_feed_shipping_max_handling_time(self):
        self._set_product_variant_field('feed_shipping_max_handling_time')
