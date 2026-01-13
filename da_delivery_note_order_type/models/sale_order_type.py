# Copyright (C) 2018-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class SaleOrderTypologyInherit(models.Model):
    _inherit = "sale.order.type"

    delivery_note_type_id = fields.Many2one(
        "stock.delivery.note.type", string="DN Type"
    )
