/** @odoo-module alias=theme_alan.ProductShare **/

import { Component,useRef } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class ProductShare extends Component {
    static template = "theme_alan.ProductShare";
    static components = { Dialog };
    static props = {
        close: Function,
        product_link: String,
        body: String,
    }
    setup() {
        this.notification = useService("notification");
        this.copyBtn = useRef("copy_btn");
        super.setup();
    }
    async copyToProductLink() {
        let button = this.copyBtn.el;
        let input = document.createElement("input");
        input.value = this.props.product_link;
        document.body.appendChild(input);
        input.select();
        input.setSelectionRange(0, 99999); // For mobile compatibility

        try {
            document.execCommand("copy");
            button.disabled = true;
            button.innerHTML = `<i class="fa fa-check" aria-hidden="true"></i>`;
            setTimeout(() => {
                button.disabled = false;
                button.innerHTML = `<i class="fa fa-clone"></i>`;
            }, 2000);
        } catch (err) {
            console.error("Copy failed", err);
            this.notification.add(_t("Failed to copy link!"));
        } finally {
            document.body.removeChild(input);
        }
    }
}
export default {
    ProductShare: ProductShare
}