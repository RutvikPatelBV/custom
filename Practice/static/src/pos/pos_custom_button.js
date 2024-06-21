/* @odoo-module */

import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";


class PosCustomButton extends Component {
    static template = "point_of_sale.PosCustomButton";

    setup() {
        this.popup = useService("popup");
        this.pos = useService("pos");
        console.log('hello world');
    }
    async onClickClear(){
            const selectedLine = this.pos.get_order().get_selected_orderline();
            if (selectedLine){
            this.pos.get_order().removeOrderline(selectedLine);
            console.log(selectedLine)
            }


//         this.popup.add(ErrorPopup, {
//            title: _t("Test Clicked"),
//            body: _t("Custom Popup."),
//        });
    }
    async onClickClearAll(){
            const selectedLines = this.pos.get_order().get_orderlines();
            console.log(selectedLines)
        if (selectedLines){
         this.popup.add(ErrorPopup, {
            title: _t("All Order is Removed"),
            body: _t("Orderlines is now empty."),
        });
        for (const line of  selectedLines) {
            if (line) {
                this.pos.get_order().removeOrderline(line);
            }
        }
        }
    }
};

ProductScreen.addControlButton({
    component: PosCustomButton,
    position: ["after", "SetSaleOrderButton"]
});


//get_orderlines() {
//        const orderlines = super.get_orderlines(this, arguments);
//        const rewardLines = [];
//        const nonRewardLines = [];
//        for (const line of orderlines) {
//            if (line.is_reward_line) {
//                rewardLines.push(line);
//            } else {
//                nonRewardLines.push(line);
//            }
//        }
//        return [...nonRewardLines, ...rewardLines];
//    }