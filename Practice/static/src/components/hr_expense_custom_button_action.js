/** @odoo-module */
import { ExpenseListController } from '@hr_expense/views/list';
import { patch } from "@web/core/utils/patch";
import { jsonrpc } from "@web/core/network/rpc_service";

// Patch the ExpenseListController to add a custom button action
patch(ExpenseListController.prototype, {
    async custom_button_action() {
        console.log(this)
        const selectedRecords = this.model.root.selection.map((datapoint) => datapoint.resId);
        console.log('Selected Record IDs:', selectedRecords);
        if (!selectedRecords.length) {
            this.notification.add('Please select at least one record.', {
                title: 'No records selected',
                type: 'warning',
            });
            return;
        }

        try {
            const result = await jsonrpc('/web/dataset/call_kw', {
                model: 'hr.expense',
                method: 'print_report',
                args: [selectedRecords],
                kwargs: {},
            });
            const [reportAction, totalSum] = result
            alert(`Total expense of selected record ${totalSum}`)
            // Trigger the download of the generated PDF report
            if (result) {
                await this.actionService.doAction(reportAction, {});
            }
        } catch (error) {
            console.error('RPC Query Error:', error);
        }
    }
});
