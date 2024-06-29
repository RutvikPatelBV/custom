/* @odoo-module */

import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";

class CustomDiscount extends Component {
    static template = "point_of_sale.CustomDiscountButton";

    setup() {
        this.popup = useService("popup");
        this.pos = useService("pos");
        this.orm = useService("orm");
        console.log('hello world');
    }
    async onCustomDiscount() {
            const result = await this.orm.call("ir.config_parameter", "get_param", ["practice.custom_discount"]);
            const order = this.pos.get_order()
            const custom_discount = parseFloat(result);
            console.log(custom_discount)

        const selectedLines = this.pos.get_order().get_orderlines();
        order.discounted_order=true
        for (let selectedLine of  selectedLines){
            selectedLine.set_discount(custom_discount);
            }
        }

};

ProductScreen.addControlButton({
    component: CustomDiscount,
    position: ["after", "AddNotesButton"],
});
