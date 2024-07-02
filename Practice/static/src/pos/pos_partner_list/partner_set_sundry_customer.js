/** @odoo-module **/

import { PartnerListScreen } from "@point_of_sale/app/screens/partner_list/partner_list";
import { patch } from "@web/core/utils/patch";

patch(PartnerListScreen.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
         this.setSundryCustomer = this.setSundryCustomer.bind(this);
        console.log("Hello from customer")
    },
     async setSundryCustomer() {
        const sundryCustomerId = 66;
        const sundryCustomer = this.pos.db.get_partner_by_id(sundryCustomerId);

        if (sundryCustomer) {
            this.state.selectedPartner = sundryCustomer;
            this.confirm();
        } else {
            this.notification.add("Sundry customer not found.", { type: "danger" });
        }
    }
});

