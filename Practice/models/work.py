from odoo import models,fields,api,_
class Company(models.Model):
    _name = 'practice.work'
    _description = 'work model'


    name=fields.Char(string="name" , required=True)
    work_to_company_id=fields.Many2many('practice.company','work_company_rel','work_id','company_id',string='Associate to company')