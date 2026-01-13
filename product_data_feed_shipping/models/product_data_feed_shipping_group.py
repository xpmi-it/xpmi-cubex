# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from odoo import fields, models


class ProductDataFeedShipping(models.Model):
    _name = "product.data.feed.shipping.group"
    _description = 'Product Shipping Groups'

    name = fields.Char(required=True)
    type = fields.Selection(
        selection=[
            ('shipping_group', 'Shipping Group'),
            ('transit_time', 'Transit Time'),
        ],
        default='shipping_group',
    )

    _sql_constraints = [('product_data_feed_shipping_group_uniq',
                         'UNIQUE (name)',
                         'Product Shipping Group Name must be unique.')]
