/** @odoo-module **/
import options from "@web_editor/js/editor/snippets.options";

options.registry.MegaMenuLayout = options.registry.MegaMenuLayout.extend({

    _getCurrentTemplateXMLID: function () {
        let currentTemplateXMLID = this._super();
        let asMegamenu = this.$target.find(".as_mega_menu").attr("data-as-snippet")
        if (asMegamenu == 'as_mega_menu' && (currentTemplateXMLID == 'website.undefined' || currentTemplateXMLID == 'website_sale.undefined')) {
            currentTemplateXMLID = "atharva_theme_base.as_megamenus";
            if (this.fetchEcomCategories){
                currentTemplateXMLID = "atharva_theme_base.as_mega_menu_category";
            }
            else{
                currentTemplateXMLID = "atharva_theme_base.as_megamenus";
            }
        }
        return currentTemplateXMLID;
    },
})