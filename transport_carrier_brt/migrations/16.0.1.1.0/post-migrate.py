# -*- coding: utf-8 -*-
# Copyright (C) 2023-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from openupgradelib import openupgrade  # pylint: disable=W7936
from odoo import SUPERUSER_ID, api

@openupgrade.migrate()
# def migrate(env, installed_version):
def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})


    dap = env.ref('transport_carrier_base.transport_condition_dap').id
    exw = env.ref('transport_carrier_base.transport_condition_exw').id

    openupgrade.logged_query(
        env.cr,
        """
        UPDATE stock_picking
        SET tipo_porto = %s
        WHERE delivery_freight_type_code = 'DAP'
        """% dap,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE stock_picking
        SET tipo_porto = %s
        WHERE delivery_freight_type_code = 'EXW'
        """% exw,
    )
