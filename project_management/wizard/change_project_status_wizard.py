from odoo import fields, models, api


class ChangeProjectStatusWizard(models.TransientModel):
    _name = 'change.project.status.wizard'
    _description = 'project status change wizard'

    project_status = fields.Selection([
        ('new', 'New/Initiated'),
        ('planning', 'In Planning'),
        ('pending_approval', 'Pending Approval'),
        ('progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('delayed', 'Delayed'),
        ('under_review', 'Under Review'),
        ('testing', 'In Testing'),
        ('ready_deployment', 'Ready for Deployment'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('maintenance', 'Maintenance')
    ], default="new", string="Project Status", required=True)

    def change_status(self):
        records=self.env['pms.project'].browse(self._context.get('active_ids'))
        for rec in records:
            rec.update({'project_status': self.project_status})
        return True
