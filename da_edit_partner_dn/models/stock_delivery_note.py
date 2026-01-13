# Copyright (C) 2024-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso (gborruso@dinamicheaziendali.it)
# @author: Gianmarco Conte (gborruso@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).


from odoo import fields, models


class StockDeliveryNoteInherit(models.Model):
    _inherit = "stock.delivery.note"

    partner_id = fields.Many2one(readonly=False)
