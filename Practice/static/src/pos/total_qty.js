/** @odoo-module **/

import { OrderWidget } from "@point_of_sale/app/generic_components/order_widget/order_widget"; // Adjust the import path accordingly
import { patch } from "@web/core/utils/patch";
import { useState, onPatched, onMounted } from "@odoo/owl";

// Patch the OrderWidget component
patch(OrderWidget.prototype, {
    setup() {
        // Call the original setup method
        super.setup();
        // Initialize state with useState
        this.state = useState({ qty: 0,custom_discount:0 });

        // Function to update the quantity
        const updateQuantity = () => {
            const totalQuantity = this.props.lines.reduce((acc, line) => acc + line.quantity, 0);
            this.state.qty = totalQuantity;
//            console.log("Total quantity:", this.state.qty);
        };

        // Use onMounted to update the quantity when the component is first mounted
        onMounted(() => {
            updateQuantity();
        });

         onPatched(() => {
            updateQuantity();
        });
    },
});
