/* @odoo-module */

import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { TextAreaPopup } from "@point_of_sale/app/utils/input_popups/textarea_popup";

class PosCustomButton extends Component {
    static template = "point_of_sale.PosCustomButton";

    setup() {
        this.popup = useService("popup");
        this.pos = useService("pos");
        console.log('hello world');
    }

    async onClickClear() {
        const selectedLine = this.pos.get_order().get_selected_orderline();
        if (selectedLine) {
            this.pos.get_order().removeOrderline(selectedLine);
            console.log(selectedLine);
        }
    }

    async onClickClearAll() {
        const selectedLines = this.pos.get_order().get_orderlines();
        console.log(selectedLines);
        if (selectedLines.length > 0) {
            this.popup.add(ErrorPopup, {
                title: _t("All Order is Removed"),
                body: _t("Orderlines is now empty."),
            });
            for (const line of selectedLines) {
                this.pos.get_order().removeOrderline(line);
            }
        }
    }

//    async onAddItemNote() {
//        const selectedLine = this.pos.get_order().get_selected_orderline();
//        if (!selectedLine) {
//            this.popup.add(ErrorPopup, {
//                title: _t("OrderLine is not selected"),
//                body: _t("Please select an order first!"),
//            });
//            return;
//        }
//
//        const { confirmed, payload: inputNote } = await this.popup.add(TextAreaPopup, {
//            startingValue: selectedLine.get_customer_note(),
//            title: _t("Add Customer Note Here"),
//        });
//
//        if (confirmed) {
//            selectedLine.set_customer_note(inputNote);
//        }
//    }
};

ProductScreen.addControlButton({
    component: PosCustomButton,
    position: ["after", "SetSaleOrderButton"],
});
