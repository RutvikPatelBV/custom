from odoo import fields, models, api,_


class Project(models.Model):
    _name = 'pms.project'
    _description = 'Projects Details'
    _rec_name = 'project_name'
    project_ref_id=fields.Char( string="Employee Id",required=True, copy=False, readonly=False,default=lambda self: _('New'))
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
    project_name = fields.Char(string='Project Name', required=True)
    project_description = fields.Text(string='Project Description')
    project_start_date = fields.Date(string='Project Start Date', required=True, default=fields.Datetime.now())
    project_end_date = fields.Date(string='Project End Date', required=True)
    currency_id = fields.Many2one('res.currency')
    project_budget = fields.Monetary(string='project Budget')
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High'), ('3', 'Very High'), ('4', 'Urgent')],
                                string="Project Priority")
    project_manager = fields.Many2one('pms.employee', string='Project Manager')
    project_manager_experience=fields.Integer(related='project_manager.emp_experience' , string="Project Manager Experience" ,   readonly=True)
    no_of_team=fields.Integer(string='No Of Team Working' , compute='find_no_of_team')
    display_name=fields.Char(compute='_compute_display_name')
    team_ids=fields.One2many('pms.team','assigned_project_id',string='Teams')
    # project_manager_experience = fields.Integer(string="Project Manager Experience", readonly=True)

    # @api.onchange('project_manager')
    # def on_change_project_manager(self):
    #     self.project_manager_experience = self.project_manager.emp_experience

    def _compute_display_name(self):
        for rec in self:
            rec.display_name=f"{rec.project_ref_id or ''}-{rec.project_name or ''}"


    def find_no_of_team(self):
        self.no_of_team=self.env['pms.team'].search_count([('assigned_project_id.project_ref_id','=',self.project_ref_id)])
    def state_change(self):
        list_of_sequence_state = ["new","planning","pending_approval","progress","on_hold","delayed","under_review","testing","ready_deployment","completed","cancelled","maintenance"]
        current_index=list_of_sequence_state.index(self.project_status)
        if current_index+1<len(list_of_sequence_state):
            next_state=list_of_sequence_state[current_index+1]
            self.project_status=next_state
        if self.project_status=='completed':
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Completed project ',
                    'type': 'rainbow_man',
                }
            }
        else:
            return
    @api.model
    def create(self,vals):
        if vals.get('project_ref_id',_("New"))==_("New"):
            vals['project_ref_id']=self.env['ir.sequence'].next_by_code('pms.project_seq') or _("New")
        res=super(Project,self).create(vals)
        return res

    def action_open_team_from_project(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'no of team assigned',
            'res_model': 'pms.team',
            'domain': [('assigned_project_id.project_ref_id', '=', self.project_ref_id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
    @api.model
    def name_search(self,name,operator='ilike',args=None,limit=100):
        args=args or []
        domain=['|',('project_manager',operator,name),('project_ref_id',operator,name)] + args
        record=self.search(domain,limit=limit)
        return record.name_get()
