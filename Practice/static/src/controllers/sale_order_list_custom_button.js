/** @odoo-module **/
import { registry } from "@web/core/registry";
import { ListController } from "@web/views/list/list_controller";
import { listView } from "@web/views/list/list_view";

// Extend ListController to add custom behavior
class CustomButtonListController extends ListController {
    setup() {
        super.setup();
        console.log("This is working now");
    }

    custom_button_action() {
        alert("Jay Shree Ram");
    }
}

// Define a custom list view with the new controller
export const customButtonListView = {
    ...listView,
    Controller: CustomButtonListController,
    buttonTemplate: "Practice.sale_order_custom_button_tree",
};

// Register the custom list view
registry.category("views").add("custom_button_list_view", customButtonListView);
