# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from odoo import api, fields, models


class ProductDataFeedShipping(models.Model):
    _name = "product.data.feed.shipping"
    _description = 'Product Shipping Data'
    _rec_name = 'group_id'

    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country',
        ondelete='cascade',
        required=True,
    )
    state_id = fields.Many2one(
        comodel_name='res.country.state',
        ondelete='set null',
        domain="[('country_id', '=', country_id)]",
    )
    use_postal_codes = fields.Boolean()
    postal_code_from = fields.Char()
    postal_code_to = fields.Char()
    group_id = fields.Many2one(
        comodel_name='product.data.feed.shipping.group',
        string='Shipping Group',
        help='Allow grouping products together so that you can configure specific shipping rates.',
    )
    price = fields.Float(digits='Product Price', required=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id,
        required=True,
    )
    min_handling_time = fields.Integer()
    max_handling_time = fields.Integer()
    min_transit_time = fields.Integer()
    max_transit_time = fields.Integer()

    def get_region(self):
        self.ensure_one()
        return \
            self.use_postal_codes and (self.postal_code_from or self.postal_code_to) \
            and '%s-%s' % (self.postal_code_from or '', self.postal_code_to or '') \
            or not self.use_postal_codes and self.state_id and self.state_id.code or ''

    @api.depends('country_id', 'state_id', 'group_id', 'price', 'currency_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = "%s:%s:%s:%.2f %s" % (
                rec.country_id.code,
                rec.get_region(),
                rec.group_id.name if rec.group_id else '',
                rec.price,
                rec.currency_id.name,
            )
