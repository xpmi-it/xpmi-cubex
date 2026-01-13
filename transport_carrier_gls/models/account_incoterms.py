# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, fields, models


class AccountIncotermsInherit(models.Model):
    _inherit = 'account.incoterms'

    code_gls = fields.Char(string='Code Gls', help="10 - the sender is responsible for all costs at destination (CUSTOMS, VAT AND DUTIES);"
                                                   "\n20 - the recipient bears all costs at destination (CUSTOMS OP, VAT AND DUTY);"
                                                   "\n30 - the sender takes charge of the CUSTOMS and DUTY OP. The recipient pays VAT;"
                                                   "\n40 - the sender takes charge of the CUSTOMS OP. The recipient will pay DUTY and VAT at destination.",
                           size=2)
