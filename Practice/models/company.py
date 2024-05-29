from odoo import models,fields,api,_
class Company(models.Model):
    _name = 'practice.company'
    _description = 'company model'

    seq = fields.Char(default=lambda self: _('New'),
                      copy=False, readonly=True, required=True)
    name=fields.Char(string="name" , required=True)

    associated_emp_ids = fields.One2many(
        comodel_name='practice.practice',
        inverse_name='associated_company_id',
        string='Associated Employee',
        required=False)
    display_name=fields.Char(compute="_compute_display_name")
    work_count=fields.Integer(string="Work Count", compute="compute_work")
    is_licenced=fields.Boolean(string="Have Licence")


    def _compute_display_name(self):
        for rec in self:
            rec.display_name= f"{rec.seq or ''}-{rec.name or ''}"


    @api.model
    def create(self, vals):
        if vals.get('seq', _("New")) == _("New"):
            vals['seq'] = self.env['ir.sequence'].next_by_code('company.seq') or _("New")
        if vals['is_licenced']==True:
            print("Yes")
            licence_company_obj = self.env['practice.licenced.company']
            licence_company_obj.create(vals)
        res = super(Company, self).create(vals)
        return res
    @api.onchange('is_licenced')
    def for_unlink(self):
        if self.is_licenced==False:
            record=self.env['practice.licenced.company'].search([('seq', '=', self.seq)])
            print(record)
            record.unlink()


    def compute_work(self):
        for rec in self:
            # print(rec.seq)
            rec.work_count=self.env['practice.work'].search_count([('work_to_company_id.id','=',rec.id)])
            # print(rec.work_count)
    def action_open_work_from_company(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Total Work',
            'res_model': 'practice.work',
            'domain': [('work_to_company_id.id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
