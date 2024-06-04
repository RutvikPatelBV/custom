/** @odoo-module */
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { ExpenseListController } from '@hr_expense/views/list';
//const { ListController } = owl;
//const { xml } = owl;
class HrExpenseListController extends ListController{
    setup() {
        super.setup();
        console.log("This is work now");
    }
    action_custom(){
    alert("Jay Shree Ram");}
    }
//HrExpenseListController.template=Practice.new_hr_expense_Buttons
export const hrExpenseListView = {
    ...listView,
    Controller: HrExpenseListController,
    buttonTemplate: "Practice.hrExpenseListView.Buttons.new",
};

// Register the custom view
registry.category("views").add("hr_expense_inherited_list_view", hrExpenseListView);