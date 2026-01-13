# Copyright (C) 2025-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    @api.model
    def _get_overdue_invoices(self):
        domain = self._get_overdue_invoices_domain()
        return self.env["account.move"].search(domain, order="invoice_date asc")
