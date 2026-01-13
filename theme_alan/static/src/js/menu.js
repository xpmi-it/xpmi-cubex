/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
export const extraMenuUpdateCallbacks = [];
import { SIZES, utils as uiUtils } from "@web/core/ui/ui_service";

publicWidget.registry.hoverableDropdown.include({
        _updateDropdownVisibility(ev, doShow = true) {
            if (uiUtils.getSize() < SIZES.LG) {
                return;
            }
            if (ev.currentTarget.closest('.o_extra_menu_items')) {
                return;
            }
            const dropdownToggleEl = ev.currentTarget.querySelector('.dropdown-toggle');
            if (!dropdownToggleEl) {
                return;
            }
            const dropdown = Dropdown.getOrCreateInstance(dropdownToggleEl);
            const isInsideDashboard = $(dropdown._parent).closest('.as_user_dashboard').length > 0;
            if (!isInsideDashboard){
                if (doShow) {
                    dropdown.show();
                } else {
                    dropdown.hide();
                }
            }

        },
})
