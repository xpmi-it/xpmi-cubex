from odoo import api, fields, models


class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        res = super(PurchaseOrderInherit, self).button_confirm()
        for line in self.order_line:
            seller_ids = line.product_id.seller_ids.filtered(
                lambda s: s.partner_id.id == line.order_id.partner_id.id)
            if line.product_id and seller_ids:
                seller_ids[0].price = line.price_unit
            line.product_id.standard_price = line.price_unit
        return res

    partner_id = fields.Many2one('res.partner', string='Vendor', required=True,
                                 change_default=True,
                                 check_company=True,
                                 tracking=True,
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id), ('parent_id', '=', False)]",
                                 help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
