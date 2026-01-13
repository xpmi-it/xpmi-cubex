# Copyright (C) 2018-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountPaymentRegisterInvInherit(models.TransientModel):
    _inherit = "account.payment.register"

    @api.model
    def _get_communication(self, lines):
        if len(lines.move_id) == 1:
            move = lines.move_id
            label = move.ref or move.name
        elif any(move.is_outbound() for move in lines.move_id):
            # outgoing payments references should use moves references
            labels = {move.ref or move.name for move in lines.move_id}
            return ", ".join(sorted(filter(lambda l: l, labels)))
        else:
            label = self.company_id.get_next_batch_payment_communication()
        return label
