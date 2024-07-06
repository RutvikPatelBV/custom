/** @odoo-module */
import { Component, useState } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
export class CustomerLocationButton extends Component {
    static template = "custom_pos_screen.LocationButton";

    setup() {
        this.pos = usePos();
        this.state = useState({ customer_location: "Customer Location" });
        this.setLocation();
        this.popup = useService("popup");

    }

    async setLocation() {
        const current_order = this.pos.get_order();
        if(!current_order.get_partner()){
        this.state.customer_location="Customer Location"
        }
        if (current_order) {
            this.state.customer_location = current_order.location ? current_order.location : "Customer Location";
        }
    }

    click() {
        const current_order = this.pos.get_order();
        if(!current_order.get_partner()){
              this.popup.add(ErrorPopup, {
                    title: _t("Error"),
                    body: _t("Please! First you select customer"),
                });
            return
        }
        this.pos.showScreen("CustomerLocationScreen");
    }
}

// Add the button to the ProductScreen
ProductScreen.addControlButton({
    component: CustomerLocationButton,
    condition: function () {
        return true;
    },
});
