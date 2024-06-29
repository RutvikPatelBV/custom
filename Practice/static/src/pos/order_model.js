/** @odoo-module **/

import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.new_note = this.new_note || "";
        this.discounted_order = false
    },

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        if (json) {
            json.new_note = this.new_note;
            json.discounted_order = this.discounted_order;
        }
        return json;
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.new_note = json.new_note;
        this.discounted_order = json.discounted_order;
    },

    getNewNote() {
        return this.new_note;
    },

    setNewNote(note) {
        this.new_note = note || "";
    },
});

