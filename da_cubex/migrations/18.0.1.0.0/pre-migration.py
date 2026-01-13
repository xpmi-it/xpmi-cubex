#  Copyright 2024 Sergio Zanchetta
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo.upgrade import util

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info("Starting pre-migration for da_cubex")
    util.force_install_module(cr, "l10n_it_riba_oca", if_installed=["l10n_it_ricevute_bancarie"])
    # _logger.info("Uninstalling theme")
    # util.uninstall_theme(cr, "theme_alan")
    util.uninstall_module(cr, 'fb_pixel')
    #*****TEMA*****
    cr.execute("DELETE from theme_ir_ui_view where name ='Alan Static Snippets'")
    cr.execute("DELETE from theme_ir_ui_view where name ='Product Details Extends AS'")
    cr.execute("DELETE from theme_ir_ui_view where key ='theme_alan.theme_alan_static_snippet'")
    cr.execute("DELETE from ir_ui_view where name ='Alan Static Snippets'")
    cr.execute("DELETE from ir_model_data where name ='theme_alan_static_snippet'")
    cr.execute("DELETE from ir_model_data where name ='product' and module = 'fb_pixel'")
    cr.execute("DELETE from ir_model_data where name ='products' and module = 'fb_pixel'")
    cr.execute("DELETE from ir_ui_view where key ='sh_snippet_builder.sh_snippet_builder_snippets'")
    cr.execute("DELETE from ir_ui_view where key ='atharva_theme_base.products'")
    cr.execute("DELETE from ir_ui_view where key ='theme_alan.as_product_customization'")
    #**FINE TEMA**
    cr.execute("DELETE from ir_ui_view where key ='transport_carrier_brt.stock_picking_transport_carrier_brt_form_view_inherit'")
    cr.execute("""INSERT INTO date_range_type (name, active) VALUES ('{"en_US": "Anno fiscale New"}', true);""")
    cr.execute("UPDATE date_range SET type_id = (SELECT id FROM date_range_type WHERE name ->> 'en_US' = 'Anno fiscale New' AND active = true) WHERE type_id = 1;")

    _deleted_xml_records = \
        [
            # 'website_google_analytics_4.layout',
            # 'website_sale_google_analytics_4.layout',
            # 'website_sale_google_analytics_4.assets_frontend',
            # 'website_sale_tracking_base.layout',
            # 'website_sale_tracking_base.tracking_add_product_ids',
            # 'website_sale_tracking_base.tracking_add_search_term',
            # 'website_sale_tracking_base.tracking_add_product_template_id',
	    'website_sale_product_attachment.download_icons',
            'l10n_it_delivery_note.portal_my_home_delivery_note',
            'l10n_it_withholding_tax.print_withholding_tax',
            'da_cubex.delivery_note_report_template_inherit',
            'transport_carrier_base.sale_order_delivery_inherit_form_view',
            'transport_carrier_base.stock_picking_form_view_inherit',
            'common_connector_library.common_product_search_form_view',
            'common_connector_library.common_product_template_form_brand_add',
            'amazon_ept.view_amazon_instance_config_settings',
            'amazon_ept.view_amazon_config_settings'
            'theme_alan.custom_product_banner_form_view'
            # 'fb_pixel.payment',  # ci vuole?
            # 'website.submenu',  #per override fatto da atharva_theme_base su questa view
        ]
    for view in _deleted_xml_records:
        _logger.info("------DELETING view from z-cubex ")
        util.records.remove_view(cr, xml_id=view, silent=True)

    util.force_upgrade_of_fresh_module(cr, "l10n_it_account")
    #util.force_install_module(
    #    cr,
    #    "l10n_it_account_vat_period_end_settlement",
    #    if_installed=["account_vat_period_end_statement"],
    #)
    util.merge_module(cr, 'commission', 'commission_oca')

    # ****copied from cie START
    util.force_install_module(cr, "l10n_it_central_journal_reportlab",
                              if_installed=["l10n_it_central_journal"])
    modules_to_uninstall = [
        # 'l10n_it_ricevute_bancarie',
        'l10n_it_ricevute_bancarie_enterprise',
        'l10n_it_ricevute_bancarie_extended',
        'l10n_it_central_journal',
        'website_google_analytics_4',
        'da_check_access_attachment',
        #'l10n_it_reverse_charge',
        #'l10n_it_delivery_note_base',
    ]
    for module in modules_to_uninstall:
        util.uninstall_module(cr, module)
    # modules_to_uninstall2 = [
    #     'l10n_it_ricevute_bancarie_enterprise',
    #     'l10n_it_ricevute_bancarie_extended',
    #     'l10n_it_central_journal',
    # ]
    # # ****copied from cie end
    # for module in modules_to_uninstall2:
    #     util.uninstall_module(cr, module)

    # util.force_install_module(cr, "l10n_it_edi_extension", if_installed=["l10n_it_edi"])
    # cr.execute("DELETE FROM ir_asset")
