# -*- coding: utf-8 -*-
# Copyright (C) 2019-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models
from collections import OrderedDict

class ReportBordero(models.AbstractModel):
    _name = 'report.da_report_bordero_base.view_report_bordero'
    _description = 'Report Bordero'

    def _get_report_values(self, docids, data):
        if 'context' in data.keys():
            del data['context']
        new_date = OrderedDict(sorted(data.items(), key=lambda t: t['pick_name']))
        docargs = {
            'picking_data': new_date['picking_data']
        }
        return docargs
