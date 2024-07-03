/** @odoo-module */
import { Component, useState } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class CustomerLocationButton extends Component {
    static template = "custom_pos_screen.LocationButton";

    setup() {
        this.pos = usePos();
        this.state = useState({ customer_location: "Customer Location" });
        this.setLocation();
    }

    async setLocation() {
        const current_order = this.pos.get_order();
        if (current_order) {
            this.state.customer_location = current_order.location ? current_order.location : "Customer Location";
        }
    }

    click() {
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
