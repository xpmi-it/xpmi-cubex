# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, fields, models, _
from bs4 import BeautifulSoup
import requests
from odoo.exceptions import UserError
import unidecode

url = "https://labelservice.gls-italy.com/ilswebservice.asmx/AddParcel"
url_delete = "https://labelservice.gls-italy.com/ilswebservice.asmx/DeleteSped"
url_close_work_day = "https://labelservice.gls-italy.com/ilswebservice.asmx/CloseWorkDay"
url_list_sped = "https://labelservice.gls-italy.com/ilswebservice.asmx/ListSped"


class StockPickingGlsInherit(models.Model):
    _inherit = 'stock.picking'

    pricelist_code_gls = fields.Char(string='Pricelist Code Gls')
    state_label_gls = fields.Selection(selection=[('ok', 'Labels Ok'),
                                                  ('to_process', 'To Process'),
                                                  ('no_gls', 'No GLS'),
                                                  ('error_label', 'Error Label')],
                                       store=True,
                                       compute='compute_state_label_gls',
                                       string='Status Label GLS')
    status_shipping_gls = fields.Selection(
        selection=[('pending_closure', 'Pending Closure'),
                   ('closed', 'Closed')],
        string='Status Shipping Gls', copy=False)
    accessories_services_gls = fields.Many2many('accessories.services.gls',
                                                string='Accessories Services')
    date_booking_gdo = fields.Char(string='Date Booking Gdo',
                                   size=6,
                                   help='Set this only if Accessory Services 34 is '
                                        'setted on picking. Format: AAMMGG')
    time_note_booking_gdo = fields.Char(string='Time and Note Gdo',
                                        help='Set this only if Accessory Services 34 '
                                             'is setted on picking')
    gdo = fields.Boolean(compute='_compute_if_gdo', store=True)

    @api.depends('accessories_services_gls')
    def _compute_if_gdo(self):
        for picking in self:
            picking.gdo = False
            if '34' in picking.accessories_services_gls.mapped('name'):
                picking.gdo = True

    def carrier_delete_shipping(self, picking_ids):
        if picking_ids[0].transport_carrier_id.carrier == 'gls':
            for picking in picking_ids:
                if picking.deletion_shipping:  # Todo, error se non c'è deletion su TC?
                    if picking.tc_shipping_id:
                        if picking.parcel_label_ids:
                            data_delete = {'SedeGls': picking.transport_carrier_id.office_gls,
                                           'CodiceClienteGls': picking.transport_carrier_id.user,
                                           'PasswordClienteGls': picking.transport_carrier_id.passwd,
                                           'NumSpedizione': picking.tc_shipping_id
                                           }
                            response = requests.post(url_delete, data=data_delete, headers={
                                'content-type': 'application/x-www-form-urlencoded'})
                            deleted = self.check_delete_ok(response, picking.tc_shipping_id)
                            if deleted == True:
                                picking.cancellation_done = True
                                picking.validation_done = False
                                for label in picking.parcel_label_ids:
                                    label.is_label = False
                                picking.status_shipping_gls = 'pending_closure'
                                self.env.cr.commit()
        return super(StockPickingGlsInherit, self).carrier_delete_shipping(picking_ids)

    def check_delete_ok(self, response, tc_shipping_id):
        if response and tc_shipping_id:
            soup = BeautifulSoup(response.content, 'lxml')
            text = 'Eliminazione della spedizione ' + tc_shipping_id + ' avvenuta.'
            if soup.text == text:
                return True
            else:
                raise UserError(soup.text)

    @api.depends('transport_carrier_id', 'parcel_label_ids.parcel_img',
                 'parcel_label_ids', 'tc_shipping_id')
    def compute_state_label_gls(self):
        for picking in self:
            if picking.transport_carrier_id and picking.transport_carrier_id.carrier != 'gls' or not picking.transport_carrier_id:
                picking.state_label_gls = 'no_gls'
            else:
                if not picking.parcel_label_ids:
                    picking.state_label_gls = 'to_process'
                else:
                    if picking.tc_shipping_id and picking.tc_shipping_id[0] == '8':
                        picking.state_label_gls = 'error_label'
                        continue
                    state = []
                    for label_line in picking.parcel_label_ids:
                        if label_line.parcel_img or label_line.parcel_img_zpl:
                            state.append('True')
                        else:
                            state.append('False')
                        if 'False' in state:
                            picking.state_label_gls = 'to_process'
                        else:
                            picking.state_label_gls = 'ok'

    def carrier_validate_shipping(self, picking_ids):
        if picking_ids[0].transport_carrier_id.carrier == 'gls':
            model_picking = self.env['stock.picking']
            model_picking.validate_shipping_gls(picking_ids)
        return super(StockPickingGlsInherit, self).carrier_validate_shipping(picking_ids)

    def carrier_create_label(self, picking_ids):
        res = super(StockPickingGlsInherit, self).carrier_create_label(picking_ids)
        if picking_ids[0].transport_carrier_id.carrier == 'gls':
            model_picking = self.env['stock.picking']
            model_picking.process_label_gls(picking_ids)
        return res

    def process_label_gls(self, picking_ids):
        for picking in picking_ids:
            if picking.transport_carrier_id and picking.transport_carrier_id.carrier == 'gls':
                if picking.parcel_label_ids:
                    picking.call_gls()
                    picking.cancellation_done = False
                if picking.tc_shipping_id:
                    tracking = picking.get_tracking(picking.tc_shipping_id)
                    tracking_ref = picking.get_tracking_ref(picking.tc_shipping_id)
                    picking.url_tracking = tracking
                    picking.carrier_tracking_ref = tracking_ref

    def call_gls(self):
        for picking in self:
            transport_carrier_id = picking.transport_carrier_id
            body = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
                        <Info>
                            <SedeGls>%s</SedeGls>
                            <CodiceClienteGls>%s</CodiceClienteGls>
                            <PasswordClienteGls>%s</PasswordClienteGls>
                            %s
                        </Info>
                        """ % (transport_carrier_id.office_gls,
                               transport_carrier_id.user,
                               transport_carrier_id.passwd,
                               self.get_parcel_text(),
                               )
            data_infoparcel = {'XMLInfoParcel': body}
            picking.body_request_label_transport_carrier = body
            response = requests.post(url, data=data_infoparcel, headers={
                'content-type': 'application/x-www-form-urlencoded'})
            soap = BeautifulSoup(response.content, 'lxml')
            if soap:
                if soap.find('descrizioneerrore'):
                    picking.response_transport_carrier = soap.find(
                        'descrizioneerrore').text
                    continue
                shipping = soap.find('numerospedizione')
                if shipping:
                    picking.error_create_shipping = False
                    num_shipping = shipping.text
                    picking.tc_shipping_id = num_shipping
                    if picking.accessories_services_gls:
                        self.check_availability_additional_services(
                            picking.accessories_services_gls, soap)
                    type_parcel = picking.get_type_parcel()
                    for parcel in self.parcel_label_ids:
                        self.get_error_state_gls(parcel.picking_id.name, response)
                        parcel.get_segnacolli(type_parcel)
                    picking.error_create_shipping = False
                    self.env.cr.commit()

    def get_type_parcel(self):
        for picking in self:
            type_parcel_setting = picking.transport_carrier_id.generate_pdf
            if type_parcel_setting == '4':
                return 'pdf'
            elif type_parcel_setting == '6':
                return 'zpl'

    def check_availability_additional_services(self, accessories_services_gls, soap):
        additional_services = soap.find('sprinter').text
        for service in accessories_services_gls:
            if service.name_gls not in additional_services:
                raise UserError(
                    'picking n: ' + self.name + '. Service ' +
                    service.name_gls + ' non available for this place')

    def get_error_state_gls(self, pick, response):
        if response:
            if response.content:
                list_errors = [
                    "La località specificata non e' conforme allo stradario Gls.",
                    "L'indirizzo specificato non e'conforme con lo stradario Gls.",
                    "Dati non accettabili: Il peso deve essere maggiore di zero"]
                soup = BeautifulSoup(response.content, 'lxml')
                soup_note_errors = soup.find_all('notespedizione')
                if len(soup_note_errors) > 0 and soup_note_errors[0].text in list_errors:
                    raise UserError(
                        'picking n: ' + pick + ' ' + soup_note_errors[0].text)

    def get_parcel_text(self):
        # not_allowed = ['à', 'è', 'ì', 'ò', 'ù']
        model_tc = self.env['transport.carrier']
        for picking_id in self:
            business_name = model_tc.get_ragione_sociale(picking_id)
            partner_picking = picking_id.partner_id
            if not business_name or not partner_picking.street or not partner_picking.city or not partner_picking.zip:
                message = 'The shipment ' + str(picking_id.name)
                raise UserError(
                    message + ' is missing one of these info: Business name, street, place or zip')
            if partner_picking.country_id.code == 'IT' and not partner_picking.state_id.code:
                raise UserError(
                    'The shipment ' + str(picking_id.name) + ' is missing state ')
            # for char in not_allowed:
            #     if char in business_name or char in partner_picking.street or char in partner_picking.city:
            #         message = 'Shipping ' + str(picking_id.name) + ' :'
            #         raise UserError(message + 'Character not allowed in Business name, street or place')
            picking_id.pricelist_code_gls = model_tc.get_contract_code(picking_id)
            text = ''
            insurance_parcel, cod_parcel = picking_id.get_cod_assurance()
            force_weight = picking_id.check_if_force_weight()
            for lab_line in picking_id.parcel_label_ids:
                text += self.get_data_call_gls(picking_id, lab_line, False, insurance_parcel, cod_parcel, force_weight)
        return text

    def check_if_force_weight(self):
        for picking in self:
            if picking.transport_carrier_id.check_and_force_weight:
                return True
            return False

    def get_cod_assurance(self):
        for picking_id in self:
            insurance_parcel = 0.0
            cod_parcel = 0.0
            if picking_id.parcel_label_ids:
                if picking_id.amount_insurance:
                    insurance_parcel = round(picking_id.amount_insurance / len(picking_id.parcel_label_ids), 2)
                if picking_id.amount_cash_on_delivery:
                    cod_parcel = round(picking_id.amount_cash_on_delivery / len(picking_id.parcel_label_ids), 2)
            return insurance_parcel, cod_parcel

    def get_srv_accessories(self):
        for picking in self:
            services = ''
            if picking.accessories_services_gls:
                index = 1
                for service in picking.accessories_services_gls:
                    services += service.name
                    if index < len(picking.accessories_services_gls):
                        services += ','
                        index += 1
            return services

    def get_date_and_time_note_gdo(self):
        services_accessories = self.accessories_services_gls.mapped('name')
        if self.accessories_services_gls and '34' in services_accessories:
            if not self.date_booking_gdo or not self.time_note_booking_gdo:
                raise UserError('Missing Data GDO for service 34')
            text = """<DataPrenotazioneGDO>%s</DataPrenotazioneGDO>
                                 <OrarioNoteGDO>%s</OrarioNoteGDO>""" % (
                self.date_booking_gdo, self.time_note_booking_gdo)
            return text
        return ''

    def get_tracking(self, tc_shipping_id):
        for picking in self:
            transport_carrier = picking.transport_carrier_id
            if not transport_carrier.start_link or not transport_carrier.end_link:
                raise UserError('In transport Carrier miss start or end link for tracking')
            link = transport_carrier.start_link + str(
                transport_carrier.office_gls) + transport_carrier.end_link + str(
                tc_shipping_id)
            return link

    def get_tracking_ref(self, tc_shipping_id):
        for picking in self:
            transport_carrier = picking.transport_carrier_id
            tracking_ref = str(transport_carrier.office_gls) + str(tc_shipping_id)
            return tracking_ref

    def get_data_call_gls(self, picking_id, lab_line, is_validate, insurance, cod, force_weight):
        model_tc = self.env['transport.carrier']
        partner_picking = picking_id.compute_partner_picking()
        transport_carrier_id = picking_id.transport_carrier_id
        weight_label = lab_line.weight
        if force_weight:
            if weight_label >= transport_carrier_id.check_min_weight and lab_line.weight <= transport_carrier_id.check_max_weight:
                weight_label = transport_carrier_id.force_weight
        text = """<Parcel>
                        <CodiceContrattoGls>%s</CodiceContrattoGls>
                        <RagioneSociale>%s</RagioneSociale>
                        <Indirizzo>%s</Indirizzo>
                        <Localita>%s</Localita>
                        <Zipcode>%s</Zipcode>
                        <Provincia>%s</Provincia>
                        <Bda>%s</Bda>
                        <Colli>1</Colli>
                        <Incoterm>%s</Incoterm>
                        <PesoReale>%s</PesoReale>
                        <ImportoContrassegno>%s</ImportoContrassegno>
                        <NoteSpedizione>%s</NoteSpedizione>
                        <TipoPorto>%s</TipoPorto>
                        <Assicurazione>%s</Assicurazione>
                        <PesoVolume>%s</PesoVolume>
                        <TipoCollo>%s</TipoCollo>
                        <RiferimentoCliente>%s</RiferimentoCliente>
                        <NoteAggiuntive>%s</NoteAggiuntive>
                        <CodiceClienteDestinatario>%s</CodiceClienteDestinatario>
                        <Email>%s</Email>
                        <Cellulare1>%s</Cellulare1>
                        <ServiziAccessori>%s</ServiziAccessori>
                        <ModalitaIncasso>%s</ModalitaIncasso>
                        <GeneraPdf>%s</GeneraPdf>
                        <FormatoPdf>%s</FormatoPdf>
                        <ContatoreProgressivo>%s</ContatoreProgressivo>
                        <AssicurazioneIntegrativa>%s</AssicurazioneIntegrativa>
                        <TipoSpedizione>%s</TipoSpedizione>
                        <ValoreDichiarato></ValoreDichiarato>
                        <PersonaRiferimento>%s</PersonaRiferimento>
                        <IdentPIN>%s</IdentPIN>
                        <Contenuto></Contenuto>
                        <TelefonoDestinatario>%s</TelefonoDestinatario> #TODO per estero
                        <CategoriaMerceologica></CategoriaMerceologica>
                        <FatturaDoganale></FatturaDoganale>
                        <DataFatturaDoganale></DataFatturaDoganale>
                        <PezziDichiarati></PezziDichiarati>
                        <NazioneOrigine></NazioneOrigine>
                        <TelefonoMittente></TelefonoMittente>
                        <NumDayListSped>%s</NumDayListSped>
                        %s
                </Parcel>""" % (model_tc.get_contract_code(picking_id),
                                model_tc.get_ragione_sociale(picking_id),
                                self.get_address_gls(partner_picking),
                                unidecode.unidecode(partner_picking.city),
                                partner_picking.zip,
                                partner_picking.state_id.code if partner_picking.country_id.code == 'IT' else partner_picking.country_id.code,
                                picking_id.id,
                                picking_id.sale_id.incoterm.code_gls if picking_id.sale_id.incoterm.code_gls else '0',
                                weight_label,
                                cod,
                                model_tc.get_note_gls(picking_id, partner_picking),
                                picking_id.tipo_porto.code_gls if picking_id.tipo_porto.code_gls else '',
                                insurance,
                                lab_line.pesovolume,
                                transport_carrier_id.type_package,
                                picking_id.sale_id.client_order_ref if picking_id.sale_id and picking_id.sale_id.client_order_ref else '',
                                model_tc.get_additional_note_gls(picking_id,
                                                                 partner_picking),
                                partner_picking.id,
                                partner_picking.email if partner_picking.email else '',
                                partner_picking.mobile if partner_picking.mobile else '',
                                picking_id.get_srv_accessories(),
                                transport_carrier_id.colletion_mode if transport_carrier_id.colletion_mode else '',
                                transport_carrier_id.generate_pdf,
                                transport_carrier_id.format_pdf if transport_carrier_id.format_pdf else '',
                                lab_line.segnacollo,
                                transport_carrier_id.supplementary_insurance if transport_carrier_id.supplementary_insurance else '',
                                picking_id.get_type_shipping_gls(partner_picking),
                                unidecode.unidecode(partner_picking.name),
                                transport_carrier_id.identpin if transport_carrier_id.identpin else '',
                                partner_picking.phone if partner_picking.phone else '',
                                transport_carrier_id.num_day_list_sped if is_validate else 0,
                                picking_id.get_date_and_time_note_gdo()
                                )
        return text

    def get_address_gls(self, partner_picking):
        if partner_picking:
            address = ''
            if partner_picking.street:
                address += partner_picking.street
            if partner_picking.street2:
                address += '; ' + partner_picking.street2
            return unidecode.unidecode(address[0:35])

    def get_type_shipping_gls(self, partner_picking):
        if partner_picking and partner_picking.country_id:
            if partner_picking.country_id == self.env.company.country_id:
                return 'N'
        return 'P'

    def validate_shipping_gls(self, picking_ids):
        if picking_ids:
            for picking in picking_ids:
                picking.check_various_errors()
            transport_carrier_id = picking_ids[0].transport_carrier_id
            body = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
                                        <Info>
                                            <SedeGls>%s</SedeGls>
                                            <CodiceClienteGls>%s</CodiceClienteGls>
                                            <PasswordClienteGls>%s</PasswordClienteGls>
                                            %s
                                        </Info>
                                        """ % (transport_carrier_id.office_gls,
                                               transport_carrier_id.user,
                                               transport_carrier_id.passwd,
                                               self.get_text_validate_shipping(
                                                   picking_ids),
                                               )
            parcels = {'XMLCloseInfoParcel': body}
            response = requests.post(url_close_work_day, data=parcels, headers={
                'content-type': 'application/x-www-form-urlencoded'})
            error = self.get_error_gls(response)
            if error:
                raise UserError(error)
            self.get_list_sped(picking_ids[0].transport_carrier_id)

    def get_list_sped(self, transport_carrier_id):
        data_gls = {'SedeGls': transport_carrier_id.office_gls,
                    'CodiceClienteGls': transport_carrier_id.user,
                    'PasswordClienteGls': transport_carrier_id.passwd}
        response = requests.post(url_list_sped, data=data_gls, headers={
            'content-type': 'application/x-www-form-urlencoded'})
        self.get_state_gls_picking(response)

    def get_text_validate_shipping(self, picking_ids):
        text = ''
        for picking_id in picking_ids:
            insurance_parcel, cod_parcel = picking_id.get_cod_assurance()
            force_weight = picking_id.check_if_force_weight()
            for lab_line in picking_id.parcel_label_ids:
                text += self.get_data_call_gls(picking_id, lab_line, True, insurance_parcel, cod_parcel, force_weight)
        return text

    def check_various_errors(self):
        for picking in self:
            user_error = False
            if picking.status_shipping_gls == 'closed':
                user_error = _('Select only picking no closed GLS')
            if picking.carrier != 'gls':
                user_error = _('Select only picking with carrier GLS')
            if not picking.picking_type_id.dropshipping:
                if picking.state != 'done':
                    user_error = _('Select only picking done')
            if not picking.parcel_label_ids:
                user_error = ('Select only picking with label received')
            else:
                for label in picking.parcel_label_ids:
                    if not label.parcel_img and not label.parcel_img_zpl:
                        user_error = ('Select only picking with label received')
            if user_error:
                raise UserError(user_error)

    def get_error_gls(self, response):
        if not response.ok:
            if response.status_code == 500:
                return 'Error 500: ' + response.content

    def get_state_gls_picking(self, response):
        soup = BeautifulSoup(response.content, 'lxml')
        soup_parcels = soup.find_all('parcel')
        for element in soup_parcels:
            self.set_state_gls_picking(element)

    def set_state_gls_picking(self, parcel):
        if parcel:
            model_pick = self.env['stock.picking']
            picking = parcel.ddt.text
            if picking:
                picking_id = model_pick.search([('id', '=', picking),
                                                ('carrier', '=', 'gls')])
                if picking_id:
                    state_picking = parcel.find('statospedizione')
                    if state_picking and state_picking.text == 'IN ATTESA DI CHIUSURA.':
                        picking_id.status_shipping_gls = 'pending_closure'
                    if state_picking and state_picking.text == 'CHIUSA.':
                        picking_id.status_shipping_gls = 'closed'
