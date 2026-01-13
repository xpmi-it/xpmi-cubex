# Copyright (C) 2024-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models


class StockMoveInherit(models.Model):
    _inherit = "stock.move"

    def return_package_from_so_line(self):
        self.ensure_one()
        if (
            self.picking_id
            and self.sale_line_id
            and self.sale_line_id.product_packaging_id
        ):
            packaging_id = self.sale_line_id.product_packaging_id
            if self.quantity % packaging_id.qty == 0:
                return packaging_id.name, self.quantity / packaging_id.qty
            else:
                return "", 0.0
        return "", 0.0