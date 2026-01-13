# Copyright (C) 2025-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools.translate import html_translate


class ResCompanyInherit(models.Model):
    _inherit = "res.company"

    overdue_invoice_report_message = fields.Html(translate=html_translate)
