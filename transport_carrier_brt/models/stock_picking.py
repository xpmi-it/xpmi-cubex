# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime
from pdf2image import convert_from_bytes
import requests, json, ast, time, base64
from dateutil.relativedelta import relativedelta

url_shipment = "https://api.brt.it/rest/v1/shipments/shipment"
url_delete = "https://api.brt.it/rest/v1/shipments/delete"
url_validate_shipping = "https://api.brt.it/rest/v1/shipments/shipment"
url_tracking = "https://api.brt.it/rest/v1/tracking/parcelID/"


class StockPickingBRTInherit(models.Model):
    _inherit = 'stock.picking'

    service_type = fields.Selection(
        selection=[('E', 'Service Priority'),
                   (' ', 'Service Standard'),
                   ('H', 'Service 10:30')
                   ],
        store=True,
        default=' ',
        string='Service Type')
    state_label_brt = fields.Selection(selection=[('ok', 'Labels Ok'),
                                                  ('to_process', 'To Process'),
                                                  ('no_brt', 'No BRT')
                                                  ],
                                       store=True,
                                       compute='compute_state_label_brt',
                                       string='Status Label BRT')
    # delivery_freight_type_code da eliminare campo - spostato in code_brt in tipo_porto(transport_condition)
    delivery_freight_type_code = fields.Selection(
        selection=[('DAP', 'DAP - Delivered at Place'),
                   ('EXW', 'EXW - Ex Works'),
                   ], default='DAP',
        string='Delivery Freight Type Code (vabcbo)')
    type_collection_cod = fields.Selection(
        selection=[('BM', 'ACCEPT BANK CHECK MADE TO THE SENDER'),
                   ('CM', 'ACCEPT CIRCULAR CHECK MADE TO THE SENDER'),
                   ('BB', 'ACCEPT BANK CHECK FOR COURIER WITH INDEMNITY'),
                   ('OM', 'ACCEPT CHECK LISTED TO ORIGINAL SENDER'),
                   ('OC', 'ACCEPT CIRCULAR CHECK LISTED TO THE ORIGINAL SENDER'),
                   (' ', 'ACCEPT CASH')
                   ],
        string='Type Collection COD (vabtic)',
        default=' '
    )
    pricing_condition_code = fields.Char(
        string='Pricing Condition Code (vabctr)',
        compute="_compute_pricing_condition_code",
        store=True,
    )

    @api.depends("transport_carrier_id")
    def _compute_pricing_condition_code(self):
        for picking in self:
            if picking.transport_carrier_id:
                picking.pricing_condition_code = picking.transport_carrier_id.pricing_condition_code

    @api.depends('transport_carrier_id', 'parcel_label_ids.parcel_img',
                 'parcel_label_ids.parcel_img_zpl')
    def compute_state_label_brt(self):
        for picking in self:
            if picking.transport_carrier_id and not picking.transport_carrier_id.carrier == 'brt' or not picking.transport_carrier_id:
                picking.state_label_brt = 'no_brt'
            else:
                if not picking.parcel_label_ids:
                    picking.state_label_brt = 'to_process'
                else:
                    state = []
                    for label_line in picking.parcel_label_ids:
                        if label_line.parcel_img or label_line.parcel_img_zpl:
                            state.append('True')
                        else:
                            state.append('False')
                        if 'False' in state:
                            picking.state_label_brt = 'to_process'
                        else:
                            picking.state_label_brt = 'ok'

    def carrier_get_tracking_shipping(self, picking_ids):
        if picking_ids:
            if picking_ids[0].transport_carrier_id.carrier == 'brt':
                type_tracking = picking_ids[0].transport_carrier_id.type_tracking_ref
                for picking in picking_ids:
                    if picking.parcel_label_ids:
                        if type_tracking == 'segnacollo':
                            picking.carrier_tracking_ref = picking.parcel_label_ids[
                                0].segnacollo
                        url_tracking_complete = url_tracking + picking.parcel_label_ids[
                            0].segnacollo
                        transport_carrier_id = picking.transport_carrier_id
                        request = requests.get(url_tracking_complete, headers={
                            'content-type': 'application/json',
                            'userID': transport_carrier_id.user,
                            'password': transport_carrier_id.passwd})
                        if request.status_code != 200:
                            picking.error_tracking = 'Error Tracking Shipping on Picking: ' + picking.name + ' Generic Error:' + request.reason
                        if request.status_code == 200:
                            response_decoded = request.content.decode("UTF-8")
                            response_dict = ast.literal_eval(response_decoded)
                            if response_dict['ttParcelIdResponse']['executionMessage'][
                                'severity'] == 'ERROR':
                                picking.error_tracking = 'Error Tracking Shipping on Picking: ' + picking.name + ' ' + \
                                                         response_dict[
                                                             'ttParcelIdResponse'][
                                                             'executionMessage'][
                                                             'codeDesc'] + ': ' + \
                                                         response_dict[
                                                             'ttParcelIdResponse'][
                                                             'executionMessage'][
                                                             'message']
                            last_event = \
                                response_dict['ttParcelIdResponse']['lista_eventi'][0][
                                    'evento']
                            picking.date_last_update = last_event['data']
                            picking.time_last_update = last_event['ora']
                            picking.last_update_tracking = last_event['descrizione']
                            picking.response_tracking_tc = response_dict[
                                'ttParcelIdResponse']
                            if response_dict['ttParcelIdResponse']['bolla'][
                                'dati_spedizione']['spedizione_id']:
                                picking.tc_shipping_id = \
                                    response_dict['ttParcelIdResponse']['bolla'][
                                        'dati_spedizione']['spedizione_id']
                                if type_tracking == 'carrier_ref':
                                    picking.carrier_tracking_ref = \
                                        response_dict['ttParcelIdResponse']['bolla'][
                                            'dati_spedizione']['spedizione_id']
                                # if type_tracking == 'parcel_number':
                                #     picking.carrier_tracking_ref = response_dict['ttParcelIdResponse']['bolla']['dati_spedizione']['spedizione_id']
                            picking.error_tracking = False
            return super(StockPickingBRTInherit, self).carrier_get_tracking_shipping(
                picking_ids)

    def carrier_delete_shipping(self, picking_ids):
        if picking_ids[0].transport_carrier_id.carrier == 'brt':
            for picking in picking_ids:
                if picking.deletion_shipping: #Todo, error se non c'è deletion su TC?
                    transport_carrier_id = picking.transport_carrier_id
                    if transport_carrier_id.use_picking_name_alphanumeric_sender_reference:
                        alphanumeric_sender_reference = picking.name
                    else:
                        alphanumeric_sender_reference = transport_carrier_id.alphanumeric_sender_reference
                    if picking.parcel_label_ids:
                        body_delete_brt = {
                            "account": {"userID": transport_carrier_id.user,
                                        "password": transport_carrier_id.passwd},
                            "deleteData": {
                                "senderCustomerCode": transport_carrier_id.sender_customer_code,
                                "numericSenderReference": picking.id,
                                "alphanumericSenderReference": alphanumeric_sender_reference}}
                        body_delete_json = json.dumps(body_delete_brt)
                        request = requests.put(url_delete, body_delete_json,
                                               headers={'content-type': 'application/json'})
                        if request.status_code != 200:
                            raise UserError(
                                'Error Delete Shipping on Picking: ' + picking.name + ' Generic Error:' + request.reason)
                        if request.status_code == 200:
                            response_decoded = request.content.decode("UTF-8")
                            response_dict = ast.literal_eval(response_decoded)
                            if response_dict['deleteResponse']['executionMessage'][
                                'severity'] == 'ERROR':
                                raise UserError(
                                    'Error Delete Shipping on Picking: ' + picking.name + ' ' +
                                    response_dict['deleteResponse']['executionMessage'][
                                        'codeDesc'] + ': ' +
                                    response_dict['deleteResponse']['executionMessage'][
                                        'message'])
                            if response_dict['deleteResponse']['executionMessage'][
                                'codeDesc'] == 'SHIPMENT DELETED' and request.ok:
                                picking.cancellation_done = True
                                picking.validation_done = False
                                for label in picking.parcel_label_ids:
                                    label.is_label = False
                    self.env.cr.commit()
        return super(StockPickingBRTInherit, self).carrier_delete_shipping(picking_ids)

    def carrier_validate_shipping(self, picking_ids):
        if picking_ids[0].transport_carrier_id.carrier == 'brt':
            for picking in picking_ids:
                transport_carrier_id = picking.transport_carrier_id
                if transport_carrier_id.use_picking_name_alphanumeric_sender_reference:
                    alphanumeric_sender_reference = picking.name
                else:
                    alphanumeric_sender_reference = transport_carrier_id.alphanumeric_sender_reference
                body_validate_shipping_brt = {
                    "account": {"userID": transport_carrier_id.user,
                                "password": transport_carrier_id.passwd},
                    "confirmData": {
                        "senderCustomerCode": transport_carrier_id.sender_customer_code,
                        "numericSenderReference": picking.id,
                        "alphanumericSenderReference": alphanumeric_sender_reference}}
                body_validate_shipping_json = json.dumps(body_validate_shipping_brt)
                picking.body_confirm_tc = body_validate_shipping_json
                request = requests.put(url_validate_shipping, body_validate_shipping_json,
                                       headers={'content-type': 'application/json'})
                picking.response_confirm_tc = body_validate_shipping_json
                if request.status_code != 200:
                    raise UserError(
                        'Error Validation Shipping on Picking: ' + picking.name + ' Generic Error:' + request.reason)
                if request.status_code == 200:
                    response_decoded = request.content.decode("UTF-8")
                    response_dict = ast.literal_eval(response_decoded)
                    if response_dict['confirmResponse']['executionMessage'][
                        'severity'] == 'ERROR':
                        raise UserError(
                            'Error Validation Shipping on Picking: ' + picking.name + ' ' +
                            response_dict['confirmResponse']['executionMessage'][
                                'codeDesc'] + ': ' +
                            response_dict['confirmResponse']['executionMessage'][
                                'message'])
                    else:
                        picking.validation_done = True
                self.env.cr.commit()
        return super(StockPickingBRTInherit, self).carrier_validate_shipping(picking_ids)

    def carrier_create_label(self, picking_ids):
        res = super(StockPickingBRTInherit, self).carrier_create_label(picking_ids)
        if picking_ids[0].transport_carrier_id.carrier == 'brt':
            model_picking = self.env['stock.picking']
            model_picking.process_label_brt(picking_ids)
        return res

    def process_label_brt(self, picking_ids):
        for picking in picking_ids:
            if picking.parcel_label_ids:
                picking.brt_create_shipment()
                picking.cancellation_done = False
                time.sleep(picking.transport_carrier_id.time_sleep)
            self.env.cr.commit()
            tracking = picking.get_tracking_brt()
            picking.url_tracking = tracking

    def compute_weight_for_shipping(self):
        for picking in self:
            if picking.transport_carrier_id:
                tc_id = picking.transport_carrier_id
                weight = picking.get_weight_shipping()
                if tc_id.check_and_force_weight:
                    if weight >= tc_id.check_min_weight and weight <= tc_id.check_max_weight:
                        return tc_id.force_weight
                return weight
            return 0

    def brt_create_shipment(self):
        for picking in self:
            model_tc = self.env['transport.carrier']
            model_stock_picking = self.env['stock.picking']
            partner_picking = picking.compute_partner_picking()
            transport_carrier_id = picking.transport_carrier_id
            if transport_carrier_id.use_picking_name_alphanumeric_sender_reference:
                alphanumeric_sender_reference = picking.name
            else:
                alphanumeric_sender_reference = transport_carrier_id.alphanumeric_sender_reference
            if not picking.tipo_porto:
                tipo_porto = picking.get_tipo_porto_default_brt()
                if tipo_porto:
                    picking.tipo_porto = tipo_porto.id
            weight_for_shipping = picking.compute_weight_for_shipping()
            departure_depot = picking.get_departure_depot(transport_carrier_id)
            body_parcel_brt = {
                "account": {
                    "userID": transport_carrier_id.user,
                    "password": transport_carrier_id.passwd
                },
                "createData": {
                    "network": transport_carrier_id.network if transport_carrier_id.network else ' ',
                    "departureDepot": departure_depot,
                    "senderCustomerCode": transport_carrier_id.sender_customer_code,
                    "deliveryFreightTypeCode": picking.tipo_porto.code_brt,
                    "consigneeCompanyName": model_tc.get_ragione_sociale(picking).upper(),
                    "consigneeAddress": picking.get_address(partner_picking).upper(),
                    "consigneeTelephone": partner_picking.phone if partner_picking.phone else '',
                    "consigneeEMail": partner_picking.email if partner_picking.email else '',
                    "consigneeMobilePhoneNumber": partner_picking.mobile if partner_picking.mobile else '',
                    "isAlertRequired": int(transport_carrier_id.alert_shipping),
                    "pricingConditionCode": picking.pricing_condition_code if picking.pricing_condition_code else ' ',
                    "variousParticularitiesManagementCode":
                        transport_carrier_id.various_particularities_management_code if
                        transport_carrier_id.various_particularities_management_code else '',
                    "serviceType": picking.service_type,
                    "insuranceAmount": picking.amount_insurance,
                    "isCODMandatory": '1' if picking.amount_cash_on_delivery else '0',
                    "cashOnDelivery": picking.amount_cash_on_delivery,
                    "codPaymentType": picking.type_collection_cod if picking.type_collection_cod else ' ',
                    "notes": picking.get_note_shipping(),
                    "parcelsHandlingCode": transport_carrier_id.parcels_handling_code,
                    "originalSenderCompanyName": self.env.company.name,
                    "originalSenderZIPCode": "",
                    "originalSenderCountryAbbreviationISOAlpha2": "   ",
                    "numericSenderReference": picking.id,
                    "alphanumericSenderReference": alphanumeric_sender_reference,
                    "numberOfParcels": len(picking.parcel_label_ids),
                    "weightKG": weight_for_shipping,
                    "volumeM3": picking.volume,
                    "consigneeCountryAbbreviationISOAlpha2": partner_picking.country_id.code,
                    "consigneeZIPCode": partner_picking.zip,
                    "consigneeCity": partner_picking.city.upper() if partner_picking.city else '',
                    "consigneeProvinceAbbreviation": partner_picking.state_id.code if partner_picking.state_id.country_id.code == 'IT' else '',
                    "senderParcelType": 'E-COMMERCE'
                },
                "isLabelRequired": 1,
                "labelParameters": {
                    "outputType": transport_carrier_id.output_type,
                    "offsetX": 0,
                    "offsetY": 0,
                    "isBorderRequired": transport_carrier_id.border,
                    "isLogoRequired": transport_carrier_id.logo_label_brt,
                    "isBarcodeControlRowRequired":
                        transport_carrier_id.barcode_control_row
                }
            }
            if transport_carrier_id.label_format:
                body_parcel_brt['labelParameters']['labelFormat'] = \
                    transport_carrier_id.label_format
            picking.body_request_label_transport_carrier = body_parcel_brt
            body_json = json.dumps(body_parcel_brt)
            request = requests.post(url_shipment, body_json,
                                    headers={'content-type': 'application/json'})
            model_stock_picking.check_response_create_shipping(request, picking)

    def get_tipo_porto_default_brt(self):
        for picking in self:
            transport_condition_id = self.env['transport.condition'].search(
                [('code_brt', '=', 'DAP')], limit=1)
            return transport_condition_id

    def get_departure_depot(self, transport_carrier_id):
        for picking in self:
            departure_depot = transport_carrier_id.departure_depot
            if picking.picking_type_id.dropshipping and picking.partner_id.departure_depot_brt:
                departure_depot = picking.partner_id.departure_depot_brt
            elif picking.location_id.warehouse_id.departure_depot_brt:
                departure_depot = picking.location_id.warehouse_id.departure_depot_brt
            return departure_depot

    def check_response_create_shipping(self, request, picking):
        type_label = picking.transport_carrier_id.output_type
        type_tracking = picking.transport_carrier_id.type_tracking_ref
        if request.status_code != 200:
            picking.error_create_shipping = True
            picking.response_create_shipping_tc = True
            self.env.cr.commit()
            raise UserError('Picking: ' + picking.name + ' Generic Error:' + request.text)
        if request.status_code == 200:
            response_decoded = request.content.decode("UTF-8")
            response_dict = ast.literal_eval(response_decoded)
            response = response_dict['createResponse']['executionMessage']
            if response['severity'] == 'ERROR':
                error_response = response['codeDesc'] + ': ' + response['message']
                picking.error_create_shipping = True
                picking.response_create_shipping_tc = error_response
                self.env.cr.commit()
                raise UserError('Error Picking: ' + picking.name + error_response)
            labels = response_dict['createResponse']['labels']['label']
            if type_label == 'PDF':
                picking.get_brt_segnacolli(labels)
            else:
                picking.get_brt_segnacolli_zpl(labels)
            picking.error_create_shipping = False
            if type_tracking == 'parcel_number':  # for DPD
                picking.carrier_tracking_ref = \
                    response_dict['createResponse']['labels']['label'][0][
                        'parcelNumberGeoPost']
            if type_tracking == 'segnacollo':
                picking.carrier_tracking_ref = \
                response_dict['createResponse']['labels']['label'][0]['parcelID'][:-3]
        self.env.cr.commit()

    def get_brt_segnacolli(self, labels):
        for picking in self:
            index = 0
            for label_line in picking.parcel_label_ids:
                brt_decode = base64.b64decode(labels[index]['stream'])
                brt_image = convert_from_bytes(brt_decode)
                file_tmp = brt_image[0].save(open("/tmp/brt.jpg", "wb"))
                label_line.segnacollo = labels[index]['parcelID'][:-3]
                label_line.parcel_img = base64.b64encode(
                    open("/tmp/brt.jpg", "rb").read())
                index += 1

    def get_brt_segnacolli_zpl(self, labels):
        for picking in self:
            index = 0
            for label_line in picking.parcel_label_ids:
                zpl_decoded = base64.b64decode(labels[index]['stream'])
                label_line.segnacollo = labels[index]['parcelID'][:-3]
                label_line.parcel_img_zpl = zpl_decoded
                index += 1

    def get_tracking_brt(self):
        for picking in self:
            transport_carrier = picking.transport_carrier_id
            if not transport_carrier.start_link or not transport_carrier.end_link:
                raise UserError('In transport Carrier miss start or end link for tracking')
            link = ''
            if transport_carrier.start_link:
                link += transport_carrier.start_link
            if transport_carrier.type_tracking_ref in ('parcel_number', 'segnacollo'):
                link += str(picking.carrier_tracking_ref)
                return link
            link += str(picking.id)
            if transport_carrier.end_link:
                link += transport_carrier.end_link
            return link

    def get_address(self, partner_picking):
        for picking in self:
            if partner_picking:
                address = ''
                if partner_picking.street:
                    address += partner_picking.street
                if partner_picking.street2:
                    address += ' ' + partner_picking.street2
                return address

    def get_note_shipping(self):
        field_converter_model = self.env["ir.fields.converter"]
        for picking in self:
            note = ''
            if picking.transport_carrier_id.picking_in_note:
                note += picking.name + ' - '
            if picking.sale_id and picking.sale_id.note:
                note += field_converter_model.text_from_html(picking.sale_id.note, False,
                                                             False, "...")
            elif picking.note:
                note += field_converter_model.text_from_html(picking.note, False, False,
                                                             "...")
            return note[0:70]

    # cron
    def _update_ship_tracking_brt_cron(self):
        today = datetime.now().date()
        new_date = today - relativedelta(days=15)
        model_picking = self.env['stock.picking']
        picking_ids = model_picking.search(['|',
                                            ('last_update_tracking', '!=', 'CONSEGNATA'),
                                            ('last_update_tracking', '=', False),
                                            ('num_bordero', '!=', False),
                                            ('carrier', '=', 'brt'),
                                            ('date_done', '>=', new_date)])
        model_picking.carrier_get_tracking_shipping(picking_ids)

    # cron
    def _update_missing_tracking_ref_shipping_brt_cron(self):
        today = datetime.now().date()
        new_date = today - relativedelta(days=15)
        model_picking = self.env['stock.picking']
        picking_ids = model_picking.search(['|',
                                            ('last_update_tracking', '!=', 'CONSEGNATA'),
                                            ('last_update_tracking', '=', False),
                                            ('carrier_tracking_ref', '=', False),
                                            ('num_bordero', '!=', False),
                                            ('carrier', '=', 'brt'),
                                            ('date_done', '>=', new_date)])
        model_picking.carrier_get_tracking_shipping(picking_ids)

    def get_label_from(self):
        for picking in self:
            if picking.parcel_label_ids.mapped('segnacollo'):
                return min(picking.parcel_label_ids.mapped('segnacollo'))

    def get_label_to(self):
        for picking in self:
            if picking.parcel_label_ids.mapped('segnacollo'):
                return max(picking.parcel_label_ids.mapped('segnacollo'))
