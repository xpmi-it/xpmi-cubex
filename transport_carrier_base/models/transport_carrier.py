# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import unidecode


class TransportCarrier(models.Model):
    _name = 'transport.carrier'
    _description = 'Transport Carrier'

    name = fields.Char(string='Name Carrier', required=True)
    carrier = fields.Selection([], string='Carrier')
    sequence_id = fields.Many2one('ir.sequence', string='Sequence Parcel')
    # info connection
    user = fields.Char(string='User')
    passwd = fields.Char(string='Password')
    # info tracking
    start_link = fields.Char(string='Start Link')
    end_link = fields.Char(string='End Link')
    # function
    check_weight = fields.Boolean(string='Check if Weight greater than 0',
                                  help='If checked, before prepare parcel, '
                                       'check if weight of all product is greater than 0')
    check_volume = fields.Boolean(string='Check Volume greater than 0',
                                  help='If checked, before prepare parcel, '
                                       'check if volume of all product is '
                                       'greater than 0')
    volume_conversion = fields.Integer(string='Value Conversion Volume',
                                       default=1,
                                       help='Value for conversion volume from '
                                            'UOM product and UOM for transport carrier')

    # DR
    # campi del multi destination
    child_ids = fields.One2many(comodel_name="transport.carrier",
                                inverse_name="parent_id", string="Destination grid")
    parent_id = fields.Many2one(comodel_name="transport.carrier", string="Parent carrier")
    destination_type = fields.Selection(selection=[('one', 'One destination'),
                                                   ('multi', 'Multiple destinations')],
                                        default="one", required=True)

    peso_campione = fields.Float()
    divisor = fields.Float(string='Divisor', digits=(16, 3))
    divisor2 = fields.Float(string='Divisor2', digits=(16, 3))
    extra_percent = fields.Float(string='Extra Percent')
    extra_fix = fields.Float(
        string='Extra Fix')  # tipo calcolo efficienty  per scelta corriere
    extra_ids = fields.One2many('delivery.product.extra', 'transport_carrier_id',
                                string='Product Extra')
    efficienty = fields.Float(string='Efficienty Carrier', default=1)
    delivery_carrier_ids = fields.Many2many('delivery.carrier', string='Delivery Carrier')
    team_ids = fields.Many2many('crm.team', string='Sales Team')
    sequence = fields.Integer(help="Determine the display order", default=10)
    delivery_type = fields.Selection(
        [('fixed', 'Fixed Price'), ('base_on_rule', 'Based on Rules')],
        string='Pricing', default='fixed', required=True)
    warehouse_id = fields.Many2one('stock.warehouse')
    country_ids = fields.Many2many('res.country', string='Countries')
    state_ids = fields.Many2many('res.country.state', string='States')
    zip_from = fields.Char('Zip From')
    zip_to = fields.Char('Zip To')
    price_rule_ids = fields.One2many('delivery.price.rule', 'transport_carrier_id',
                                     'Pricing Rules', copy=True)
    fixed_price = fields.Float(string='Fixed Price')
    max_parcel = fields.Integer(string='Max Parcel for Shipping', default=10000)
    check_max_char_street = fields.Integer(string="Max Char Street for Check",
                                           help="If you set 35 on this field, "
                                                "if street partner in "
                                                "picking(with this TC)"
                                                "is longer than 35 char, we set "
                                                "'Check KO' on picking, else 'Check OK'")
    option_check_street = fields.Selection(selection=[('street', 'Street'),
                                                      ('street_street2',
                                                       'Street and Street2')],
                                           default="street")

    check_and_force_weight = fields.Boolean(string='Check and Force Weight',
                                            help='Check and force '
                                                 'weight if weight is between '
                                                 'Check Min Weight amd Check Max Weight.'
                                                 'This control varies from carrier to carrier. At moment, '
                                                 'check is present for GLS, BRT and DHL.'
                                                 'Some carrier (like BRT) want the total weight of the shipment, '
                                                 'so the check will be made on the total weight of the shipment.'
                                                 'Other couriers however (e.g. GLS) receive the weight detail '
                                                 'per parcel, so in this case the weight control and forcing '
                                                 'takes place on each individual parcel.')
    check_min_weight = fields.Float(string='Check Min Weight')
    check_max_weight = fields.Float(string='Check Max Weight')
    force_weight = fields.Float(string='Force Weight')
    max_circumference = fields.Integer(string='Max Circumference (cm)',
                                       help='Set this field only if you want '
                                            'check circumference(shipping with 1 parcel).'
                                            'Total circumference is computed by:'
                                            '(Parcel Lenght * 2) + '
                                            '(Parcel Widht * 2) + Parcel Height.'
                                            'You should enter the UOM in cm for product measurements.')
    picking_in_note = fields.Boolean(string='Name Picking in Note Shipping')
    deletion_shipping = fields.Boolean(string='Deletion Shipping',
                                       help='Not All Carrier Allow Deletion')
    validation_shipping = fields.Boolean(string='Validation Shipping',
                                         help='Not All Carrier Allow Validation')
    default_package_type_id = fields.Many2one('stock.package.type',
                                              string='Default Package Type',
                                              help='This package type will be used '
                                                   'when package are created automatically')
    group_into_single_package = fields.Boolean(
        string="Create Single Package",
        help="If checked, all products will be packed into a single package",
    )

    def get_ragione_sociale(self, picking):
        if picking:
            partner = False
            if picking.picking_type_id.dropshipping and picking.sale_id:
                partner = picking.sale_id.partner_shipping_id  # se drop uso partner sped. SO
            else:
                partner = picking.partner_id
            if partner.parent_id:
                if not partner.parent_id.print_child_in_label:
                    partner = partner.parent_id
            return unidecode.unidecode(partner.name)

    def name_get(self):
        display_delivery = self.env.context.get('display_delivery', False)
        order_id = self.env.context.get('order_id', False)
        if display_delivery and order_id:
            order = self.env['sale.order'].browse(order_id)
            currency = order.pricelist_id.currency_id.name or ''
            res = []
            for carrier_id in self.ids:
                try:
                    r = self.read([carrier_id], ['name', 'price'])[0]
                    res.append((r['id'], r['name'] + ' (' + (
                        str(r['price'])) + ' ' + currency + ')'))
                except ValidationError:
                    r = self.read([carrier_id], ['name'])[0]
                    res.append((r['id'], r['name']))
        else:
            res = super(TransportCarrier, self).name_get()
        return res

    @api.onchange('state_ids')
    def onchange_states(self):
        self.country_ids = [
            (6, 0, self.country_ids.ids + self.state_ids.mapped('country_id.id'))]


class DeliveryOutFit(models.Model):
    _name = 'delivery.product.extra'
    _description = 'Delivery Product Extra'

    transport_carrier_id = fields.Many2one('transport.carrier', copy=False,
                                           string='Transport Carrier')
    product_id = fields.Many2one('product.product', 'Product', required=False,
                                 ondelete='cascade')
    extra_cost = fields.Float(string='Extra Cost')


class DeliveryPriceRuleInherit(models.Model):
    _inherit = 'delivery.price.rule'

    transport_carrier_id = fields.Many2one('transport.carrier', copy=False,
                                           string='Transport Carrier')
    carrier_id = fields.Many2one('delivery.carrier', 'Carrier', required=False,
                                 ondelete='cascade')
    variable = fields.Selection(selection_add=[('greater_weight_and_weightvolume',
                                                'Greater Between Weight and Weightvolume')],
                                ondelete={
                                    'greater_weight_and_weightvolume': 'set default'})
