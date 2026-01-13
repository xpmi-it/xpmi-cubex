# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from odoo import fields, models

SHIPPING_WEIGHT_UOM = [
    ('kg', 'kg'),
    ('g', 'g'),
    ('lb', 'lb'),
    ('oz', 'oz'),
]
SHIPPING_SIZE_UOM = [
    ('cm', 'cm'),
    ('in', 'in'),
]


class ProductProduct(models.Model):
    _inherit = "product.product"

    feed_shipping_group_id = fields.Many2one(
        comodel_name='product.data.feed.shipping.group',
        string='Shipping Label',
        domain="[('type', '=', 'shipping_group')]",
        help='Allow grouping products together so that you can configure specific shipping rates.',
    )
    feed_shipping_weight = fields.Float(
        string='Shipping Weight',
        digits='Stock Weight',
    )
    feed_shipping_weight_uom = fields.Selection(
        selection=SHIPPING_WEIGHT_UOM,
        string='Shipping Weight UOM',
    )
    feed_shipping_length = fields.Float(
        string='Shipping Length',
        digits='Product Unit of Measure',
    )
    feed_shipping_width = fields.Float(
        string='Shipping Width',
        digits='Product Unit of Measure',
    )
    feed_shipping_height = fields.Float(
        string='Shipping Height',
        digits='Product Unit of Measure',
    )
    feed_shipping_size_uom = fields.Selection(
        selection=SHIPPING_SIZE_UOM,
        string='Size UOM',
        help='Unit of Measure for shipping.',
    )
    feed_shipping_transit_time_group_id = fields.Many2one(
        comodel_name='product.data.feed.shipping.group',
        string='Transit Time Label',
        domain="[('type', '=', 'transit_time')]",
        help='Use the transit time label in Merchant Center "Shipping settings" to def'
             'ine a specific transit time for each of the previously defined groups.',
    )
    feed_shipping_min_handling_time = fields.Integer()
    feed_shipping_max_handling_time = fields.Integer()
