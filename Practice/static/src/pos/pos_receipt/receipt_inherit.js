/** @odoo-module */

import { Order, Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
   export_for_printing() {
       const result = super.export_for_printing(...arguments);
       if (this.new_note) {
           result.headerData.new_note = this.new_note;
       }
       if (this.location){
           result.headerData.location = this.location;
       }
       return result;
   },
});