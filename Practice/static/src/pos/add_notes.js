/* @odoo-module */

import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { TextAreaPopup } from "@point_of_sale/app/utils/input_popups/textarea_popup";
import { jsonrpc } from "@web/core/network/rpc_service";

class AddNotes extends Component {
    static template = "point_of_sale.AddNotesButton";

    setup() {
        super.setup()
        this.popup = useService("popup");
        this.pos = useService("pos");
        console.log('hello world');
    }

    async onAddItemNote() {
        const order = this.pos.get_order()
        if (!order) {
            this.popup.add(ErrorPopup, {
                title: _t("OrderLine is not selected"),
                body: _t("Please select an order first!"),
            });
            return;
        }

        const { confirmed, payload: inputNote } = await this.popup.add(TextAreaPopup, {
            startingValue: order.getNewNote(),
            title: _t("Add Customer Note Here"),
        });

        if (confirmed) {
            order.setNewNote(inputNote);

        }
    }
};

ProductScreen.addControlButton({
    component: AddNotes,
    position: ["after", "SetSaleOrderButton"],
});
