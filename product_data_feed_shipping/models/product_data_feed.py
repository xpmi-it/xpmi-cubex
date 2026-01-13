# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html).

from odoo import fields, models


class ProductDataFeed(models.Model):
    _inherit = "product.data.feed"

    feed_shipping_ids = fields.Many2many(
        comodel_name='product.data.feed.shipping',
        string='Shipping Costs',
    )
