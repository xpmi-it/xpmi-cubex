# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from odoo import fields, models


class ProductDataFeedGMCSizeType(models.Model):
    _name = "product.data.feed.gmc_size_type"
    _description = 'Google Merchant Feed Size Types'

    name = fields.Char(required=True)

    _sql_constraints = [('product_data_feed_gmc_size_type_uniq',
                         'UNIQUE (name)',
                         'Google Merchant Size Type name must be unique.')]
