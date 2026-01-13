# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, fields, models


class StockQuantPackageInherit(models.Model):
    _inherit = 'stock.quant.package'

    is_label = fields.Boolean(string='Is Label')
    #spostato da parcel label
    picking_id = fields.Many2one('stock.picking', string='Picking',
                                 ondelete='cascade')  # Manca attualmente
    product_id = fields.Many2one('product.product',
                                 readonly=True,
                                 string='Product')
    package_id = fields.Many2one('stock.quant.package', readonly=True,
                                 string='Package')
    # weight = fields.Float(string='Weight Parcel')
    volume = fields.Float(string='Volume Parcel', digits=(12, 5))
    pesovolume = fields.Float(string='Weight Volume Parcel cm³', digits=(12, 5))
    move_line_id = fields.Many2one('stock.move.line')
    parcel_img_zpl = fields.Text(string='Parcel Image Zpl')
    parcel_img = fields.Binary(string='Parcel Image')
    parcel_img2 = fields.Binary(string='Parcel Image 2')
    parcel_img3 = fields.Binary(string='Parcel Image 3')
    parcel_img4 = fields.Binary(string='Parcel Image 4')
    segnacollo = fields.Char(string='Segnacollo')