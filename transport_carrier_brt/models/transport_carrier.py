# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models


class TransportCarrierBRTInherit(models.Model):
    _inherit = 'transport.carrier'

    carrier = fields.Selection(selection_add=[('brt', 'BRT')])
    use_picking_name_alphanumeric_sender_reference = fields.Boolean(
        'Use Picking Name Alphanumeric Sender Reference')
    alphanumeric_sender_reference = fields.Char(string='Alphanumeric Sender Ref (vabrma)')
    sender_customer_code = fields.Char(string='Sender Customer Code (vabccm)')
    departure_depot = fields.Char(string='Departure Depot (vablnp)',
                                  help='Communicated by BRT')
    output_type = fields.Selection(selection=[('PDF', 'PDF'),
                                              ('ZPL', 'ZPL')],
                                   string='Output Type')
    parcels_handling_code = fields.Char(string='Parcels Handling Code (vabctm)',
                                        help='Communicated by BRT')
    border = fields.Selection(selection=[('0', 'No Border'),
                                         ('1', 'Yes Border')],
                              string='Border to Label')
    logo_label_brt = fields.Selection(selection=[('0', 'No Logo'),
                                                 ('1', 'Yes Logo')],
                                      string='Logo to Label')
    barcode_control_row = fields.Selection(
        selection=[('0', 'No Barcode Control Row'),
                   ('1', 'Yes Barcode Control Row')],
        string='Barcode Control Row to Label')
    time_sleep = fields.Float(string='Time Sleep',
                              help='Time sleep after every request for Labels',
                              default=1)
    alert_shipping = fields.Boolean(string='Request Alert Shipping')
    pricing_condition_code = fields.Char(string='Pricing Condition Code (vabctr)')
    type_tracking_ref = fields.Selection(selection=[('segnacollo', 'Segnacollo'),
                                                    ('carrier_ref', 'Carrier Ref'),
                                                    ('parcel_number', 'Parcel Number'),
                                                    ],
                                         default='carrier_ref',
                                         help='Parcel number is used only for DPD',
                                         string='Type Tracking Ref')
    network = fields.Char(string='Network (vabatb)',
                          help='EX: Italy: Empty, DPD: D, EuroExpress: E, Fedex: S')
    label_format = fields.Selection(selection=[('DP5', 'DP5')], help='Used Only for DPD',
                                    string='Label Format')
    various_particularities_management_code = fields.Char(
        string='Various Particularities Management Code')
