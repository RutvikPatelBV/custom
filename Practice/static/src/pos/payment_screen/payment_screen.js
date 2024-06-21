/**@odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
//import { CustomAlertPopup } from "@pos_buttons/js/PopUp/pos_pop_up";
import { patch } from "@web/core/utils/patch";
patch(PaymentScreen.prototype, {
setup(){
super.setup()
console.log("Jay Shree Ram From Payment")
},
async onClick() {
alert("Jay Shree Ram From Payment")
}
})