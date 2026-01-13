/** @odoo-module **/

import { SnippetBuilder } from "./SnippetBuilder"
import { registry } from "@web/core/registry";
import options from "@web_editor/js/editor/snippets.options";
import {debounce} from "@web/core/utils/timing";

options.registry.SnippetBuilderOption = options.Class.extend({
    events:{
        'click .as_snippet_open_preview':'_openSnippetConfigure',
    },

    init() {
        this._super(...arguments);
        this.dialog = this.bindService("dialog");
        this._openSnippetConfigureDebounced = debounce(this._openSnippetConfigure.bind(this), 300);
        this.$target.on("click", this._openSnippetConfigureDebounced);

    },

    _openSnippetConfigure(ev) {
        const snippet_type = this.$target.attr("data-as-snippet");
        const DynamicSnippetLists = registry.category("snippet_builder").get("as_dynamic_snippets");
        const MegamenuSnippetLists = registry.category("snippet_builder").get("as_megamenu_snippets");
        const SnippetLists = snippet_type === "as_mega_menu" ? MegamenuSnippetLists : DynamicSnippetLists;
        let config_data = $(this.$target).find(".as-snippet-preview");
        if(config_data.length == 0 || config_data.find(".as_col").length == 0){
            config_data = undefined
        }

        if(ev.handleObj.selector == ".as_snippet_open_preview"){
            this.dialog.add(SnippetBuilder, {
                snippets: SnippetLists,
                target: this,
                config_data,
                snippet_type,
                confirm: () => resolve(true),
                cancel: () => resolve(false),
                });
        }

        if(config_data !=undefined){
            config_data.find(".as_col").off("click").on("click", function (e) {
                if($(e.currentTarget).attr("data-snippet-name") != "static_snippets"){
                    this.dialog.add(SnippetBuilder, {
                    snippets: SnippetLists,
                    target: this,
                    config_data,
                    snippet_type,
                    confirm: () => resolve(true),
                    cancel: () => resolve(false),
                    });
                }
            }.bind(this));
        }
        else{
            this.dialog.add(SnippetBuilder, {
            snippets: SnippetLists,
            target: this,
            config_data,
            snippet_type,
            confirm: () => resolve(true),
            cancel: () => resolve(false),
            });
        }
    },

    onBuilt() {
        const SnippetLists = registry.category("snippet_builder").get("as_dynamic_snippets");
        const snippet_type = this.$target.attr("data-as-snippet");
        this.dialog.add(SnippetBuilder, {
            snippets: SnippetLists,
            target: this,
            snippet_type,
            confirm: () => resolve(true),
            cancel: () => resolve(false),
        });
    },
    cleanForSave: function () {
        $(this.$target).find(".as-snippet-drop-container").each(function (idx, elem) {
            if ($(elem).attr("data-snippet-name") != "static_snippets"){
                $(elem).empty();
            }
        });
    },
})
