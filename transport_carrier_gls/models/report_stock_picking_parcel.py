# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from collections import OrderedDict


class ReportGlsListLabel(models.AbstractModel):
    _name = 'report.transport_carrier_gls.report_label_gls'
    _description = 'Label Gls'

    def _get_report_values(self, docids, data):
        if 'context' in data.keys():
            del data['context']
        new_date = OrderedDict(sorted(data.items(), key=lambda t: t[0]))
        docargs = {
            'lines': new_date['data_report']
        }
        return docargs


class ReportGlsZplLabel(models.AbstractModel):
    _name = 'report.transport_carrier_gls.report_label_zpl_gls'
    _description = 'Report Label ZPL'

    def _get_report_values(self, docids, data):
        if 'context' in data.keys():
            del data['context']
        docargs = {
            'labels': data['data_report']
        }
        return docargs