/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";
import { _t } from '@web/core/l10n/translation';
import { LoginPopup } from "theme_alan.LoginPopup";
import publicWidget from "@web/legacy/js/public/public_widget";
import websiteSearch from '@website/snippets/s_searchbar/000';
import { renderToElement, renderToString } from "@web/core/utils/render";
import { markup } from "@odoo/owl";

var { searchBar } = websiteSearch;

let SnippetLazyLoader = publicWidget.Widget.extend({

    disabledInEditableMode: false,

    willStart: function () {
        const cr = this;
        const parent = cr._super.bind(cr, ...arguments);

        if (!window.frameElement && cr.$target.hasClass('as-load')) {
            function fallbackScrollCheck() {
                return new Promise((resolve) => {
                    function checkVisibility() {
                        const scroll_pos = $(window).scrollTop();
                        const windowHeight = window.innerHeight || document.documentElement.clientHeight;
                        if (cr.$target.offset().top < scroll_pos + windowHeight + 100) {
                            $(window).off('scroll', throttledCheck);
                            resolve();
                        }
                    }
                    const throttledCheck = _.throttle(checkVisibility, 100);
                    setTimeout(checkVisibility, 50); // allow DOM rendering
                    $(window).on('scroll', throttledCheck);
                });
            }

            function useIntersectionObserver() {
                return new Promise((resolve) => {
                    const observer = new IntersectionObserver((entries, obs) => {
                        if (entries[0].isIntersecting) {
                            obs.disconnect();
                            resolve();
                        }
                    }, { rootMargin: "100px" });
                    observer.observe(cr.el);
                });
            }

            const loader = ('IntersectionObserver' in window)
                ? useIntersectionObserver()
                : fallbackScrollCheck();

            return loader.then(() => parent());
        }

        return parent();
    },

})

// Login Popup
export const AlanLoginPopup = publicWidget.Widget.extend({
    selector: ".as_login_popup",
    events:{
        'click':'_show_login_popup',
    },

    _show_login_popup:function(ev){
        ev.preventDefault();
        const offcanvasEl = document.getElementById("top_menu_collapse_mobile");
        if (offcanvasEl && offcanvasEl.classList.contains('show')) {
            offcanvasEl.classList.remove('show');
            document.body.classList.remove('offcanvas-backdrop', 'modal-open');
            document.body.style.overflow = '';
            document.body.style.paddingRight = '';
            offcanvasEl.setAttribute('aria-hidden', 'true');
            offcanvasEl.setAttribute('aria-expanded', 'false');
        }
        this.call("dialog", "add", LoginPopup, {})
    }
})

publicWidget.registry.AlanLoginPopup = AlanLoginPopup;

publicWidget.registry.ProductWishlist.include({
    selector: '#wrapwrap',
})
publicWidget.registry.ProductComparison.include({
    selector: '#wrapwrap',
})

let AlanSliders = SnippetLazyLoader.extend({
    init: function () {
        this._super.apply(this, arguments);
        this.rpc = rpc
    },
    _get_loader:function(){
        for (const product_slider of this.$target) {
            const $slider = $(product_slider);
            const snippet_editor = JSON.parse($slider.attr("data-design-edit"));
            const def_col = Number(snippet_editor.default_col_desk);

            // compute a Bootstrap col‑width so that def_col cards fit in one row
            // e.g. if def_col = 4, colClass = 'col-lg-3' (12/4 = 3)
            const colSize = Math.floor(12 / def_col) || 1;
            const colClass = `col-lg-${colSize} col-md-${Math.min(6, colSize*2)}`;
            if(!this.editableMode){
                 rpc('/get/snippets_loader_gif').then((res)=>{
                if (!colClass){
                    colClass = 1
                }

                // your single-card placeholder template (no outer <div class="row">)
                const singleLoaderGif = `
                <div class="${colClass} mb-4 text-center">
                    <img
                    src="${res}"
                    alt="Loading…"
                    style="margin:auto;"
                    />
                </div>`;

                // build the full row of def_col cards
                let rowHtml = '<div class="row">';
                for (let i = 0; i < def_col; i++) {
                  rowHtml += singleLoaderGif;
                }
                rowHtml += '</div>';

                // inject into your slider container
                $slider.empty().append(rowHtml);
            })
            }
        }
    },
    _getProductSlider:function(){
        for (const product_slider of this.$target) {
            let snippet_editor = JSON.parse($(product_slider).attr("data-design-edit"))
            let context = {
                'snippet':$(product_slider).attr("data-snippet-name"),
                'record_ids':JSON.parse($(product_slider).attr("data-records-ids")),
                'modal':$(product_slider).attr("data-modal"),
                'design_editor':snippet_editor,
            }

            if(!this.editableMode){
                rpc('/get_snippet_template', context).then((res)=>{
                    if(this.selector == "[data-snippet-name='CategoryProduct'], [data-snippet-name='categories_products']" || this.selector == "[data-snippet-name='BrandProduct'], [data-snippet-name='brand_products']"){
                        $(product_slider).empty().append(res['template']);
                        var $template = $(product_slider).find('.as_page_swiper')
                        for (let s_templ of $template) {

                            $(s_templ).attr("id",'as_swiper_slider_as');
                            if(Object.keys(res.slider_config).length != 0){
                                new Swiper("#as_swiper_slider_as", res.slider_config);
                            }
                            $(s_templ).removeAttr("id","as_swiper_slider_as")
                        }

                    }
                    else{
                        if('record_ids' in res){
                            $(product_slider).attr("data-records-ids", JSON.stringify(res.record_ids))
                        }
                        var $template =  $(res['template']).attr("id","as_swiper_slider_as");
                        $(product_slider).empty().append($template);
                        if(Object.keys(res.slider_config).length != 0){
                            new Swiper("#as_swiper_slider_as", res.slider_config);
                        }
                        $template.removeAttr("id");
                    }
                    this.trigger_up('widgets_start_request', {$target: $template});
                    this.trigger_up('widgets_start_request', {$target: $(".as_quick_view")});
                    this.trigger_up('widgets_start_request', {$target: $(".as_color_variant")});
                });
            }
            else{
                $(product_slider).parents(".s_dynamic_snippets").attr("contenteditable",true)
                $(product_slider).empty().append("<div class='text-center'> <h3>"+snippet_editor.name+"</h3> </div>");
            }
        }
    },
    _tab_change:function(ev){
        this.$target.find(".as-tab-name").removeClass("active");
        let tab_id = $(ev.currentTarget).data('id');
        $(ev.currentTarget).addClass('active');
        if(this.selector == "[data-snippet-name='CategoryProduct'], [data-snippet-name='categories_products']"){
            var slider_tab = "[data-tab-id='category_"+tab_id+"']";
            this.$target.find(".as_category_products").removeClass("active");

        }else{
            var slider_tab = "[data-tab-id='brand_"+tab_id+"']";
            this.$target.find(".as_brand_products").removeClass("active");
        }
        this.$target.find(".as-tab-pane").removeClass("active")
        this.$target.find(slider_tab).addClass("active");
    },
})

publicWidget.registry.alanProductSlider = AlanSliders.extend({
    selector:"[data-snippet-name='ProductSlider'], [data-snippet-name='products'], [data-snippet-name='BestSellingProduct'], [data-snippet-name='LatestProduct']",
    disabledInEditableMode: false,
    start:function(){
        this._get_loader()
        this._getProductSlider();
    }
});

publicWidget.registry.alanCategoryProduct = AlanSliders.extend({
    selector:"[data-snippet-name='CategoryProduct'], [data-snippet-name='categories_products']",
    disabledInEditableMode: false,
    events:{
        'click .as-tab-name':'_tab_change'
    },
    start:function(){
        this._get_loader()
        this._getProductSlider();
    }
});

publicWidget.registry.alanBrandProduct = AlanSliders.extend({
    selector:"[data-snippet-name='BrandProduct'], [data-snippet-name='brand_products']",
    disabledInEditableMode: false,
    events:{
        'click .as-tab-name':'_tab_change'
    },
    start:function(){
        this._get_loader()
        this._getProductSlider();
    }
});

publicWidget.registry.alanProductBanner = AlanSliders.extend({
    selector:"[data-snippet-name='ProductBanner'], [data-snippet-name='product_banner']",
    disabledInEditableMode: false,
    start:function(){
        this._get_loader()
        this._getProductSlider();
    }
});

publicWidget.registry.alanCategorySlider = AlanSliders.extend({
    selector:"[data-snippet-name='CategorySlider'], [data-snippet-name='categories']",
    disabledInEditableMode: false,
    start:function(){
        this._get_loader()
        this._getProductSlider();
    }
});

publicWidget.registry.alanBrandSlider = AlanSliders.extend({
    selector:"[data-snippet-name='BrandSlider'], [data-snippet-name='brands']",
    disabledInEditableMode: false,
    start:function(){
        this._get_loader()
        this._getProductSlider();
    }
});

publicWidget.registry.alanBlogSlider = AlanSliders.extend({
    selector:"[data-snippet-name='BlogSlider'], [data-snippet-name='blogs']",
    disabledInEditableMode: false,
    start:function(){
        this._get_loader()
        this._getProductSlider();
    }
});

publicWidget.registry.MegaMenuTabsSnippets = publicWidget.Widget.extend({
    selector: '.as-mm-tabs-level-1',
    disabledInEditableMode:false,
    events:{
        'mouseenter':'_showMegaMenuTabs',
        'click .as-mob-tab-menu':'_showMegaMenuTabsMob',
    },
    _showMegaMenuTabs:function(ev){
        if($(ev.currentTarget).hasClass("active") == false){
            this.$target.parents(".as-mm-tabs-levels").find(".as-mm-tabs-level-1.active").removeClass("active");
            $(ev.currentTarget).addClass("active");
            this.trigger_up("widgets_start_request", { $target: $("[data-snippet-name='megamenu_products'],[data-snippet-name='MegaMenuProduct']") })
            this.trigger_up("widgets_start_request", { $target: $("[data-snippet-name='megamenu_category'],[data-snippet-name='MegaMenuCategory']") })
            this.trigger_up("widgets_start_request", { $target: $("[data-snippet-name='megamenu_brand'],[data-snippet-name='MegaMenuBrand']") })
        }

    },
    _showMegaMenuTabsMob:function(ev){
        ev.preventDefault();
        ev.stopPropagation();
        if($(ev.currentTarget).parents(".as-mm-tabs-level-1").hasClass("as-mob-menu")){
            $(ev.currentTarget).parents(".as-mm-tabs-level-1").removeClass("active").removeClass("as-mob-menu");
        }else{
            $(ev.currentTarget).parents(".as-mm-tabs-level-1").addClass("active").addClass("as-mob-menu");
        }
    }
});

publicWidget.registry.AdvanceMegaMenu = publicWidget.Widget.extend({
    selector: '.as-advance-header',
    start:function(){
        this.$target.find('.as-ah-mobile_menu').click(function (ev) {
            ev.stopPropagation();
            // $(ev.currentTarget).addClass("as-ah-h1-close")
            $(ev.currentTarget).parents(".as-l1-items").addClass("as-ah-h1-open").trigger('click');
        });
        this.$target.find('.as-ah-mobile_menu-l2').click(function (ev) {
            ev.stopPropagation();
            $(ev.currentTarget).parents(".as-l2-items").addClass("as-ah-h2-open").trigger('click');
        });
        this.$target.find('.as-ah-mobile_menu-l3').click(function (ev) {
            ev.stopPropagation();
            $(ev.currentTarget).parents(".as-l3-items").addClass("as-ah-h3-open").trigger('click');
        });
    },
});

publicWidget.registry.AdvanceMegaMenuMobile = publicWidget.Widget.extend({
    selector: '.as-mob-2nd-menu',
    start:function(){
        this.$target.find('.as_mob_2nd_btn').click(function(ev){
            $($(ev.currentTarget)[0].nextElementSibling).addClass("as-advance-header-open")
        })
        this.$target.find('.as-bbl-1').click(function(ev){
            $(ev.currentTarget).parents(".as-advance-header").removeClass("as-advance-header-open")
        })
        this.$target.find('.as-bbl-2').click(function(ev){
            $(ev.currentTarget).parents(".as-l1-items").removeClass("as-ah-h1-open")
        })
        this.$target.find('.as-bbl-3').click(function(ev){
            $(ev.currentTarget).parents(".as-l2-items").removeClass("as-ah-h2-open")
        })
        this.$target.find('.as-bbl-4').click(function(ev){
            $(ev.currentTarget).parents(".as-l3-items").removeClass("as-ah-h3-open")
        })
    }
});

publicWidget.registry.MegaMenuSnippets = publicWidget.Widget.extend({
    selector: '.nav-item',
    disabledInEditableMode:false,
    is_clicked :false,
    events:{
        'click .as-advance-nav-mob':'_advanceNavMob',
        'click .as-advance-header-close':'_advanceNavMobClose',
        'click .swiper-button-next, .swiper-button-prev':'_stopCloseMenu',
    },
    init: function () {
        this._super.apply(this, arguments);
    },

    _stopCloseMenu:function(ev){
        ev.preventDefault();
        ev.stopPropagation()
    },
    start:function(){
        this.$target.find('.as-ah-mobile_menu-l1').click(function (ev) {
            $(ev.currentTarget).click(function (ev) {
                if($(ev.currentTarget).parents(".as-ah-h1-open").length){
                    $(ev.currentTarget).parents(".as-l1-items").removeClass("as-ah-h1-open");
                    $($(ev.currentTarget)[0].nextElementSibling).find(".as-l2-items").removeClass("as-ah-h2-open")
                    $($(ev.currentTarget)[0].nextElementSibling).find(".as-l3-items").removeClass("as-ah-h3-open")
                }
                else{
                    $(ev.currentTarget).parents(".as-l1-items").addClass("as-ah-h1-open").trigger('click');
                }
            });

        });
        this.$target.find('.as-ah-mobile_menu-l2').click(function (ev) {
            $(ev.currentTarget).click(function (ev) {
                if($(ev.currentTarget).parents(".as-ah-h2-open").length){
                    $(ev.currentTarget).parents(".as-l2-items").removeClass("as-ah-h2-open");
                    $($(ev.currentTarget).parents(".as-l2-link")[0].nextElementSibling).find(".as-l3-items").removeClass("as-ah-h3-open")
                }
                else{
                    $(ev.currentTarget).parents(".as-l2-items").addClass("as-ah-h2-open").trigger('click');
                }
            });

        });
        this.$target.find('.as-ah-mobile_menu-l3').click(function (ev) {
            $(ev.currentTarget).click(function (ev) {
                if($(ev.currentTarget).parents(".as-ah-h3-open").length){
                    $(ev.currentTarget).parents(".as-l3-items").removeClass("as-ah-h3-open");
                }
                else{
                    $(ev.currentTarget).parents(".as-l3-items").addClass("as-ah-h3-open").trigger('click');
                }
            });
        });
    },
    _advanceNavMob: function(ev){
        $(ev.currentTarget).parents('li').addClass("as-advance-header-li-open")
        $($(ev.currentTarget)).addClass("as-advance-header-close")
        $($(ev.currentTarget)[0].nextElementSibling).addClass("as-advance-header-open")

    },
    _advanceNavMobClose:function(ev){
        $(ev.currentTarget).parents('li').removeClass("as-advance-header-li-open")
        $($(ev.currentTarget)).removeClass("as-advance-header-close")
        $($(ev.currentTarget)[0].nextElementSibling).removeClass("as-advance-header-open")
        $($(ev.currentTarget)[0].nextElementSibling).find(".as-l1-items").removeClass("as-ah-h1-open")
        $($(ev.currentTarget)[0].nextElementSibling).find(".as-l2-items").removeClass("as-ah-h2-open")
        $($(ev.currentTarget)[0].nextElementSibling).find(".as-l3-items").removeClass("as-ah-h3-open")
    },
})

let MegaMenuSnippetLazyLoader = publicWidget.Widget.extend({
    disabledInEditableMode: false,
    willStart: function () {
        var cr = this;
        var parent = cr._super.bind(cr, ...arguments);
        if (!window.frameElement) {
            // cr.target.parents(".as-mm-tabs-level-1")
            var _itsToShow = function () {
                var show = new Promise((resolve, reject) => {
                    function checkVisibility() {
                        resolve();
                    }
                    checkVisibility();

                });
                return show;
            };
            if ($(cr.$target).parents(".as-mm-tabs-level-1").hasClass("active") || cr.$target.parents(".as-mega-menu-preview-section").parent(".o_mega_menu")) {
                return _itsToShow().then(() => parent());
            }
            else{
                return new Promise((resolve, reject) => {})
            }
        }
        return parent();
    },
})

let MegaMenuSnippets = MegaMenuSnippetLazyLoader.extend({
    init: function () {
        this._super.apply(this, arguments);
        this.rpc = rpc
    },
    _showMegaMenu: async function () {
        for (const product_slider of this.$target) {
            const $el = $(product_slider);
            const snippetName = $el.attr("data-snippet-name");
            const recordIds = JSON.parse($el.attr("data-records-ids") || "[]");
            const snippetKey = `mega_snippet_cache:${snippetName}-${recordIds.join(',')}`;

            const context = {
                snippet: snippetName,
                record_ids: recordIds,
                modal: $el.attr("data-modal"),
                design_editor: JSON.parse($el.attr("data-design-edit")),
            };

            if (!this.editableMode) {
                const cached = localStorage.getItem(snippetKey);

                if (cached) {
                    this._renderSnippet($el, JSON.parse(cached));
                } else {
                    this._clearMegaSnippetCache();
                    this.rpc('/get_megamenu_snippet_template', context).then((res) => {
                        localStorage.setItem(snippetKey, JSON.stringify(res));
                        this._renderSnippet($el, res);
                    });
                }
            } else {
                $el.parents(".as_mega_menu").attr("contenteditable", true);
                $el.empty().append(`<div class='text-center'><h3>${context.design_editor.name}</h3></div>`);
            }
        }
    },
    _clearMegaSnippetCache: function () {
    for (let i = localStorage.length - 1; i >= 0; i--) {
        const key = localStorage.key(i);
        if (key && key.startsWith('mega_snippet_cache:')) {
            localStorage.removeItem(key);
        }
    }
},

    _renderSnippet: function ($el, res) {
        if (res.record_ids) {
            $el.attr("data-records-ids", JSON.stringify(res.record_ids));
        }
        const $template = $(res.template).attr("id", "as_swiper_slider_as");
        $el.empty().append($template);
        if (Object.keys(res.slider_config).length !== 0) {
            new Swiper("#as_swiper_slider_as", res.slider_config);
        }
        $template.removeAttr("id");
    }
})


publicWidget.registry.alanMegamenuProductSlider = MegaMenuSnippets.extend({
    selector:"[data-snippet-name='megamenu_products'],[data-snippet-name='MegaMenuProduct']",
    disabledInEditableMode: false,
    start:function(){
        this._showMegaMenu();
    },

});

publicWidget.registry.alanMegamenuCategorySlider = MegaMenuSnippets.extend({
    selector:"[data-snippet-name='megamenu_category'],[data-snippet-name='MegaMenuCategory']",
    disabledInEditableMode: false,
    start:function(){
        this._showMegaMenu();
    }
});

publicWidget.registry.alanMegamenuBrandSlider = MegaMenuSnippets.extend({
    selector:"[data-snippet-name='megamenu_brand'],[data-snippet-name='MegaMenuBrand']",
    disabledInEditableMode: false,
    start:function(){
        this._showMegaMenu();
    }
});

export const HeroSlider = publicWidget.Widget.extend({
    selector:".hero_slider",
    disabledInEditableMode: false,
    start:function(){
        var data = new Swiper(".as-slide-swiper", {
            slidesPerView: 1,
            centeredSlides: true,
            slidesPerGroup: 1,
            spaceBetween: 15,
            slideToClickedSlide: true,
            loop: true,
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
              breakpoints: {
                1024: {
                  slidesPerView: 1.60,
                },
              },
        });
    }
});
publicWidget.registry.HeroSlider = HeroSlider;

searchBar.include({
    xmlDependencies:['/website/static/src/snippets/s_searchbar/000.xml'],

    _render: function (res) {
        const $prevMenu = this.$menu;
        this.$el.toggleClass('dropdown show', !!res);
        if (res && this.limit) {
            const results = res['results'];
            if (this.searchType == 'as_advance_search') {
                var template = 'theme_alan.s_alan_searchbar';
            }else{
                var template = 'website.s_searchbar.autocomplete';
            }
            const candidate = template + '.' + this.searchType;
            if (renderToString.app.getRawTemplate(candidate)) {
                template = candidate;
            }
            this.$menu = $(renderToElement(template, {
                results: results,
                brands: res['brands'],
                tags: res['tags'],
                category: res['category'],
                is_child_categ: Array.isArray(res['category']) && res['category'].length > 0 ? res['category'].some((category) => category.parent_id): false,
                products: res['products'],
                parts: res['parts'],
                hasMoreResults: results.length < res['results_count'],
                search: this.$input.val(),
                fuzzySearch: res['fuzzy_search'],
                widget: this,
            }));
            this.$menu.css('min-width', this.autocompleteMinWidth);
            this.$el.append(this.$menu);
            this.$el.find('button.extra_link').on('click', function (event) {
                event.preventDefault();
                window.location.href = event.currentTarget.dataset['target'];
            });
            this.$el.find('.s_searchbar_fuzzy_submit').on('click', (event) => {
                event.preventDefault();
                this.$input.val(res['fuzzy_search']);
                const form = this.$('.o_search_order_by').parents('form');
                form.submit();
            });
        }
        if ($prevMenu) {
            $prevMenu.remove();
        }
    },
    async _fetch() {
        if(this.searchType == "as_advance_search"){
            const res = await rpc('/website/snippet/autocomplete',
                {
                    'search_type': this.searchType,
                    'term': this.$input.val(),
                    'order': this.order,
                    'limit': this.limit,
                    'max_nb_chars': Math.round(Math.max(this.autocompleteMinWidth, parseInt(this.$el.width())) * 0.22),
                    'options': this.options,
                },
            );
            const fieldNames = [
                'name',
                'description',
                'extra_link',
                'detail',
                'detail_strike',
                'detail_extra',
            ];
            if(res.products == undefined){
                res.products = [];
            }
            if(res.brands == undefined){
                res.brands = [];
            }
            if(res.tags == undefined){
                res.tags = [];
            }
            if(res.category == undefined){
                res.category = [];
            }
            const as_srch_lst = [res.products, res.brands, res.tags, res.category];
            as_srch_lst.forEach(ele => {
                ele.forEach(record => {
                    for (const fieldName of fieldNames) {
                        if (record[fieldName]) {
                            if (typeof record[fieldName] === "object") {
                                for (const fieldKey of Object.keys(record[fieldName])) {
                                    record[fieldName][fieldKey] = markup(record[fieldName][fieldKey]);
                                }
                            } else {
                                record[fieldName] = markup(record[fieldName]);
                            }
                        }
                    }
                });
            });
            return res;
        }
        else{
            return this._super.apply(this, arguments);
        }
    },
})

publicWidget.registry.MegaMenuDropdown.include({

    _updateActiveMenuLinks() {
        if (this.el.querySelector(".navbar #top_menu a.nav-link.active")) {
            return;
        }
        const currentHrefWithoutHash = `${window.location.origin}${window.location.pathname}`;
        const megaMenuEls = this.el.querySelectorAll(".o_mega_menu");
        let matchingLink = null;
        megaMenuEls.forEach((megaMenuEl, position) => {
            const linkEls = Array.from(megaMenuEl.querySelectorAll(`a:not([href="#"])`));
            matchingLink = linkEls.find((linkEl) => {
                const url = new URL(linkEl.href);
                return `${url.origin}${url.pathname}` === currentHrefWithoutHash;
            });
            if (matchingLink) {
                const megaMenuToggleEl = megaMenuEl
                    .closest(".nav-item")
                    .querySelector(".o_mega_menu_toggle");

                const mobileMegaMenuToggleEl = this.el.querySelectorAll(
                    "#top_menu_collapse_mobile .top_menu .o_mega_menu_toggle"
                )[position];

                if (megaMenuToggleEl && mobileMegaMenuToggleEl){
                    megaMenuToggleEl.classList.add("active");
                    mobileMegaMenuToggleEl.classList.add("active");
                }
            }
        });
    },
})

export default {
    HeroSlider: publicWidget.registry.HeroSlider,
    searchBar: searchBar,
};
