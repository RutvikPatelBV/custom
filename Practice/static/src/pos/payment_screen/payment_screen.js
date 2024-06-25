/**@odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
//import { CustomAlertPopup } from "@pos_buttons/js/PopUp/pos_pop_up";
import { patch } from "@web/core/utils/patch";
import {useState} from "@odoo/owl";

patch(PaymentScreen.prototype, {
setup(){
this.state=useState({value:0})
super.setup()
console.log("Jay Shree Ram From Payment")
},
async onClick() {
alert(`Jay Shree Ram From Payment ${this.state.value}`)
this.state.value++
}
})


//add service which give notification every 5 second:

//import { registry } from "@web/core/registry";
//
//const serviceRegistry = registry.category("services");
//
//const myService = {
//    dependencies: ["notification"],
//    start(env, { notification }) {
//        let counter = 1;
//        setInterval(() => {
//            notification.add(`Tick Tock ${counter++}`);
//        }, 5000);
//    }
//};
//
//serviceRegistry.add("myService", myService);