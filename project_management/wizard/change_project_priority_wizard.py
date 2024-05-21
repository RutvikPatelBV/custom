from odoo import fields, models, api


class ChangeProjectPriorityWizard(models.TransientModel):
    _name = 'change.project.priority.wizard'
    _description = 'project priority change wizard'

    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High'), ('3', 'Very High'), ('4', 'Urgent')],
                                string="Project Priority")

    def change_priority(self):
        records=self.env['pms.project'].browse(self._context.get('active_ids'))
        for rec in records:
            rec.update({'priority': self.priority})
        return True
