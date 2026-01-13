# -*- coding: utf-8 -*-
# Copyright (C) 2024-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso (gborruso@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import _, api, models
from odoo.exceptions import UserError

global_transport_carrier = False
global_carrier_cost = 999999
global_carrier_cost_efficienty = 999999999
global_carrier_base_cost = 0


class CarrierCheckerMixin(models.AbstractModel):
    _name = "carrier.checker.mixin"
    _description = "Carrier Checker Mixin"

    @api.model
    def new_compute_total_weight(self, info_products, info_packages):
        total_weight = 0.0

        if info_products:
            total_weight += sum(
                product.weight * value.get("quantity", 1.0)
                for product, value in info_products.items()
            )
        if info_packages:
            total_weight += sum(
                package.weight * value.get("quantity", 1.0)
                for package, value in info_packages.items()
            )
        return total_weight

    @api.model
    def new_compute_total_volume(self, info_products, info_packages):
        total_volume = 0.0

        if info_products:
            total_volume += sum(
                product.volume * value.get("quantity", 1.0)
                for product, value in info_products.items()
            )
        if info_packages:
            total_volume += sum(
                value.get("volume", 1.0)
                for _, value in info_packages.items()
            )
        return total_volume

    @api.model
    def new_compute_total_package(self, info_products, info_packages):
        total_package = 0.0

        if info_products:
            total_package += sum(
                product.number_package * value.get("quantity", 1.0)
                for product, value in info_products.items()
            )
        if info_packages:
            total_package += sum(
                value.get("quantity", 1.0)
                for _, value in info_packages.items()
            )
        return total_package

    @api.model
    def new_compute_total_quantity(self, info_products, info_packages):
        total_quantity = 0.0
        if info_products:
            total_quantity += sum(
                value.get("quantity", 1.0)
                for _, value in info_products.items()
            )
        if info_packages:
            total_quantity += sum(
                value.get("quantity", 1.0)
                for _, value in info_packages.items()
            )
        return total_quantity

    @api.model
    def new_compute_total_price(self, info_products, info_packages):
        total_price = 0.0

        if info_products:
            total_price += sum(
                value.get("price", 0.0)
                for _, value in info_products.items()
            )
        if info_packages:
            total_price += sum(
                value.get("price", 0.0)
                for _, value in info_packages.items()
            )
        return total_price

    @api.model
    def new_compute_max_circumference(self, info_products, info_packages):
        max_circumference_products = 0.0
        max_circumference_packages = 0.0

        if info_products:
            max_circumference_products = max(
                (product.product_length * 2)
                + (product.product_width * 2)
                + product.product_height
                for product in info_products.keys()
                if product.detailed_type in ("consu", "product")
            )
        if info_packages:
            max_circumference_packages = max(
                (package.package_type_id.packaging_length * 2)
                + (package.package_type_id.width * 2)
                + package.package_type_id.height
                for package in info_packages.keys()
            )
        return max(max_circumference_products, max_circumference_packages)

    @api.model
    def new_compute_extra_product(self, transport_carrier, info_products, info_packages):
        cost_extra_product = 0.0

        if info_products:
            for product, value in info_products.items():
                for extra_line in transport_carrier.extra_ids:
                    if product.id == extra_line.product_id.id:
                        cost_extra_product += (
                            extra_line.extra_cost
                            * value.get("quantity", 1.0)
                        )
        if info_packages:
            for package, value in info_packages.items():
                for product in package.mapped("quant_ids.product_id"):
                    for extra_line in transport_carrier.extra_ids:
                        if product.id == extra_line.product_id.id:
                            cost_extra_product += (
                                extra_line.extra_cost
                                * value.get("quantity", 1.0)
                            )
        return cost_extra_product

    @api.model
    def new_compute_extra_percent(self, transport_carrier, cost):
        extra_percent = 0.0
        if transport_carrier.extra_percent:
            extra_percent = (cost * transport_carrier.extra_percent) / 100
        return extra_percent

    @api.model
    def new_compute_extra_fix(self, transport_carrier):
        extra_fix = 0.0
        if transport_carrier.extra_fix:
            extra_fix = transport_carrier.extra_fix
        return extra_fix

    @api.model
    def new_compute_divisor(self, transport_carrier, weight):
        if weight > transport_carrier.peso_campione:
            divisor = transport_carrier.divisor
        else:
            divisor = transport_carrier.divisor2
        return divisor

    @api.model
    def new_compute_greater_weight_and_weightvolume(self, weight, weightvolume):
        if weightvolume > weight:
            return weightvolume
        else:
            return weight

    @api.model
    def new_compute_greater_between_weight_and_volumeweight(self, transport_carrier, weight, volume):
        divisor = self.new_compute_divisor(transport_carrier, weight)
        if not divisor:
            raise UserError(
                _("Set divisor on transport carrier: %s" % transport_carrier.display_name)
            )
        weightvolume = (volume / divisor) * 1000000  # TODO TESTING vol * 1000000
        greater_weight_and_weightvolume = self.new_compute_greater_weight_and_weightvolume(weight, weightvolume)
        return greater_weight_and_weightvolume

    @api.model
    def new_check_max_circumference(self, all_transport_carriers, max_circumference):
        if all_transport_carriers:
            available_transport_carriers = self.env["transport.carrier"]
            for transport_carrier in all_transport_carriers:
                if (
                    not transport_carrier.max_circumference
                    or (transport_carrier.max_circumference >= max_circumference)
                ):
                    available_transport_carriers |= transport_carrier
            return available_transport_carriers

    @api.model
    def new_compute_available_transport_carriers(
        self, carrier=None, info_products=None, info_packages=None, sale_team=None, force_carriers=False
    ):
        available_transport_carriers = self.env["transport.carrier"]
        number_package = self.new_compute_total_package(info_products, info_packages)
        quantity = self.new_compute_total_quantity(info_products, info_packages)
        max_circumference = self.new_compute_max_circumference(info_products, info_packages)

        all_transport_carriers = self.env["transport.carrier"].search([
            ("parent_id", "=", False),
            ("max_parcel", ">=", number_package),
        ])
        if quantity == 1:  # TODO: se maggiore di 1 non faccio il check?
            all_transport_carriers = (
                self.new_check_max_circumference(all_transport_carriers, max_circumference)
            )
        if carrier or sale_team:
            if carrier:
                for transport_carrier in all_transport_carriers:
                    if carrier in transport_carrier.delivery_carrier_ids:
                        available_transport_carriers |= transport_carrier
            if (
                not available_transport_carriers
                and all_transport_carriers
                and sale_team
            ):
                for transport_carrier in all_transport_carriers:
                    if sale_team in transport_carrier.team_ids:
                        available_transport_carriers |= transport_carrier
        elif force_carriers:
            available_transport_carriers = all_transport_carriers
        return available_transport_carriers

    @api.model
    def new_check_partner_country(self, partner):
        if not partner.country_id:
            raise UserError(_("Set country in partner"))

    @api.model
    def new_check_carrier_cost(self, transport_carrier, cost, efficienty, info_products, info_packages):
        global global_carrier_cost, global_transport_carrier, global_carrier_cost_efficienty, global_carrier_base_cost
        old_cost = cost
        cost_extra_product = self.new_compute_extra_product(transport_carrier, info_products, info_packages)
        new_cost = cost + cost_extra_product
        extra_percent = self.new_compute_extra_percent(transport_carrier, new_cost)
        extra_fix = self.new_compute_extra_fix(transport_carrier)
        cost = new_cost + extra_percent + extra_fix
        value = efficienty * cost
        if value < global_carrier_cost_efficienty:
            global_carrier_cost = cost
            global_transport_carrier = (
                transport_carrier.parent_id.id
                if transport_carrier.parent_id
                else transport_carrier.id
            )
            global_carrier_cost_efficienty = value
            global_carrier_base_cost = old_cost

    @api.model
    def new_try_formula_and_check_carrier_cost(
        self, formula, transport_carrier, rule, price_dict, info_products, info_packages
    ):
        if eval(formula) is True:
            efficienty = transport_carrier.efficienty
            cost = rule.list_base_price + rule.list_price * price_dict[rule.variable]
            self.new_check_carrier_cost(
                transport_carrier, cost, efficienty, info_products, info_packages
            )
            return True
        return False

    @api.model
    def new_check_carrier_rule(self, transport_carrier, info_products, info_packages):
        transport_carrier_parent = (
            transport_carrier.parent_id
            if transport_carrier.parent_id
            else transport_carrier
        )
        weight = self.new_compute_total_weight(info_products, info_packages)
        volume = self.new_compute_total_volume(info_products, info_packages)
        weight_multiply_volume = weight * volume
        quantity = self.new_compute_total_quantity(info_products, info_packages)
        price = self.new_compute_total_price(info_products, info_packages)
        greater_weight_and_weightvolume = (
            self.new_compute_greater_between_weight_and_volumeweight(transport_carrier_parent, weight, volume)
        )
        price_dict = {
            "price": price,
            "volume": volume,
            "weight": weight,
            "wv": volume * weight,
            "quantity": quantity,
            "greater_weight_and_weightvolume": greater_weight_and_weightvolume,
        }

        for rule in transport_carrier.price_rule_ids:
            if rule and rule.variable and rule.operator:
                operator = rule.operator
                max_value = rule.max_value
                if rule.variable == "weight":
                    formula = str(weight) + operator + str(max_value)
                    if self.new_try_formula_and_check_carrier_cost(
                        formula,
                        transport_carrier_parent,
                        rule,
                        price_dict,
                        info_products,
                        info_packages
                    ):
                        return True
                elif rule.variable == "volume":
                    formula = str(volume) + operator + str(max_value)
                    if self.new_try_formula_and_check_carrier_cost(
                        formula,
                        transport_carrier_parent,
                        rule,
                        price_dict,
                        info_products,
                        info_packages
                    ):
                        return True
                elif rule.variable == "wv":
                    formula = str(weight_multiply_volume) + operator + str(max_value)
                    if self.new_try_formula_and_check_carrier_cost(
                        formula,
                        transport_carrier_parent,
                        rule,
                        price_dict,
                        info_products,
                        info_packages
                    ):
                        return True
                elif rule.variable == "price":
                    formula = str(price) + operator + str(max_value)
                    if self.new_try_formula_and_check_carrier_cost(
                        formula,
                        transport_carrier_parent,
                        rule,
                        price_dict,
                        info_products,
                        info_packages
                    ):
                        return True
                elif rule.variable == "quantity":
                    formula = str(quantity) + operator + str(max_value)
                    if self.new_try_formula_and_check_carrier_cost(
                        formula,
                        transport_carrier_parent,
                        rule,
                        price_dict,
                        info_products,
                        info_packages
                    ):
                        return True
                elif rule.variable == "greater_weight_and_weightvolume":
                    formula = str(greater_weight_and_weightvolume) + operator + str(max_value)
                    if self.new_try_formula_and_check_carrier_cost(
                        formula,
                        transport_carrier_parent,
                        rule,
                        price_dict,
                        info_products,
                        info_packages
                    ):
                        return True
        return False

    @api.model
    def new_check_partner_zip(self, transport_carrier, partner):
        zip_from = transport_carrier.zip_from
        zip_to = transport_carrier.zip_to

        if partner and partner.zip:
            if (
                zip_from
                and zip_to
                and zip_from < partner.zip < zip_to
            ):
                return True
            if zip_from and partner.zip == zip_from:
                return True
            if zip_to and partner.zip == zip_to:
                return True
        return False

    @api.model
    def new_check_carrier_zip(self, transport_carrier, partner, info_products, info_packages):
        if (
            (transport_carrier.zip_from or transport_carrier.zip_to)
            and self.new_check_partner_zip(transport_carrier, partner)
        ):
            if transport_carrier.delivery_type == "fixed":
                self.new_check_carrier_cost(
                    transport_carrier,
                    transport_carrier.fixed_price,
                    transport_carrier.efficienty,
                    info_products,
                    info_packages,
                )
                return True
            else:
                self.new_check_carrier_rule(transport_carrier, info_products, info_packages)
                return True
        return False

    @api.model
    def new_check_partner_city(self, partner, states_to_check):
        if (
            partner
            and partner.state_id
            and states_to_check
            and partner.state_id in states_to_check
        ):
            return True
        return False

    @api.model
    def new_check_carrier_city(self, transport_carrier, partner, info_products, info_packages):
        state_ids = transport_carrier.state_ids
        zip_to = transport_carrier.zip_to
        zip_from = transport_carrier.zip_from
        if (
            state_ids
            and not zip_to
            and not zip_from
            and self.new_check_partner_city(partner, state_ids)
        ):
            if transport_carrier.delivery_type == "fixed":
                self.new_check_carrier_cost(
                    transport_carrier,
                    transport_carrier.fixed_price,
                    transport_carrier.efficienty,
                    info_products,
                    info_packages,
                )
                return True
            else:
                self.new_check_carrier_rule(transport_carrier, info_products, info_packages)
                return True
        return False

    @api.model
    def new_check_partner_nation(self, partner, nations_to_check):
        if (
            partner
            and partner.country_id
            and nations_to_check
            and partner.country_id in nations_to_check
        ):
            return True
        return False

    @api.model
    def new_check_carrier_nation(self, transport_carrier, partner, info_products, info_packages):
        country_ids = transport_carrier.country_ids
        state_ids = transport_carrier.state_ids
        zip_to = transport_carrier.zip_to
        zip_from = transport_carrier.zip_from
        if (
            country_ids
            and not state_ids
            and not zip_to
            and not zip_from
            and self.new_check_partner_nation(partner, country_ids)
        ):
            if transport_carrier.delivery_type == "fixed":
                self.new_check_carrier_cost(
                    transport_carrier,
                    transport_carrier.fixed_price,
                    transport_carrier.efficienty,
                    info_products,
                    info_packages,
                )
                return True
            else:
                self.new_check_carrier_rule(transport_carrier, info_products, info_packages)
                return True
        return False

    def check_warehouse_child_and_so(self, transport_carrier_child):
        if 'warehouse_id' in self.fields_get():
            if transport_carrier_child.warehouse_id:
                if transport_carrier_child.warehouse_id.id == self.warehouse_id.id:
                    return True
                return False
        return True

    @api.model
    def new_compute_carrier_cost_rule(self, transport_carriers, partner, info_products, info_packages):
        for transport_carrier in transport_carriers:
            check = False
            # self.check_partner_country(partner)
            if transport_carrier.destination_type == "multi":
                for mode in ["zip", "city", "nation"]:
                    for transport_carrier_child in transport_carrier.child_ids:
                        if not transport_carrier_child.warehouse_id or self.check_warehouse_child_and_so(transport_carrier_child):
                            function_name = "new_check_carrier_" + mode
                            check = getattr(self, function_name, None)(
                                transport_carrier_child, partner, info_products, info_packages
                            )
                            if check:
                                break
                    if check:
                        break
            else:
                for mode in ["zip", "city", "nation"]:
                    function_name = "new_check_carrier_" + mode
                    check = getattr(self, function_name, None)(
                        transport_carrier, partner, info_products, info_packages
                    )
                    if check:
                        break

    @api.model
    def new_compute_carrier_cost(
        self, carrier, partner, info_products=None, info_packages=None, sale_team=None, force_carriers=False
    ):
        available_transport_carriers = (
            self.new_compute_available_transport_carriers(
                carrier, info_products, info_packages, sale_team, force_carriers
            )
        )
        if available_transport_carriers:
            self.new_compute_carrier_cost_rule(
                available_transport_carriers, partner, info_products, info_packages
            )
        return global_carrier_cost, global_transport_carrier, global_carrier_base_cost
