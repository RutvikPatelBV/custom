from datetime import datetime
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class Practice(models.Model):
    _name = 'practice.practice'
    _description = 'for practice model exersice'

    seq = fields.Char( default=lambda self: _('New'),
                      copy=False, readonly=True, required=True)
    name = fields.Char(string='Name')
    dob = fields.Date(string="Date Of Birth", required=True)
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    email = fields.Char(string="Email", default="abcd1234@gmail.com", required=True)
    associated_company_id = fields.Many2one(
        comodel_name='practice.company',
        string='Associated Company',
        required=False)

    @api.model
    def create(self, vals):
        if vals.get('seq', _("New")) == _("New"):
            vals['seq'] = self.env['ir.sequence'].next_by_code('practice.seq') or _("New")
        res = super(Practice, self).create(vals)
        return res

    @api.depends('dob')
    def _compute_age(self):
        today = datetime.today()
        print(today)
        for rec in self:
            if rec.dob:
                rec.age = today.year - rec.dob.year
            else:
                rec.age = 0

    @api.onchange('dob')
    def check_dob(self):
        for rec in self:
            if rec.dob == datetime.today().date():
                raise ValidationError(_("DOB must not be today"))

    def send_mail(self):
        template = self.env.ref('Practice.new_practice_emp_mail_template')
        ctx = {
            'default_model': 'practice.practice',
            'default_res_ids': self.ids,
            'default_template_id': template if template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
    # Not have any use but for removing error of not find _get_customer_info()
    def _get_customer_information(self):
        # Implement this method to return the necessary customer information
        # Example implementation:
        return {
            'customer_name': self.name,
            'customer_email': self.email,
            'associated_company': self.associated_company_id.name if self.associated_company_id else ''
        }