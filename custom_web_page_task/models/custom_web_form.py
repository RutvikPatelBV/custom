from odoo import models, fields
class CustomWebForm(models.Model):
    _name = 'custom.web.form'
    _description="custom_web_form"
    name = fields.Many2one('res.partner')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    message = fields.Text(string='message')
