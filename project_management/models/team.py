from odoo import fields,models,api
class Team(models.Model):

    _name='pms.team'
    _description='team deteils'

    team_name=fields.Char(string='Name',required=True)
    team_member_ids=fields.Many2many('pms.employee',string="Team Member",required=True)
    assigned_project_id=fields.Many2one('pms.project',string="Assigned Project")
    project_manager= fields.Many2one(related='assigned_project_id.project_manager', string='Project Manager', store=True)
    # @api.depends('assigned_project_ids.project_manager')
    # def _compute_project_manager(self):
    #     for team in self:
    #         project_managers = team.assigned_project_ids.mapped('project_manager')
    #         if project_managers:
    #             team.project_manager = project_managers[0]
    #         else:
    #             team.project_manager = False
