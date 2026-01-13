# Copyright (C) 2023-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class AccountPaymentTermInherit(models.Model):
    _inherit = "account.payment.term"

    cod = fields.Boolean(string="COD", help="Cash on Delivery")
