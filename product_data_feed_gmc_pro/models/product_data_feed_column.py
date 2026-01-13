# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html).

from odoo import models


class ProductDataFeedColumn(models.Model):
    _inherit = "product.data.feed.column"

    def get_special_value(self, product):
        value = super(ProductDataFeedColumn, self).get_special_value(product)
        if self.recipient_id != self.env.ref(
                'product_data_feed_gmc.recipient_google_merchant_center'):
            return value
        return value
