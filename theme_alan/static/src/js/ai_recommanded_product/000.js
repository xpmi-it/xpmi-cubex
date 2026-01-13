/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.AIProductRecommandation = publicWidget.Widget.extend({
    selector: ".product_recommanded_ai, .as_recommanded_model",

    disabledInEditableMode:false,
    init() {
        this._super(...arguments);
        this.rpc = rpc;
    },

    start: function () {
        this.get_recommanded_product()
        return this._super.apply(this, arguments);
    },

    get_recommanded_product: async function(){
        if(!this.editableMode){
            let product = $(".product_recommanded_ai").attr("data-product-tmpl-id") || 0
            let url = "/fetch_ai_recommanded_product/" + product
            await this.rpc(url, {}).then((data)=>{

            $(".offcanvas_recommanded_product").empty().append(data['shop_template'])
            $(".product_recommanded_container").empty().append(data['product_template'])
            new Swiper(".as-ai-recommanded-swiper", {
                slidesPerView: 1.75,
                spaceBetween: 10,
                navigation: {
                    nextEl: ".swiper-button-alt-next",
                    prevEl: ".swiper-button-alt-prev",
                },
                breakpoints: {
                    640: {
                        slidesPerView: 2,
                        spaceBetween: 24,
                    },
                    768: {
                        slidesPerView: 3,
                        spaceBetween: 24,
                    },
                    1024: {
                        slidesPerView: 4,
                        spaceBetween: 24,
                    },

                },
            });
            // this.$target.removeClass("d-none");
            })
            this.trigger_up('widgets_start_request', {$target: $(".as_color_variant")});

        }
        else{
            $(".product_recommanded_container").empty().append('<h2 class="text-center">Similar Products (Generated from AI)</h2>');
        }

    }
});