from odoo import fields, models, api

class Task(models.Model):
    _name = 'pms.task'
    _description = 'Task Details'
    _rec_name='task_name'

    task_name = fields.Char(string='Task Name', required=True)
    task_status = fields.Selection([
    ('new', 'New/To Do'),
    ('in_progress', 'In Progress'),
    ('blocked', 'Blocked'),
    ('on_hold', 'On Hold'),
    ('deferred', 'Deferred'),
    ('ready_testing', 'Ready for Testing'),
    ('in_testing', 'In Testing'),
    ('in_review', 'In Review'),
    ('completed', 'Completed'),
    ('reopened', 'Reopened'),
    ('cancelled', 'Cancelled'),
], string='Task Status', default='new')

    related_project_id = fields.Many2one('pms.project', string='Related Project', store=True)
    task_description = fields.Text(string='Task Description', required=True)
    depended_task_ids = fields.Many2many('pms.task', 'task_dependency_rel', 'task_id', 'depend_on_id', string='Depended On')

    _sql_constraints = [
        ('task_name_unique', 'UNIQUE(task_name)', 'Task name must be unique!'),
    ]
