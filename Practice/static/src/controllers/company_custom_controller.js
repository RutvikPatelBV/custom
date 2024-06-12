/** @odoo-module **/
import { registry } from "@web/core/registry";
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";

// Extend FormController to add custom behavior
class CompanyController extends FormController {
    setup() {
        super.setup();
        console.log("Company Form controller is working now");
    }

    custom_button_action() {
        alert("Jay Shree Ram");
    }
}

// Define a custom form view with the new controller
export const customButtonFormViewCompany = {
    ...formView,
    Controller: CompanyController,
    buttonTemplate: "Practice.company_custom_button_form",
};

// Register the custom form view
registry.category("views").add("company_button_form_view", customButtonFormViewCompany);
