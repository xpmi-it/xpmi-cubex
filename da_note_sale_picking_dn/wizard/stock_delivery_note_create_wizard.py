# Copyright (C) 2024-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockDeliveryNoteCreateWizardInherit(models.TransientModel):
    _inherit = "stock.delivery.note.create.wizard"

    def confirm(self):
        res = super().confirm()
        for wizard in self:
            for picking_id in wizard.selected_picking_ids:
                picking_id.delivery_note_id.note = picking_id.note
        return res
