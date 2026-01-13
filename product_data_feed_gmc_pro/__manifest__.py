# Copyright © 2022 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/master/legal/licenses.html#odoo-apps).

{
    'name': 'Odoo Google Merchant Center Professional',
    'version': '18.0.1.0.0',
    'category': 'eCommerce',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz/en/blog/odoo-e-commerce/odoo-google-shopping',
    'license': 'OPL-1',
    'summary': 'Product Data Feeds for Google Merchant | Google Shopping Professional | Google Feed Pro',
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'live_test_url': 'https://garazd.biz/r/ckD',
    'depends': [
        'product_data_feed_extra',
        'product_data_feed_energy_class',
        'product_data_feed_gmc',
        'product_data_feed_feature',
        'product_data_feed_shipping',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/product_data_feed_gmc_destination_data.xml',
        'data/product_data_feed_gmc_size_type_data.xml',
        'data/product_data_feed_feature_data.xml',
        'data/product_data_feed_column_data.xml',
        # 'views/product_template_views.xml',
        # 'views/product_product_views.xml',
    ],
    'price': 40.00,
    'currency': 'EUR',
    'support': 'support@garazd.biz',
    'application': True,
    'installable': True,
    'auto_install': False,
}
