from odoo import models, api, _
from odoo.exceptions import UserError

class HrExpense(models.Model):
    _inherit = 'hr.expense'

    # def calculate_total(self,recordsId):
    # browsed_records = self.env['hr.expense'].browse(recordsId)
    # amounts = []
    # for record in browsed_records:
    #     amounts.append(record.total_amount)
    # sumall = sum(amounts)
    #     return sumall
    @api.model
    def print_report(self, record_ids):
        browsed_records = self.env['hr.expense'].browse(record_ids)
        amounts = []
        for record in browsed_records:
            amounts.append(record.total_amount)
        sumall = sum(amounts)
        # Fetch the records
        expenses = self.browse(record_ids)

        # Check if report template exists
        report_template = self.env.ref('Practice.action_hr_expense_qweb_report_id')
        if not report_template:
            raise UserError("Report template not found.")
        report_action = report_template.report_action(browsed_records)
        # newDictionary={
        #     'report_action':report_action,
        #     'sumall':sumall
        # }
        # Generate the report action
        return report_action,sumall
