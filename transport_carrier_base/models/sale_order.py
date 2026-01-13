# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models
from odoo.exceptions import UserError

from ..mixins import carrier_checker

transport_carrier = False
delivery_cost = 999999
delivery_cost_efficienty = 999999999

delivery_base_cost = 0


class SaleOrderInherit(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "carrier.checker.mixin"]

    check_street_tc = fields.Selection(selection=[('check_ok', 'Check Street Ok'),
                                                  ('check_ko', 'Check Street KO')],
                                       store=True,
                                       compute='compute_check_street_tc',
                                       string='Check Street')
    force_street_ok = fields.Boolean(string='Force Street Ok')

    @api.depends('transport_carrier_id', 'partner_id.street',
                 'partner_shipping_id.street', 'partner_id.street2',
                 'partner_shipping_id.street2', 'force_street_ok')
    def compute_check_street_tc(self):
        for sale in self:
            partner_id = sale.get_partner_sale()
            if partner_id:
                if sale.force_street_ok:
                    sale.check_street_tc = 'check_ok'
                    continue
                if sale.transport_carrier_id and sale.transport_carrier_id.check_max_char_street > 0:
                    street = partner_id.street
                    if sale.transport_carrier_id.option_check_street == 'street_street2' and street and partner_id.street2:
                        street += ' ' + partner_id.street2
                    if street and len(
                            street) > sale.transport_carrier_id.check_max_char_street:
                        sale.check_street_tc = 'check_ko'
                    else:
                        sale.check_street_tc = 'check_ok'

    transport_carrier_id = fields.Many2one('transport.carrier', copy=False,
                                           string='Transport Carrier')
    carrier_cost = fields.Float(string='Carrier Cost Total', copy=False)
    carrier_base_cost = fields.Float(string='Carrier Base Cost', copy=False)

    def return_amount_cod(self):
        for order in self:
            if order.payment_term_id and order.payment_term_id.cod:
                return order.amount_total

    def street2_in_note(self):
        for order in self:
            if order.partner_shipping_id and order.partner_shipping_id.street2:
                street2 = order.partner_shipping_id.street2.strip()
                if street2.isdigit():
                    new_street = order.partner_shipping_id.street + ' ' + street2
                    order.partner_shipping_id.write({'street': new_street, 'street2': ''})
                if order.note:
                    order.note += ' ' + "\r" + street2
                else:
                    order.note = street2

    def recompute_carrier_on_picking(self, sale, carrier):
        if carrier:
            for order in sale:
                for picking in order.picking_ids:
                    picking.transport_carrier_id = carrier
                    picking.carrier_cost = order.carrier_cost
                    picking.carrier_base_cost = order.carrier_base_cost

    def recompute_carrier_sale(self):
        for sale in self:
            partner = sale.get_partner_sale()
            carrier_id = False
            team_id = False
            if sale.carrier_id:
                carrier_id = sale.carrier_id
            if sale.team_id:
                team_id = sale.team_id
            weight = sale._get_weight(sale)
            volume = sale._get_volume(sale)
            weight_multiply_volume = weight * volume
            price = sale.amount_total
            quantity = sale._get_quantity(sale)
            circumference = 0
            if quantity == 1:
                so_line_id = sale.order_line.filtered(lambda l: l.product_id.type in ('consu', 'product'))
                if so_line_id:
                    circumference = self.compute_circumference(so_line_id.product_id)
            if carrier_id or team_id:
                values = sale.get_carrier(carrier_id, weight, volume,
                                          weight_multiply_volume, price,
                                          quantity, partner, team_id, circumference)
                if values[0] != 999999:
                    sale.write(
                        {'carrier_cost': values[0], 'transport_carrier_id': values[1],
                         'carrier_base_cost': values[2]})
                    self.recompute_carrier_on_picking(sale, values[1])
            global delivery_cost, transport_carrier, delivery_cost_efficienty, delivery_base_cost
            transport_carrier = False
            delivery_cost = 999999
            delivery_base_cost = 0
            delivery_cost_efficienty = 999999999

    def get_partner_sale(self):
        for order in self:
            partner = order.partner_id
            if order.partner_shipping_id:
                partner = order.partner_shipping_id
            return partner

    def action_confirm(self):
        res = super(SaleOrderInherit, self).action_confirm()
        for order in self:
            order.recompute_carrier_sale()
            order.street2_in_note()
        return res

    def compute_expected_number_package(self):
        for sale in self:
            expected_number_package = 0
            for line in sale.order_line:
                expected_number_package += (line.product_id.number_package * line.product_uom_qty)
            return expected_number_package

    @api.onchange('carrier_id', 'partner_id', 'order_line')
    def recompute_transport_carrier_onchange(self):
        if self:
            if self.order_line:
                partner = False
                carrier_id = False
                team_id = False
                if self.partner_id:
                    partner = self.partner_id
                if self.carrier_id:
                    carrier_id = self.carrier_id
                if self.team_id:
                    team_id = self.team_id
                weight = self._get_weight(self)
                volume = self._get_volume(self)
                weight_multiply_volume = weight * volume
                price = self.amount_total
                quantity = self._get_quantity(self)
                circumference = 0
                if quantity == 1:
                    so_line_id = self.order_line.filtered(lambda l: l.product_id.type in ('consu', 'product'))
                    if so_line_id:
                        circumference = self.compute_circumference(so_line_id.product_id)
                if carrier_id or team_id:
                    values = self.get_carrier(carrier_id, weight, volume,
                                              weight_multiply_volume, price,
                                              quantity, partner, team_id, circumference)
                    if values[0] != 999999:
                        self.update(
                            {'carrier_cost': values[0], 'transport_carrier_id': values[1],
                             'carrier_base_cost': values[2]})
                global delivery_cost, transport_carrier, delivery_cost_efficienty
                transport_carrier = False
                delivery_cost = 999999
                delivery_cost_efficienty = 999999999

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        for order in orders:
            if order.order_line:
                partner = False
                team = False
                carrier = False
                if order.partner_id:
                    partner = order.partner_id
                if order.team_id:
                    team = order.team_id
                if order.carrier_id:
                    carrier = order.carrier_id
                weight = self._get_weight(order)
                volume = self._get_volume(order)
                weight_multiply_volume = weight * volume
                price = order.amount_total
                quantity = self._get_quantity(order)

                circumference = 0
                if quantity == 1:
                    so_line_id = order.order_line.filtered(lambda l: l.product_id.type in ('consu', 'product'))
                    if so_line_id:
                        circumference = self.compute_circumference(so_line_id.product_id)
                values = self.get_carrier(carrier, weight, volume,
                                          weight_multiply_volume, price, quantity,
                                          partner, team, circumference)
                if values:
                    if values[0] != 999999:
                        order.write(
                            {'carrier_cost': values[0], 'transport_carrier_id': values[1],
                             'carrier_base_cost': values[2]})
                global delivery_cost, transport_carrier, delivery_cost_efficienty, delivery_base_cost
                transport_carrier = False
                delivery_cost = 999999
                delivery_cost_efficienty = 999999999
                delivery_base_cost = 0
        return orders

    def compute_circumference(self, product_id):
        circumference = (product_id.product_length * 2) + (product_id.product_width * 2) + product_id.product_height
        return circumference

    def get_carrier(self, carrier, weight, volume, weight_multiply_volume,
                    price, quantity, partner, team, circumference):
        expected_number_package = self.compute_expected_number_package()
        if carrier or team:
            transport_carrier_model = self.env['transport.carrier']
            carrier_list = []
            transport_carrier_list = transport_carrier_model.search(
                [('parent_id', '=', False),
                 ('max_parcel', '>=', expected_number_package)])
            if quantity == 1:
                transport_carrier_list = self.check_max_circumference(transport_carrier_list, circumference)
            if carrier:
                for t_carrier in transport_carrier_list:
                    if carrier in t_carrier.delivery_carrier_ids:
                        carrier_list.append(t_carrier)
            if transport_carrier_list:
                if len(carrier_list) == 0 and team:
                    for t_carrier in transport_carrier_list:
                        if team in t_carrier.team_ids:
                            carrier_list.append(t_carrier)
            if len(carrier_list) > 0:
                self.check_zip_city_nation(carrier_list, weight,
                                           volume, weight_multiply_volume,
                                           price, quantity, partner)
            return delivery_cost, transport_carrier, delivery_base_cost

    def check_max_circumference(self, transport_carrier_list, circumference):
        if transport_carrier_list:
            new_transport_carrier_list = []
            for transport_carrier in transport_carrier_list:
                if not transport_carrier.max_circumference:
                    new_transport_carrier_list.append(transport_carrier)
                else:
                    if circumference > transport_carrier.max_circumference:
                        pass
                    else:
                        new_transport_carrier_list.append(transport_carrier)
            return new_transport_carrier_list

    def check_zip_city_nation(self, carrier_list, weight, volume,
                              weight_multiply_volume,
                              price, quantity, partner):
        # tc = transport_carrier
        # con il break, alla prima regola che trovo, calcolo costo del corriere successivo
        for tc in carrier_list:
            check = False
            # partner_country = partner.country_id
            # if not partner_country:
            #     raise UserError('Set Country in Partner')
            if tc.destination_type == 'multi':  # se TC è multidestionation
                for subcarrier in tc.child_ids:
                    if not subcarrier.warehouse_id or (subcarrier.warehouse_id and subcarrier.warehouse_id.id == self.warehouse_id.id):
                        zip = False
                        # if (subcarrier.zip_from or subcarrier.zip_to) and partner_country.id in subcarrier.country_ids.ids:
                        if subcarrier.zip_from or subcarrier.zip_to:
                            zip = self.check_zip(partner, subcarrier.zip_from,
                                                 subcarrier.zip_to)
                        if zip:
                            if subcarrier.delivery_type == 'fixed':  # se la prima destin. ha prezzo fisso
                                self.select_carrier(subcarrier, subcarrier.fixed_price,
                                                    tc.efficienty)
                                check = True
                                break
                            else:  # se invece ha prezzo su regole
                                self.check_price_rule(tc, subcarrier, weight, volume,
                                                      weight_multiply_volume, price, quantity)
                                check = True
                                break
                if check:
                    continue
                for subcarrier in tc.child_ids:
                    if not subcarrier.warehouse_id or (
                            subcarrier.warehouse_id and subcarrier.warehouse_id.id == self.warehouse_id.id):
                        if (
                                subcarrier.state_ids and not subcarrier.zip_to and not subcarrier.zip_from):
                            city = self.check_city(partner, subcarrier.state_ids)
                            if city:
                                if subcarrier.delivery_type == 'fixed':  # se la prima destin. ha prezzo fisso
                                    self.select_carrier(subcarrier, subcarrier.fixed_price,
                                                        tc.efficienty)
                                    check = True
                                    break
                                else:
                                    self.check_price_rule(tc, subcarrier, weight, volume,
                                                          weight_multiply_volume, price,
                                                          quantity)
                                    check = True
                                    break
                if check:
                    continue
                for subcarrier in tc.child_ids:
                    if not subcarrier.warehouse_id or (
                            subcarrier.warehouse_id and subcarrier.warehouse_id.id == self.warehouse_id.id):
                        if (
                                subcarrier.country_ids and not subcarrier.state_ids and not subcarrier.zip_to and not subcarrier.zip_from):
                            nation = self.check_nation(partner, subcarrier.country_ids)
                            if nation:
                                if subcarrier.delivery_type == 'fixed':  # se la prima destin. ha prezzo fisso
                                    self.select_carrier(subcarrier, subcarrier.fixed_price,
                                                        tc.efficienty)
                                    check = True
                                    break
                                else:
                                    self.check_price_rule(tc, subcarrier, weight, volume,
                                                          weight_multiply_volume, price,
                                                          quantity)
                                    check = True
                                    break
                if check:
                    continue
            else:
                if not tc.warehouse_id or (tc.warehouse_id and tc.warehouse_id.id == self.warehouse_id.id):
                    zip = False
                    # if tc.zip_from or tc.zip_to and partner_country.id in tc.country_ids.ids:
                    if tc.zip_from or tc.zip_to:
                        zip = self.check_zip(partner, tc.zip_from, tc.zip_to)
                        if zip:
                            if tc.delivery_type == 'fixed':  # se tc ha prezzo fisso
                                self.select_carrier(tc, tc.fixed_price, tc.efficienty)
                                continue
                            else:
                                self.check_price_rule(tc, tc, weight, volume,
                                                      weight_multiply_volume, price, quantity)
                                continue
                    if check:
                        continue
                    if (tc.state_ids and not tc.zip_to and not tc.zip_from):
                        city = self.check_city(partner, tc.state_ids)
                        if city:
                            if tc.delivery_type == 'fixed':  # se la prima destin. ha prezzo fisso
                                self.select_carrier(tc, tc.fixed_price,
                                                    tc.efficienty)
                                continue
                            else:
                                self.check_price_rule(tc, tc, weight,
                                                      volume,
                                                      weight_multiply_volume,
                                                      price, quantity)
                                continue
                    if (
                            tc.country_ids and not tc.state_ids and not tc.zip_to and not tc.zip_from):
                        nation = self.check_nation(partner, tc.country_ids)
                        if nation:
                            if tc.delivery_type == 'fixed':  # se la prima destin. ha prezzo fisso
                                self.select_carrier(tc, tc.fixed_price, tc.efficienty)
                                continue
                            else:
                                self.check_price_rule(tc, tc, weight, volume,
                                                      weight_multiply_volume, price, quantity)
                                continue
                if check:
                    continue

    def get_greater_between_weight_and_volumeweight(self, tc, weight, volume):
        divisor = self.get_divisor(tc, weight)
        if not divisor:
            raise UserError('Set divisor on Transport Carrier')
        weightvolume = (volume / divisor) * 1000000  # TODO TESTING vol * 1000000
        greater_weight_and_weightvolume = self.set_greater_weight_and_weightvolume(weight,
                                                                                   weightvolume)
        return greater_weight_and_weightvolume

    def set_greater_weight_and_weightvolume(self, weight, weightvolume):
        if weightvolume > weight:
            return weightvolume
        else:
            return weight

    def check_price_rule(self, tc, subcarrier, weight, volume,
                         weight_multiply_volume, price, quantity):
        greater_weight_and_weightvolume = self.get_greater_between_weight_and_volumeweight(
            tc, weight, volume)
        price_dict = {'price': price, 'volume': volume, 'weight': weight,
                      'wv': volume * weight, 'quantity': quantity,
                      'greater_weight_and_weightvolume': greater_weight_and_weightvolume}
        for rule in subcarrier.price_rule_ids:
            if rule and rule.variable and rule.operator:
                operator = rule.operator
                max_value = rule.max_value
                if rule.variable == 'weight':
                    formula = str(weight) + operator + str(max_value)
                    self.try_formula_and_select_carrier(formula, tc, rule, price_dict)
                elif rule.variable == 'volume':
                    formula = str(volume) + operator + str(max_value)
                    self.try_formula_and_select_carrier(formula, tc, rule, price_dict)
                elif rule.variable == 'wv':
                    formula = str(weight_multiply_volume) + operator + str(max_value)
                    self.try_formula_and_select_carrier(formula, tc, rule, price_dict)
                elif rule.variable == 'price':
                    formula = str(price) + operator + str(max_value)
                    self.try_formula_and_select_carrier(formula, tc, rule, price_dict)
                elif rule.variable == 'quantity':
                    formula = str(quantity) + operator + str(max_value)
                    self.try_formula_and_select_carrier(formula, tc, rule, price_dict)
                elif rule.variable == 'greater_weight_and_weightvolume':
                    formula = str(greater_weight_and_weightvolume) + operator + str(
                        max_value)
                    self.try_formula_and_select_carrier(formula, tc, rule, price_dict)
        return False

    def try_formula_and_select_carrier(self, formula, tc, rule, price_dict):
        if eval(formula) is True:
            efficienty = tc.efficienty
            cost = rule.list_base_price + rule.list_price * price_dict[
                rule.variable_factor]
            self.select_carrier(tc, cost, efficienty)
            return True

    def get_divisor(self, tc, weight):
        if weight > tc.peso_campione:
            divisor = tc.divisor
        else:
            divisor = tc.divisor2
        return divisor

    def check_zip(self, partner, zip_from, zip_to):
        if partner and partner.zip:
            if zip_from and zip_to:
                if partner.zip > zip_from and partner.zip < zip_to:
                    return True
            if zip_from:
                if partner.zip == zip_from:
                    return True
            if zip_to:
                if partner.zip == zip_to:
                    return True
        return False

    def check_city(self, partner, cities):
        if partner and partner.state_id:
            if cities:
                if partner.state_id in cities:
                    return True
        return False

    def check_nation(self, partner, nations):
        if partner and partner.country_id:
            if nations:
                if partner.country_id in nations:
                    return True
        return False

    def select_carrier(self, tc, cost, efficienty):
        global delivery_cost, transport_carrier, delivery_cost_efficienty, delivery_base_cost
        transport_carrier_id = tc
        old_cost = cost
        cost_extra_product = 0
        extra_percent = 0
        extra_fix = 0
        if transport_carrier_id.extra_ids:
            cost_extra_product = self.get_product_extra(transport_carrier_id.extra_ids)
        new_cost = cost + cost_extra_product
        if transport_carrier_id.extra_percent:
            extra_percent = (new_cost * transport_carrier_id.extra_percent) / 100
        if transport_carrier_id.extra_fix:
            extra_fix = transport_carrier_id.extra_fix
        cost = new_cost + extra_percent + extra_fix
        value = efficienty * cost
        if value < delivery_cost_efficienty:
            delivery_cost = cost
            if tc.parent_id:
                tc = tc.parent_id
            transport_carrier = tc.id
            delivery_cost_efficienty = value
            delivery_base_cost = old_cost

    def _get_weight(self, res):
        for sale in res:
            weight_order = 0
            for line in sale.order_line:
                weight_order += (line.product_id.weight * line.product_uom_qty)
            return weight_order

    def _get_volume(self, res):
        for sale in res:
            volume = 0
            for line in sale.order_line:
                volume += (line.product_id.volume * line.product_uom_qty)
            return volume

    def _get_quantity(self, res):
        for sale in res:
            total_quantity = 0
            for line in sale.order_line:
                if not line.product_id or line.product_id and line.product_id.type != 'service':
                    total_quantity += line.product_uom_qty
            return total_quantity

    def get_product_extra(self, product_extra_cost):
        product_extra = 0
        for sale in self:
            for line in sale.order_line:
                for extra_line in product_extra_cost:
                    if line.product_id == extra_line.product_id:
                        product_extra += (extra_line.extra_cost * line.product_uom_qty)
        return product_extra

    def recompute_carrier_new(self):
        for sale in self:
            partner = sale.partner_id if sale.partner_id else False
            team = sale.team_id if sale.team_id else False
            carrier = sale.carrier_id if sale.carrier_id else False

            info_products = {
                order_line.product_id: {
                    "quantity": order_line.product_uom_qty,
                    "price": order_line.price_total,
                }
                for order_line in sale.order_line
            }
            values = sale.new_compute_carrier_cost(
                carrier, partner, info_products=info_products, sale_team=team
            )
            if values:
                if values[0] != 999999:
                    sale.write(
                        {
                            "carrier_cost": values[0],
                            "transport_carrier_id": values[1],
                            "carrier_base_cost": values[2],
                        }
                    )
            carrier_checker.global_transport_carrier = False
            carrier_checker.global_carrier_cost = 999999
            carrier_checker.global_carrier_cost_efficienty = 999999999
            carrier_checker.global_carrier_base_cost = 0


class ChooseDeliveryCarrierInherit(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    def button_confirm(self):
        res = super(ChooseDeliveryCarrierInherit, self).button_confirm()
        self.order_id.recompute_carrier_sale()
        return res
