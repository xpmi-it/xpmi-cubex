# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import models, api


class PrintLabelWizardBrt(models.TransientModel):
    _inherit = 'print.label.wizard'

    def print_label(self):
        res = super(PrintLabelWizardBrt, self).print_label()
        self.ensure_one()
        if 'transport_carrier_id' in res.keys():
            if res['transport_carrier_id'].carrier == 'brt':
                return self.env.ref(
                    'transport_carrier_brt.report_list_label_brt').report_action(self,
                                                                                 res)
        return res

    def print_label_zpl(self):
        res = super(PrintLabelWizardBrt, self).print_label_zpl()
        self.ensure_one()
        if 'transport_carrier_id' in res.keys():
            if res['transport_carrier_id'].carrier == 'brt':
                return self.env.ref(
                    'transport_carrier_brt.report_list_label_zpl_brt').report_action(self,
                                                                                     res)
        return res
