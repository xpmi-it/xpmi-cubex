/** @odoo-module **/

import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";

export class WebsiteBuilder extends Component {
    static components = { Dialog };
    static template = 'theme_alan.website_builder';
    activeTab(ev, target){
        $('.edit-snippet-builder-box .e-sb-tab label').removeClass('e-sb-active');
        $(ev.target).addClass('e-sb-active');
        $('.e-sb-tab--content').removeClass('active').addClass('d-none');
        $('#'+target).addClass('active').removeClass('d-none');
    }
    _confirm(){
        const uniq = `${Date.now()}_${Math.floor(Math.random() * 1000)}`;
        var snippet = $("input[name='radio-snippet']:checked").closest('.snippet-as').find('textarea').html();

        var target = this.props.target.$target
        $(target).empty().append(snippet);
        var model = $(target).parent().attr('data-oe-model');
        if(model){
            $(target).parent().addClass('o_editable o_dirty');
        }
        const $carousel = $(target).find('.s_carousel');
        if ($carousel.length) {
            const newId = 'myCarousel_' + uniq;
            $carousel.attr('id', newId);

            $(target)
                .find('button[data-bs-target^="#myCarousel"]')
                .attr('data-bs-target', '#' + newId);
                
            $(target)
            .find('a.carousel-control-prev, a.carousel-control-next')
            .attr('href', `#${newId}`);
            }
        // this.trigger_up('widgets_start_request', {
        //     $target:$('.hero_slider')
        // });
        this.props.close();
    }
}
