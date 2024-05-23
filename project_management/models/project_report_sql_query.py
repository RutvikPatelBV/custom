from odoo import api, fields, models


class ProjectReportSqlQuery(models.Model):
    _name = "pms.project.report.sql.query"
    _description = "Project Report In Details"

    project_ref_id = fields.Char(string="Employee Id", required=True, copy=False, readonly=False,
                                 default=lambda self: _('New'))
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
    project_manager_experience = fields.Integer(string="Project Manager Experience", readonly=True)
    no_of_team = fields.Integer(string='No Of Team Working')
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

    # Define methods to construct SQL queries
    def _select(self):
        # Construct the SELECT part of the SQL query
        return """
            pp.id,
            pp.create_uid,
            pp.write_uid,
            pp.create_date,
            pp.write_date,
            pp.project_ref_id,
            pp.project_status,
            pp.project_name,
            pp.project_description,
            pp.project_start_date,
            pp.project_end_date,
            pp.currency_id,
            pp.project_budget,
            pp.priority,
            pp.project_manager,
            pp.project_manager_experience,
            pt.task_name,
            pt.task_status,
            (SELECT COUNT(*) FROM pms_team WHERE assigned_project_id = pp.id) AS no_of_team
        """

    def _from(self):
        return """
            pms_project pp LEFT JOIN pms_task pt
            ON pt.related_project_id=pp.id 
        """

    def _where(self):
        # Construct the WHERE part of the SQL query
        pass

    def _group_by(self):
        return """
            pp.id,
            pp.project_ref_id,
            pp.project_status,
            pp.project_name,
            pp.project_description,
            pp.project_start_date,
            pp.project_end_date,
            pp.currency_id,
            pp.project_budget,
            pp.priority,
            pp.project_manager,
            pp.project_manager_experience,
            pp.id,
            pt.task_name,
            pt.task_status
        """

    def _order_by(self):
        # Construct the ORDER BY part of the SQL query
        pass

    # Define other methods as needed to compute fields or perform other tasks

    # Define a property to combine all the parts of the query
    @property
    def _table_query(self):
        return f"""
                        SELECT {self._select()}
                        FROM {self._from()}
                        
                        GROUP BY {self._group_by()}
                    """
