# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models
import requests
import base64
from bs4 import BeautifulSoup
from odoo.exceptions import UserError
from pdf2image import convert_from_bytes

url_get_pdf = "https://labelservice.gls-italy.com/ilswebservice.asmx/GetPdf"
url_get_zpl = "https://labelservice.gls-italy.com/ilswebservice.asmx/GetZpl"


class ParcelLabelGlsInherit(models.Model):
    _inherit = 'stock.quant.package'

    def get_segnacolli(self, type_parcel):
        model_tc = self.env['transport.carrier']
        label_picking_id = self.picking_id
        transport_carrier_id = label_picking_id.transport_carrier_id
        datas = {'SedeGls': transport_carrier_id.office_gls,
                 'CodiceCliente': transport_carrier_id.user,
                 'Password': transport_carrier_id.passwd,
                 'CodiceContratto': model_tc.get_contract_code(self.picking_id),
                 'ContatoreProgressivo': self.segnacollo}
        if type_parcel == 'pdf':
            response = requests.post(url_get_pdf, data=datas, headers={
                'content-type': 'application/x-www-form-urlencoded'})
            self.get_segnacolli_pdf(response)
        elif type_parcel == 'zpl':
            response = requests.post(url_get_zpl, data=datas, headers={
                'content-type': 'application/x-www-form-urlencoded'})
            self.get_segnacolli_zpl(response)

    def get_segnacolli_pdf(self, response):
        soup = BeautifulSoup(response.content, 'lxml')
        soup_segnacolli = soup.find_all('base64binary')
        gls_data = []
        for element in soup_segnacolli:
            gls_data.append(str(element.text))
        if gls_data and len(gls_data[0]) > 0:
            gls_decode = base64.b64decode(gls_data[0])
            gls_image = convert_from_bytes(gls_decode)
            file_tmp = gls_image[0].save(open("/tmp/gls.jpg", "wb"))
            self.parcel_img = base64.b64encode(open("/tmp/gls.jpg", "rb").read())
        else:
            raise UserWarning('Error!')

    def get_segnacolli_zpl(self, response):
        soup = BeautifulSoup(response.content, 'lxml')
        if response.status_code == 200 and soup.text:
            self.parcel_img_zpl = soup.text
        else:
            raise UserError('Error! No Labels Generated')
