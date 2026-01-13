# Copyright (C) 2023-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Andrea Barbato (abarbato@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, fields, models
from collections import OrderedDict

class DueRegisterWizard(models.TransientModel):
    _name = "due.register.wizard"
    _description = "Due Register Wizard"

    date_at = fields.Datetime(string="Date Bill")
    supplier_ids = fields.Many2many(
        "res.partner",
        string="Suppliers",
        domain=[("supplier_rank", ">", 0)]
    )
    order_view = fields.Selection(
        selection=[
            ('supplier', 'Supplier'),
            ('date_due', 'Date Due'),
        ],
        string="Type",)
    order = fields.Selection(
        selection=[
            ('date', 'Accounting Date'),
            ('invoice_date', 'Invoice Date'),
        ],
        string="Order by",)

    def print_due_register_report(self):
        self.ensure_one()
        if self.order_view == 'supplier':
            return (
                self.env.ref("da_account_reports.action_due_register_report")
                .report_action(
                    [],
                    data={
                        "date_at": self.date_at,
                        "suppliers": self.supplier_ids.ids,
                        "order": self.order,
                        "order_view" : self.order_view,
                    },
                )
            )
        else:
            return (
                self.env.ref("da_account_reports.action_due_date_report")
                .report_action(
                    [],
                    data={
                        "date_at": self.date_at,
                        "suppliers": self.supplier_ids.ids,
                        "order": self.order,
                        "order_view": self.order_view,
                    },
                )
            )
