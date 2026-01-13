# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models


class TransportCarrierGLSInherit(models.Model):
    _inherit = 'transport.carrier'

    carrier = fields.Selection(selection_add=[('gls', 'GLS')])
    office_gls = fields.Char(string='Office Gls')
    generate_pdf = fields.Selection(selection=[('4', 'Immediate Return Pdf'),
                                               ('6', 'Immediate Return ZPL')],
                                    string='Generation Pdf')
    format_pdf = fields.Selection(selection=[('A5', 'A5 Format'),
                                             ('A6', 'A6 Format')],
                                  string='Pdf Format',
                                  default='A6')
    identpin = fields.Char(string='IdentPIN')
    type_package = fields.Selection(selection=[('0', 'Normal'),
                                             ('4', 'Plus')],
                                  string='Type Package',
                                  help='4 - Only for National Shipping')
    colletion_mode = fields.Selection(selection=[('CONT', 'Cash'),
                                                   ('AC', "Cashier's check"),
                                                   ('AB', 'Bank check'),
                                                   ('AP', 'Postal check'),
                                                   ('ASS',
                                                    'Postal check/Banking/Cashier'),
                                                   ('ABP', 'Check Bank/Postal'),
                                                   ('ASR', 'Check as released'),
                                                   ('ARM',
                                                    'Check as released int. Sender'),
                                                   ('ABC',
                                                    'Back Check/Cashier - No postal'),
                                                   ('ASRP',
                                                    'Check as released - No postal'),
                                                   ('ARMP',
                                                    'Check as released int. Sender - No postal')],
                                        string='Collection Mode')
    supplementary_insurance = fields.Selection(selection=[('A', 'ALL-IN'),
                                                          ('F', '10/10'),
                                                          ('',
                                                           'No Supplementary Insurance')],
                                               string='Supplementary Insurance')
    num_day_list_sped = fields.Integer(string='Num Day List Sped',
                                       help='Number of days back for the return of shipping '
                                            'list of shipments made(Used only in CloseWorkDay) - Max 40 days')
    light_pricelist = fields.Char(string='Code Light Pricelist')
    standard_pricelist = fields.Char(string='Code Standard Pricelist')
    weight_pricelist = fields.Float(string='Weight for check pricelist',
                                    help='If shipping is over this weight, it will '
                                         'applied standard pricelist, else, light pricelist')

    def get_contract_code(self, picking):
        weight_for_carrier = picking.get_weight_for_carrier()
        if weight_for_carrier <= picking.transport_carrier_id.weight_pricelist:
            return picking.transport_carrier_id.light_pricelist
        else:
            return picking.transport_carrier_id.standard_pricelist

    def get_note_gls(self, picking, partner_picking):
        field_converter_model = self.env["ir.fields.converter"]
        note = ''
        if picking.transport_carrier_id.picking_in_note:
            note += picking.name + ' - '
        if partner_picking.phone:
            note += partner_picking.phone + ' - '
        if picking and picking.sale_id and picking.sale_id.note:
            note += field_converter_model.text_from_html(
                picking.sale_id.note, False, False, "...")
        elif picking.note:
            note += field_converter_model.text_from_html(picking.note, False, False, "...")
        if len(note) < 41:
            return note
        else:
            return note[0:40]

    def get_additional_note_gls(self, picking, partner_picking):
        field_converter_model = self.env["ir.fields.converter"]
        note = ''
        if picking.transport_carrier_id.picking_in_note:
            note = picking.name + ' - '
        if partner_picking.phone:
            note += partner_picking.phone + ' - '
        if picking and picking.sale_id and picking.sale_id.note:
            note += field_converter_model.text_from_html(picking.sale_id.note, False, False, "...")
        elif picking.note:
            note += field_converter_model.text_from_html(picking.note, False, False, "...")
        if len(note) > 40:
            return note[40:81]
        else:
            return note
