/** @odoo-module */
import { PlanningGanttController } from "@planning/views/planning_gantt/planning_gantt_controller";
import { patch } from "@web/core/utils/patch";
import { jsonrpc } from "@web/core/network/rpc_service";
patch(PlanningGanttController.prototype,{
    async custom_button_action() {
    alert("Jay Shree Ram")}
})