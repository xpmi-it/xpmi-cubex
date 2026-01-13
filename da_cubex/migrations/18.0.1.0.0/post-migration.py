#  Copyright 2024 Sergio Zanchetta
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo.upgrade import util

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info("Starting post-migration for da_cubex")
    _logger.info("Uninstalling modules")
    modules_to_uninstall = [
                            # 'account_vat_period_end_statement',
                            'base_product_mass_addition',
                            'da_account_aged_partner_balance',
                            'da_account_move_show_posted_before',
                            'da_fiscalcode_upper',
                            #'da_import_price_list',
                            'da_print_package_picking_and_dn',
                            # 'l10n_it_ricevute_bancarie',
                            'l10n_it_ricevute_bancarie_enterprise',
                            'l10n_it_ricevute_bancarie_extended',
                            'purchase_order_line_packaging_qty',
                            'purchase_quick',
                            'web_sheet_full_width',
                            'website_sale_google_analytics_4',
                            'website_google_analytics_4',
                            'sale_order_line_packaging_qty',
                            'sale_commission_oca',
                            'website_sale_product_description']
    for module in modules_to_uninstall:
        util.uninstall_module(cr, module)

    _logger.info("Deleting views")
    _deleted_xml_records = \
        ['portal.portal_docs_entry', 'portal.portal_my_home']
    for view in _deleted_xml_records:
        util.records.remove_view(cr, xml_id=view, silent=True)
    cr.execute("DELETE FROM ir_asset")
