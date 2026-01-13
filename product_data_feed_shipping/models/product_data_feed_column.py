# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html).

from odoo import fields, models


class ProductDataFeedColumn(models.Model):
    _inherit = "product.data.feed.column"

    special_type = fields.Selection(
        selection_add=[('product_shipping', 'Product Shipping Costs')],
        ondelete={'product_shipping': 'cascade'},
    )

    def get_special_value(self, product):
        value = super(ProductDataFeedColumn, self).get_special_value(product)

        if self.special_type == 'product_shipping':
            shippings = product.feed_shipping_ids or self.feed_id.feed_shipping_ids
            value = []
            for shipping in shippings:
                value.append({
                    'country': shipping.country_id.code,
                    'region': shipping.get_region(),
                    'service': shipping.group_id and shipping.group_id.name or '',
                    'price': '%.2f %s' % (shipping.price, shipping.currency_id.name),
                    'min_handling_time': '%d' % shipping.min_handling_time,
                    'max_handling_time': '%d' % shipping.max_handling_time,
                    'min_transit_time': '%d' % shipping.min_transit_time,
                    'max_transit_time': '%d' % shipping.max_transit_time,
                })

        return value
