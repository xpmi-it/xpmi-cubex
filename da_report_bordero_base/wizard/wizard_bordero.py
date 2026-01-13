# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, models, fields
from odoo.exceptions import UserError


class PickingBorderoWizard(models.TransientModel):
    _name = 'picking.bordero.wizard'
    _description = "Picking Bordero General Wizard"

    def check_carrier(self, picking_ids):
        all_carrier = picking_ids.mapped('transport_carrier_id')
        if not all_carrier:
            raise UserError('No Carrier on Picking')
        elif all_carrier and len(all_carrier) > 1:
            raise UserError('Selected picking must have same carrier')
        else:
            return all_carrier

    def set_num_bordero_on_picking(self, picking_ids, num_bordero):
        for picking in picking_ids:
            if not picking.num_bordero:
                picking.num_bordero = num_bordero

    def print_bordero(self):
        data = self._prepare_data_bordero()
        return self.env.ref('da_report_bordero_base.report_bordero').report_action(self, data)

    #base method for other tc modules
    def check_specific_transport_carrier(self, picking_ids):
        return picking_ids

    # Se ok, rimuovere da modulo brt
    def get_city_state(self, picking, partner_picking):
        if picking:
            location = ''
            if partner_picking.city:
                location = partner_picking.city.upper()
            if partner_picking.state_id:
                location += ' ' + '(' + partner_picking.state_id.code + ')'
            return location

    def _prepare_data_bordero(self):
        self.ensure_one()
        model_pick = self.env['stock.picking']
        picking_ids = model_pick.browse(self._context['active_ids'])
        picking_no_drop_ids = picking_ids.filtered(lambda pick: not pick.picking_type_id.dropshipping)  # for drop picking, customer need print bordero before validation picking
        state_picking_ids = picking_no_drop_ids.mapped('state')
        if not all(element == 'done' for element in state_picking_ids):
            raise UserError('Select only Validated Picking')
        first_num_bordero = 0
        for picking in picking_ids:
            if picking.num_bordero:
                first_num_bordero = picking.num_bordero
                break
            pass
        new_picking_ids = []
        if first_num_bordero:
            for new_pick in picking_ids:
                if new_pick.num_bordero and new_pick.num_bordero == first_num_bordero:
                    new_picking_ids.append(new_pick.id)
        new_picking_ids = model_pick.browse(new_picking_ids)
        if len(new_picking_ids) > 0:
            picking_ids = new_picking_ids
        else:
            pass
        picking_sorted_ids = sorted(picking_ids, key=lambda a: a.id)
        data = []
        carrier = self.check_carrier(picking_ids)
        self.check_specific_transport_carrier(picking_ids)
        for pick in picking_sorted_ids:
            data.append(self.prepare_data_picking_bordero(pick))
        if not first_num_bordero:
            sequence_bordero_id = carrier.sequence_bordero_id
            num_bordero = sequence_bordero_id.next_by_id()
            self.set_num_bordero_on_picking(picking_sorted_ids, num_bordero)
        return {'picking_data': data,
                'transport_carrier_id': carrier.carrier,
                'sender_customer_code': carrier.sender_customer_code,
                'sender_company_name': self.env.company.name}

    def prepare_data_picking_bordero(self, pick):
        model_transport_carrier = self.env['transport.carrier']
        partner_picking = pick.compute_partner_picking()
        return {'pick_name': pick.name,
                'destinatario': model_transport_carrier.get_ragione_sociale(pick),
                'service_type': pick.service_type,
                'address': pick.get_address(partner_picking).upper(),
                'zip': partner_picking.zip,
                'city_state': self.get_city_state(pick, partner_picking),
                'pick_id': pick.id,
                'number_label': len(pick.parcel_label_ids),
                'weight': pick.weight,
                'volume': round(pick.volume, 2),
                }