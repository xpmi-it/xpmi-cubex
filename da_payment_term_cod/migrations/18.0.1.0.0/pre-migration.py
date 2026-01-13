#  Copyright 2024 Sergio Zanchetta
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo.upgrade import util

_logger = logging.getLogger(__name__)


# Fatto per Cubex , eliminare dopo migrazione;
def migrate(cr, version):
    _logger.info("Starting pre-migration for da_cubex")
    util.force_install_module(
        cr, "l10n_it_riba_oca", if_installed=["l10n_it_ricevute_bancarie"]
    )
    util.uninstall_module(cr, "fb_pixel")
    # *****TEMA*****
    cr.execute("DELETE from theme_ir_ui_view where name ='Alan Static Snippets'")
    cr.execute("DELETE from theme_ir_ui_view where name ='Product Details Extends AS'")
    cr.execute(
        "DELETE from theme_ir_ui_view where key ='theme_alan.theme_alan_static_snippet'"
    )
    cr.execute("DELETE from ir_ui_view where name ='Alan Static Snippets'")
    cr.execute("DELETE from ir_model_data where name ='theme_alan_static_snippet'")
    cr.execute(
        "DELETE from ir_model_data where name ='product' and module = 'fb_pixel'"
    )
    cr.execute(
        "DELETE from ir_model_data where name ='products' and module = 'fb_pixel'"
    )
    cr.execute(
        "DELETE from ir_ui_view "
        "where key ='sh_snippet_builder.sh_snippet_builder_snippets'"
    )
    cr.execute("DELETE from ir_ui_view where key ='atharva_theme_base.products'")
    cr.execute(
        "DELETE from ir_ui_view where key ='theme_alan.as_product_customization'"
    )
    # **FINE TEMA**
    cr.execute(
        """
        DELETE from ir_ui_view
        where key ='transport_carrier_brt.stock_picking_transport_carrier_brt_form_view_inherit'
        """  # noqa E501
    )
    cr.execute(
        """
        INSERT INTO date_range_type (name, active)
        VALUES ('{"en_US": "Anno fiscale New"}', true);
        """
    )
    cr.execute(
        """
        UPDATE date_range
        SET type_id = (
            SELECT id
            FROM date_range_type
            WHERE
                name ->> 'en_US' = 'Anno fiscale New'
                AND active = true
        )
        WHERE type_id = 1;
        """
    )

    _deleted_xml_records = [
        "website_sale_product_attachment.download_icons",
        "l10n_it_delivery_note.portal_my_home_delivery_note",
        "l10n_it_withholding_tax.print_withholding_tax",
        "da_cubex.delivery_note_report_template_inherit",
        "transport_carrier_base.sale_order_delivery_inherit_form_view",
        "transport_carrier_base.stock_picking_form_view_inherit",
        "common_connector_library.common_product_search_form_view",
        "common_connector_library.common_product_template_form_brand_add",
        "amazon_ept.view_amazon_instance_config_settings",
        "amazon_ept.view_amazon_config_settings"
        "theme_alan.custom_product_banner_form_view",
    ]
    for view in _deleted_xml_records:
        _logger.info("------DELETING from da_payment_term_cod")
        util.records.remove_view(cr, xml_id=view, silent=True)
