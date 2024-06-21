/** @odoo-module **/
import { registry } from "@web/core/registry";
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";

// Extend FormController to add custom behavior
class CustomButtonFormController extends FormController {
    setup() {
        super.setup();
        console.log("Form controller is working now");
    }

    custom_button_action() {
        alert("Jay Shree Ram");
    }
}

// Define a custom form view with the new controller
CustomButtonFormController.template="Practice.sale_order_custom_button_form"
export const customButtonFormView = {
    ...formView,
    Controller: CustomButtonFormController,
//    buttonTemplate: "Practice.sale_order_custom_button_form",
};

// Register the custom form view
registry.category("views").add("custom_button_form_view", customButtonFormView);
