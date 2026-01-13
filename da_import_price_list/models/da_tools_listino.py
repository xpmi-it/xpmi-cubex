# Copyright (C) 2023-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso (gborruso@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class DaToolsListino(models.Model):
    _name = "da_tools.listino"
    _description = "Import Pricelist"
    _rec_name = "pricelist_name"

    pricelist_name = fields.Char()
    active = fields.Boolean(string="Attiva", default=True)
    evaso = fields.Boolean(default=False)
    partner_code = fields.Char(string="Codice cliente (Riferimento)")
    ragione_sociale = fields.Char(string="Ragione sociale")
    applied_on = fields.Selection(
        [
            ("1_product", "Prodotto"),
            ("0_product_variant", "Variante Prodotto"),
        ],
        default="1_product",
        string="Applicare a",
    )
    codice = fields.Char(string="Codice prodotto")
    sconto = fields.Float()
    prezzo_fisso = fields.Float(string="Prezzo fisso")
    errore = fields.Char()

    def auto_import_pricelist(self):
        imports_datas = self.search([("evaso", "=", False)])
        product_price_list_model = self.env["product.pricelist"]
        product_price_list_item_model = self.env["product.pricelist.item"]
        partner_model = self.env["res.partner"]
        company_id = self.env.user.company_id.id

        for import_data in imports_datas:
            # svuoto errore
            import_data.errore = ""

            if not import_data.pricelist_name:
                import_data.errore = "Manca name su riga listino"
                continue

            # cerco il listino
            domain = [("name", "=", import_data.pricelist_name)]
            pricelist_id = product_price_list_model.search(domain, limit=1)
            if not pricelist_id:
                price_list_data = {
                    "name": import_data.pricelist_name,
                    "company_id": company_id,
                }
                pricelist_id = product_price_list_model.create(price_list_data)

                # creo la prima regola vuota
                price_list_product_data = {
                    "applied_on": "3_global",
                    "pricelist_id": pricelist_id.id,
                    "company_id": company_id,
                }
                product_price_list_item_model.create(price_list_product_data)

            # abbino listino a cliente se trovato
            domain = [("name", "=", import_data.ragione_sociale)]
            partner_id = partner_model.search(domain)
            if not partner_id and import_data.partner_code:
                domain = [("ref", "=", import_data.partner_code)]
                partner_id = partner_model.search(domain)
                if not partner_id:
                    domain = [("ref", "ilike", import_data.partner_code)]
                    partner_ids = partner_model.search(domain, limit=1)
                    for partner in partner_ids:
                        list_ref = partner.ref.split()
                        for ref in list_ref:
                            if ref == import_data.partner_code:
                                partner_id = partner
                                break

            # abbinare il listino al cliente
            if partner_id and not partner_id.property_product_pricelist:
                partner_id.property_product_pricelist = pricelist_id.id

            # cerco l'articolo
            domain = [("default_code", "=", import_data.codice)]
            if import_data.applied_on == "1_product":
                product_model = self.env["product.template"]
                product_key = "product_tmpl_id"
            else:
                product_model = self.env["product.product"]
                product_key = "product_id"
            product_id = product_model.search(domain, limit=1)
            if not product_id:
                import_data.errore = "Manca prodotto con riferimento interno"
                continue

            # creo la regola per l'articolo letto
            if import_data.prezzo_fisso:
                price_list_product_data = {
                    "applied_on": import_data.applied_on,
                    "pricelist_id": pricelist_id.id,
                    product_key: product_id.id,
                    "compute_price": "fixed",
                    "fixed_price": import_data.prezzo_fisso,
                }
            else:
                price_list_product_data = {
                    "applied_on": import_data.applied_on,
                    "pricelist_id": pricelist_id.id,
                    product_key: product_id.id,
                    "compute_price": "percentage",
                    "percent_price": import_data.sconto,
                }
            price_list_product_data["company_id"] = company_id
            product_price_list_item_model.create(price_list_product_data)
            import_data.evaso = True
