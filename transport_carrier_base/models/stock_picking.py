# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from .hooks import cleanup_obsolete_views

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round, float_compare


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def init(self):
        super().init()
        cleanup_obsolete_views(self.env)

    number_of_packages = fields.Integer(string='Number of Packages', copy=False)

    transport_carrier_id = fields.Many2one('transport.carrier',
                                           string='Transport Carrier')
    volume = fields.Float('Volume', readonly=True, copy=False, digits=(12, 5))
    pesovolume = fields.Float(string='Pesovolume cm³', copy=False, digits=(12, 5))
    amount_insurance = fields.Float(string='Amount Insurance', copy=False)
    amount_cash_on_delivery = fields.Float(string='Cod Value', copy=False)
    dangerous_goods = fields.Boolean(string='Dangerous Goods', copy=False)
    url_tracking = fields.Char(string='Url Tracking', copy=False)
    last_update_tracking = fields.Char(string='Last update Tracking', copy=False)
    date_last_update = fields.Char(string='Date Last Update', copy=False)
    time_last_update = fields.Char(string='Time Last Update', copy=False)
    error_tracking = fields.Char(string='Error Tracking', copy=False)
    parcel_label_ids = fields.One2many('stock.quant.package', 'picking_id',
                                       string='Parcel Label', copy=False,
                                       domain=[('is_label', '=', True)])
    response_transport_carrier = fields.Text(string='Response Carrier', copy=False)

    carrier_cost = fields.Float(string='Carrier Cost', copy=False, readonly=False)
    carrier_base_cost = fields.Float(string='Carrier Base Cost', copy=False,
                                     readonly=False)

    tipo_porto = fields.Many2one('transport.condition', string='Port type', copy=False)
    body_request_label_transport_carrier = fields.Text(
        string='Body request label Transport Carrier',
        readonly=True, copy=False)
    tc_shipping_id = fields.Char(string='TC Shipping ID', copy=False)

    body_confirm_tc = fields.Text(string='Body Confirm TC', copy=False)
    response_create_shipping_tc = fields.Text(string='Response Create Shipping', copy=False)
    response_confirm_tc = fields.Text(string='Response Confirm', copy=False)
    response_tracking_tc = fields.Text(string='Response Tracking', copy=False)

    deletion_shipping = fields.Boolean(string='Deletion Shipping',
                                       related='transport_carrier_id.deletion_shipping')
    validation_shipping = fields.Boolean(string='Validation Shipping',
                                         related='transport_carrier_id.validation_shipping')
    cancellation_done = fields.Boolean(string='Cancellation Carrier Done', copy=False)
    validation_done = fields.Boolean(string='Validation Carrier Done', copy=False)
    carrier = fields.Selection(related='transport_carrier_id.carrier', string='Carrier')
    error_create_shipping = fields.Boolean('Error Create Shipping', copy=False)

    def process_label(self):
        model_move_line = self.env['stock.move.line']
        for picking in self:
            if picking.parcel_label_ids:
                picking.check_product_weight(picking.transport_carrier_id)
                picking.check_product_volume(picking.transport_carrier_id)
                for label in picking.parcel_label_ids:
                    move_lines_same_package = model_move_line.search(
                        [('picking_id', '=', picking.id),
                         ('result_package_id', '=', label.id)])
                    weight_package = label.package_type_id.base_weight or 0.0
                    for ml in move_lines_same_package:
                        qty = ml.product_uom_id._compute_quantity(ml.quantity,
                                                                  ml.product_id.uom_id)
                        weight_package += qty * ml.product_id.weight
                    volume_package = self.get_volume_package(move_lines_same_package, picking.transport_carrier_id)
                    pesovolume_package = self.get_pesovolume_package(move_lines_same_package, weight_package, volume_package)
                    label_line_vals = {
                                       'shipping_weight': weight_package,
                                       'volume': volume_package,
                                       'pesovolume': pesovolume_package,
                                       }
                    if picking.transport_carrier_id.sequence_id:
                        label_line_vals['segnacollo'] = picking.transport_carrier_id.sequence_id.next_by_id()
                    label.write(label_line_vals)
                    # elif move_line.product_id:
                    #     prod_number_package = move_line.product_id.number_package
                    #     if prod_number_package == 0:
                    #         prod_number_package = 1
                    #     if move_line.quantity:
                    #         move_qty = move_line.quantity
                    #     else:
                    #         continue
                    #     pesovolume = (self.get_volume_weight(move_line.product_id.weight,
                    #                                          move_line.product_id.volume,
                    #                                          picking) * 1000000)
                    #     total_weight_product = move_line.product_id.weight * move_qty
                    #     total_volume_product = move_line.product_id.volume * move_qty
                    #     peso_collo = round(total_weight_product / prod_number_package,2) / move_qty
                    #     volume_collo = round(total_volume_product / prod_number_package,2) / move_qty
                    #     index = 0
                    #     total_pesovolume_product = pesovolume * move_qty
                    #     pesovolume_collo = round(total_pesovolume_product / prod_number_package, 2) / move_qty
                    #     total_number_package = int(move_qty * prod_number_package)
                    #     for product in range(total_number_package):
                    #         index += 1
                    #         if index == total_number_package:
                    #             peso_collo = total_weight_product
                    #             volume_collo = total_volume_product
                    #             pesovolume_collo = total_pesovolume_product
                    #         else:
                    #             total_weight_product -= peso_collo
                    #             total_volume_product -= volume_collo
                    #             total_pesovolume_product -= pesovolume_collo
                    #         label_line_vals = {
                    #                            'weight': peso_collo,
                    #                            'pesovolume': pesovolume_collo,
                    #                            'volume': volume_collo,
                    #                            }
                    #         if picking.transport_carrier_id.sequence_id:
                    #             label_line_vals['segnacollo'] = picking.transport_carrier_id.sequence_id.next_by_id()
                    #         model_picking_label.create(label_line_vals)
                picking.pesovolume = picking.get_pesovolume_shipping()
                picking.volume = picking.get_volume_shipping()
                self.env.cr.commit()

    def compute_partner_picking(self):
        for picking in self:
            partner_picking = picking.partner_id
            recipient_dropshipper = picking.get_partner_dropshipper()
            if recipient_dropshipper:
                partner_picking = recipient_dropshipper
            return partner_picking

    def get_partner_dropshipper(self):
        for picking in self:
            if picking.picking_type_id.dropshipping and picking.sale_id:
                return picking.sale_id.partner_shipping_id
            return False

    def get_shipper_id(self):
        for picking in self:
            if picking.location_id.warehouse_id and picking.location_id.warehouse_id.partner_id:
                shipper_id = picking.location_id.warehouse_id.partner_id
            elif picking.location_id.company_id:
                shipper_id = picking.location_id.company_id.partner_id
            elif picking.company_id:
                shipper_id = picking.company_id.partner_id
            else:
                shipper_id = self.env.company
            return shipper_id

    def get_weight_shipping(self):
        for picking in self:
            return round(sum(picking.parcel_label_ids.mapped('shipping_weight')), 2)

    def get_volume_shipping(self):
        for picking in self:
            return sum(picking.parcel_label_ids.mapped('volume'))

    def get_pesovolume_shipping(self):
        for picking in self:
            return sum(picking.parcel_label_ids.mapped('pesovolume'))

    def get_weight_package(self, package):
        if package:
            weight = 0
            model_move_line = self.env['stock.move.line']
            some_pack_move_line = model_move_line.search(
                [('picking_id', '=', package.picking_id.id),
                 ('result_package_id', '=', package.result_package_id.id)])
            for move_line in some_pack_move_line.filtered(lambda ml: ml.product_id):
                weight_total = move_line.product_id.weight * move_line.quantity
                weight += weight_total
            return weight

    # base method for other module
    def get_pesovolume_package(self, move_lines_same_package, peso_package, volume_package):
        volume_package = (volume_package or 0) * 1000000  # convert m³ to cm³
        pesovolume = self.get_volume_weight(peso_package, volume_package,
                                            move_lines_same_package.picking_id)
        return pesovolume

    def get_volume_weight(self, weight, volume, picking_id):
        transport_carrier_id = picking_id.transport_carrier_id
        if transport_carrier_id:
            if weight > transport_carrier_id.peso_campione:
                divisor = transport_carrier_id.divisor
            else:
                divisor = transport_carrier_id.divisor2
            pesovolume = volume / divisor
            return pesovolume

    def get_volume_package(self, move_lines_package, transport_carrier_id):
        if move_lines_package:
            volume_package = 0
            for move_line in move_lines_package:
                type_pack = move_line.result_package_id.package_type_id #Pack manuale
                default_package_type = transport_carrier_id.default_package_type_id #su setting
                if type_pack and type_pack.id == default_package_type.id:
                    if move_line.product_id:
                        volume_total = move_line.product_id.volume * move_line.quantity
                        volume_package += volume_total
                else:
                    if not type_pack.height or not type_pack.width or not type_pack.packaging_length:
                        raise UserError("You must set dimension in Package type")
                    #TODO #su pack son mm, su pick serve in m³
                    # volume_package = (type_pack.height * type_pack.width * type_pack.packaging_length) * 100 #*100 add in v18. default mm on measure package. In v16 in TC was in cm
                    volume_package = (type_pack.height * type_pack.width * type_pack.packaging_length) / 1000000000 #dai mm del type package a m³ del pick
            return volume_package  # return volume in m³

    # TODO TEST
    def get_number_of_package(self):
        for picking in self:
            number_packages = 0
            move_qty = 0
            packages = []
            for move_line in picking.move_line_ids:
                if not move_line.result_package_id:
                    if move_line.quantity:
                        move_qty = move_line.quantity
                    number_packages += (move_line.product_id.number_package * move_qty)
                    move_qty = 0
                else:
                    if move_line.result_package_id not in packages:
                        packages.append(move_line.result_package_id)
            number_packages += len(packages)
            picking.write({'number_of_packages': number_packages})

    # now, used only for tnt, FedEx, brt
    def check_product_weight(self, transport_carrier_id):
        if transport_carrier_id.check_weight:
            for picking in self:
                product_ids = picking.move_line_ids.mapped('product_id')
                for product in product_ids:
                    if product.weight <= 0:
                        raise UserError(self.env._('Missing Weight on Product ' + picking.name))

    # now, used only for tnt, FedEx, brt
    def check_product_volume(self, transport_carrier_id):
        if transport_carrier_id.check_volume:
            for picking in self:
                product_ids = picking.move_line_ids.mapped('product_id')
                for product in product_ids:
                    if product.volume <= 0:
                        raise UserError(self.env._('Missing Volume on Product ' + picking.name))

    def get_weight_for_carrier(self):
        for picking in self:
            move_qty = 0
            total_weight_for_carrier = 0
            for move_line in picking.move_line_ids:
                if move_line.quantity:
                    move_qty = move_line.quantity
                total_weight_for_carrier += (move_qty * move_line.product_id.weight)
                move_qty = 0
            return total_weight_for_carrier

    def action_carrier(self, picking_ids, create_label, delete_shipping,
                       validate_shipping, get_tracking):
        if picking_ids:
            carrier_list = picking_ids.mapped('transport_carrier_id')
            if len(carrier_list) != 1:
                raise UserError(
                    self.env._("Missing or different Transport Carriers on Selected Pickings"))
            if create_label:
                self.carrier_create_label(picking_ids)
            if delete_shipping:
                self.carrier_delete_shipping(picking_ids)
            if validate_shipping:
                self.carrier_validate_shipping(picking_ids)
            if get_tracking:
                self.carrier_get_tracking_shipping(picking_ids)
            return

    def carrier_create_label(self, picking_ids):
        for picking in picking_ids:
            all_packages = picking.check_all_packages()
            all_labels = picking.check_all_label()
            if all_packages and all_labels:
                continue #se ci sono sia tutti i package che label, solo chiamata corriere
            elif all_packages and not all_labels:
                move_lines_no_label = picking.move_line_ids.filtered(lambda ml: ml.result_package_id and not ml.result_package_id.is_label)
                move_lines_no_label.mapped("result_package_id").write(
                    {
                        "is_label": True,
                        "picking_id": picking.id,
                    }
                ) #Todo test 2 move lines no labels, 2 pack diversi
                picking.process_label()
                continue
            else:
                packages = picking.mapped("move_line_ids.result_package_id")
                move_lines = picking.move_line_ids.filtered(lambda ml: ml.quantity)
                if packages:
                    move_lines = picking.move_line_ids.filtered(
                        lambda ml: not ml.result_package_id and ml.quantity
                    )

                move_line_qty = {
                    move_line: move_line.quantity
                    for move_line in move_lines
                }
                move_lines.write({"quantity": 0})

                for move_line in move_lines:
                    rounding = move_line.product_uom_id.rounding or 0.01
                    qty = float_round(
                        float(move_line_qty[move_line] or 0.0),
                        precision_rounding=rounding
                    )
                    if float_compare(qty, 0.0, precision_rounding=rounding) <= 0:
                        continue

                    if picking.transport_carrier_id.group_into_single_package:
                        move_line.write({"quantity": qty})
                    else:
                        int_qty = int(qty)
                        float_qty = float_round(qty - int_qty, precision_rounding=rounding)

                        if int_qty > 0:
                            move_line.write({"quantity": 1})
                            picking.action_put_in_pack_tc()

                            for _ in range(int_qty - 1):
                                new_ml = move_line.copy(
                                    {
                                        "location_id": move_line.location_id.id,
                                        "location_dest_id": move_line.location_dest_id.id,
                                        "result_package_id": False,
                                        "quantity": 0,
                                        "lot_id": False,
                                        "lot_name": False,
                                    }
                                )
                                new_ml.write({"quantity": 1})
                                picking.action_put_in_pack_tc()

                        if float_compare(float_qty, 0.0, precision_rounding=rounding) > 0:
                            if not int_qty:
                                move_line.write({"quantity": float_qty})
                                picking.action_put_in_pack_tc()
                            else:
                                new_ml = move_line.copy(
                                    {
                                        "location_id": move_line.location_id.id,
                                        "location_dest_id": move_line.location_dest_id.id,
                                        "result_package_id": False,
                                        "quantity": 0,
                                        "lot_id": False,
                                        "lot_name": False,
                                    }
                                )
                                new_ml.write({"quantity": float_qty})
                                picking.action_put_in_pack_tc()

                    self.env.cr.commit()

                if picking.transport_carrier_id.group_into_single_package:
                    picking.action_put_in_pack_tc()

                packages = picking.mapped("move_line_ids.result_package_id")
                default_package_type = picking.transport_carrier_id.default_package_type_id
                if packages:
                    packages.write(
                        {
                            "is_label": True,
                            "picking_id": picking.id,
                            "package_type_id": default_package_type.id,
                        }
                    )

                picking.process_label()
        return

    def check_all_packages(self):
        for picking in self:
            move_line_ids = picking.move_line_ids.filtered(lambda ml: ml.quantity)
            for move_line in move_line_ids:
                if not move_line.result_package_id:
                    return False
            return True

    #Se non ci sono package o se i package non sono label, viene fatto put in pack
    def check_all_label(self):
        for picking in self:
            packages = picking.move_line_ids.mapped('result_package_id')
            for pack in packages:
                if not pack.is_label:
                    return False  #non devo rifare i package ma sono
            return True

    def action_put_in_pack_tc(self):
        for picking in self:
            if not picking.transport_carrier_id.default_package_type_id:
                raise UserError(
                    self.env._('Missing Default Package Type'))
            result = picking.action_put_in_pack()
            if isinstance(result, dict):
                if result.get("res_model") == "choose.delivery.package":
                    package_type = picking.transport_carrier_id.default_package_type_id

                    wizard = (
                        self.env["choose.delivery.package"]
                        .with_context(result.get("context"))
                        .create({"delivery_package_type_id": package_type.id})
                    )
                    wizard.action_put_in_pack()

    def carrier_delete_shipping(self, picking_ids):
        return

    def carrier_validate_shipping(self, picking_ids):
        return

    def carrier_get_tracking_shipping(self, picking_ids):
        return
