from odoo import models, fields
class CustomWebFormAuth(models.Model):
    _name = 'custom.web.form.auth'
    _description="custom_web_form_auth"
    name = fields.Many2one('res.partner')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    message = fields.Text(string='message')
