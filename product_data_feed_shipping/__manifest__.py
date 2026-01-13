# Copyright © 2022 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/master/legal/licenses.html#odoo-apps).

{
    'name': 'Product Shipping Fields for Data Feeds',
    'version': '18.0.1.0.0',
    'category': 'Hidden',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz',
    'license': 'OPL-1',
    'summary': 'Extra Shipping Fields for Product Data Feeds',
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'live_test_url': 'https://garazd.biz/r/pSx',
    'depends': [
        'product_data_feed',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_data_feed_shipping_views.xml',
        'views/product_data_feed_views.xml',
        # 'views/product_template_views.xml',
        # 'views/product_product_views.xml',
    ],
    'price': 10.00,
    'currency': 'EUR',
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
