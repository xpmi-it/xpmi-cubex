# Copyright (C) 2021-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"
    # _order = "priority desc, scheduled_date asc, id desc" this is the original order
    _order = "priority desc, id desc"
