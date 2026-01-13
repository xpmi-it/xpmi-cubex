# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import models, api
from odoo.exceptions import UserError

class PrintLabelWizard(models.TransientModel):
    _name = 'print.label.wizard'
    _description = 'Print Label Wizard'

    def check_carrier(self):
        model_picking = self.env['stock.picking']
        picking_list = self._context['active_ids']
        picking_ids = model_picking.browse(picking_list)
        all_carrier = picking_ids.mapped('transport_carrier_id')
        if not all_carrier:
            raise UserError('No Carrier on Picking')
        elif all_carrier and len(all_carrier) > 1:
            raise UserError(
                'Selected picking must have same carrier')
        else:
            return all_carrier

    def print_label(self):
        self.ensure_one()
        transport_carrier = self.check_carrier()
        if transport_carrier:
            picking_list = self._context['active_ids']
            # model_label_line = self.env['parcel.label']
            model_label_line = self.env['stock.quant.package']
            segnacollo_id = []
            label_list = model_label_line.search([('picking_id', 'in', picking_list)])
            for label in label_list.sorted('picking_id'):
                segnacollo_id.append(label.parcel_img)
                if label.parcel_img2:
                    segnacollo_id.append(label.parcel_img2)
                if label.parcel_img3:
                    segnacollo_id.append(label.parcel_img3)
                if label.parcel_img4:
                    segnacollo_id.append(label.parcel_img4)
            data = {'data_report': segnacollo_id, 'transport_carrier_id': transport_carrier}
            return data

    def print_label_zpl(self):
        self.ensure_one()
        transport_carrier = self.check_carrier()
        if transport_carrier:
            picking_list = self._context['active_ids']
            # model_label_line = self.env['parcel.label']
            model_label_line = self.env['stock.quant.package']
            label_list = model_label_line.search([('picking_id', 'in', picking_list)])
            file_zpl = ''
            for label in label_list.sorted(key=lambda l: l.picking_id.name, reverse=True):
                file_zpl += label.parcel_img_zpl if label.parcel_img_zpl else ""
            data = {'data_report': file_zpl, 'transport_carrier_id': transport_carrier}
            return data