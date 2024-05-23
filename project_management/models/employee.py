from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class Employee(models.Model):
    _name = 'pms.employee'
    _description = 'Employee details'
    _rec_name = 'emp_name'
    emp_id = fields.Char(
        string="Employee Id",
        required=True, copy=False, readonly=False,
        default=lambda self: _('New'))
    sequ = fields.Integer('sequence')
    emp_name = fields.Char(string='Name', required=True)
    emp_role = fields.Selection(
        [('frontend_developer', 'Frontend Developer'), ('backend_developer', 'Backend Developer'),
         ('designer', 'Designer'), ('qa_tester', 'QA Tester')], string="Role", required=True)
    emp_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], string="Gender",
                                  required=True)
    joining_date = fields.Date(string='Joining Date', required=True)
    emp_email = fields.Char(string='Email', required=True, default="abcd@gmail.com")
    emp_experience = fields.Integer(string='Experience', compute='_compute_experience', store=True,
                                    help="This is automaticly calculate based on joining date")
    emp_photo = fields.Binary(string='Photo')
    emp_address = fields.Text(string='Address', required=True)
    emp_dob = fields.Date(string='Date Of Birth', required=True)
    emp_age = fields.Integer(string='Age', compute="_compute_age_of_employee")
    emp_salary = fields.Monetary(string='Salary', required=True)
    currency_id = fields.Many2one('res.currency')
    emp_country = fields.Char(string="Country", required=True)
    emp_country_new = fields.Many2one('res.country', string="Country")
    emp_extra_achievements = fields.Html(string="Extra Achievements")
    emp_hobby = fields.Char(string="Hobby")
    emp_in_team = fields.Integer(string='In How many team', compute='find_how_many_team_no')

    # display_name=fields.Char(compute="_compute_display_name")
    # def _compute_display_name(self):
    #     for rec in  self:
    #         rec.display_name=f"{rec.emp_id or ''}-{rec.emp_name or ''}"

    # @api.model
    # def name_search(self,name,args=None,limit=100,operator='ilike'):
    #     args=args or []
    #     domain=['|',('emp_id',operator,name),('emp_name',operator,name)]+args
    #     record=self.search(domain,limit=limit)
    #     return record.name_get()

    @api.constrains('emp_dob', 'joining_date')
    def _check_date(self):
        for record in self:
            if record.emp_dob > record.joining_date:
                raise ValidationError(_("Entered joining date is wrong"))

    @api.model
    def birthday_wise(self):
        today = date.today()
        print(today.month, today.day)
        employee_with_birthday = self.search([('emp_dob', '!=', False),
                                              ('emp_dob', '!=', None),
                                              ('emp_dob', 'like', f'%-{today.month:02d}-{today.day:02d}')])
        print(employee_with_birthday)
        for employee in employee_with_birthday:
            print(employee)
            print(employee.emp_name)
            print(employee.emp_email)
            self.env['mail.mail'].create({
                'subject': "Happy Birthday!",
                'body_html': f"<p>Happy Birthday, {employee.emp_name}!</p>",
                'email_to': employee.emp_email,
            }).send()

    def find_how_many_team_no(self):
        self.emp_in_team = self.env['pms.team'].search_count([('team_member_ids.emp_id', '=', self.emp_id)])
        print(self.emp_in_team)

    def action_open_team(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'In no of team',
            'res_model': 'pms.team',
            'domain': [('team_member_ids.emp_id', '=', self.emp_id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def orm_test(self):
        res = self.env['pms.employee'].search([('emp_gender', '=', 'male')])
        res_browse = self.env['pms.employee'].browse([1, 2])
        res_count1 = self.env['pms.employee'].search_count([('emp_gender', '=', 'male')])
        res_count2 = self.env['pms.project'].search_count([('project_status', '=', 'completed')])
        print(res)
        print(res_browse)
        for i in res_browse:
            print(i['emp_name'])
        print(res_count1)
        print(res_count2)
        print(type(res))
        print(type(res_browse))
        print(type(res_count1))
        print(type(res_count2))
        print(type(self.env['pms.employee']))
        print(type(type(res_browse)))

    @api.depends('joining_date')
    def _compute_experience(self):
        for emp in self:
            if emp.joining_date:
                # Calculate the difference between the current date and the joining date
                join_date = fields.Date.from_string(emp.joining_date)
                today = datetime.today().date()
                emp_experience = today.year - join_date.year - (
                            (today.month, today.day) < (join_date.month, join_date.day))
                emp.emp_experience = emp_experience
            else:
                emp.emp_experience = 0

    @api.depends('emp_dob')
    def _compute_age_of_employee(self):
        today = date.today()
        for emp in self:
            if emp.emp_dob and emp.emp_dob.year < today.year:
                emp.emp_age = today.year - emp.emp_dob.year
            else:
                emp.emp_age = 0

    @api.model
    def create(self, vals):
        if vals.get('emp_id', _("New")) == _("New"):
            vals['emp_id'] = self.env['ir.sequence'].next_by_code('pms.employee_seq') or _("New")
        res = super(Employee, self).create(vals)
        return res

    def use_group_read(self):
        domain = [('emp_gender', '=', 'male')]
        groupby = ['emp_role', 'emp_country']
        fields = ['emp_name', 'emp_id']
        summary_data = self.env['pms.employee'].read_group(domain, groupby, fields)
        print(summary_data)
        for data in summary_data:
            print(data)
