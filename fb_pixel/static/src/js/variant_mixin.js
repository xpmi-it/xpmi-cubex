/** @odoo-module **/

import VariantMixin from "@website_sale/js/sale_variant_mixin";
import publicWidget from "@web/legacy/js/public/public_widget";
import "@website_sale/js/website_sale";

publicWidget.registry.WebsiteSale.include({
    /**
     * Adds the default_code to the regular _onChangeCombination method
     * @override
     */
    _onChangeCombination: function (ev, $parent, combination){
        VariantMixin._onChangeCombination.apply(this, arguments);
        $parent
            .find('.default_code')
            .first()
            .val(combination.default_code || combination.id)
            .trigger('change');
    }
});
