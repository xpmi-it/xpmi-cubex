from odoo import api, fields, models


class StockDeliveryNoteLineInherit(models.Model):
    _inherit = "stock.delivery.note.line"

    price_subtotal = fields.Monetary(
        string="Price Subtotal",
        currency_field="currency_id",
        compute="_compute_amount_price",
    )
    price_total = fields.Monetary(
        string="Price Total",
        currency_field="currency_id",
        compute="_compute_price_total",
    )

    @api.depends("price_unit", "discount", "product_qty", "tax_ids")
    def _compute_amount_price(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(
                price,
                line.currency_id,
                line.product_qty
            )
            line.update({
                "price_total": taxes['total_included'],
                "price_subtotal": taxes['total_excluded'],
            })
