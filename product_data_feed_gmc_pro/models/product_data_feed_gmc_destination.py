# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from odoo import fields, models


class ProductDataFeedGMCDestination(models.Model):
    _name = "product.data.feed.gmc_destination"
    _description = 'Google Merchant Feed Destinations'

    name = fields.Char(required=True)
    value = fields.Char(required=True)

    _sql_constraints = [('product_data_feed_gmc_destination_uniq',
                         'UNIQUE (value)',
                         'Google Merchant Destination Value must be unique.')]
