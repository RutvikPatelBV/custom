from odoo import models,fields,api,_
class LicencedCompany(models.Model):
    _name = 'practice.licenced.company'
    _description = 'licenced company model'

    seq = fields.Char(default=lambda self: _('New'),
                      copy=False, readonly=True, required=True)
    name=fields.Char(string="name" , required=True)

    associated_emp_ids = fields.One2many(
        comodel_name='practice.practice',
        inverse_name='associated_company_id',
        string='Associated Employee',
        required=False)
    # work_count=fields.Integer(string="Work Count", compute="compute_work")
    # is_licenced=fields.Boolean(string="Have Licence")
