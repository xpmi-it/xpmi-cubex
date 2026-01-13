# Copyright (C) 2018-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    def _create_delivery_note(self):
        delivery_note_id = super()._create_delivery_note()
        if (
            self.sale_id
            and self.sale_id.type_id
            and self.sale_id.type_id.delivery_note_type_id
        ):
            delivery_note_id.type_id = self.sale_id.type_id.delivery_note_type_id.id
        return delivery_note_id

    def action_delivery_note_create(self):
        action = super().action_delivery_note_create()
        if (
            self.sale_id
            and self.sale_id.type_id
            and self.sale_id.type_id.delivery_note_type_id
        ):
            action["context"].update(
                {"default_type_id": self.sale_id.type_id.delivery_note_type_id.id}
            )
        return action
