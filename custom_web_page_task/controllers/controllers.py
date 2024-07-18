from odoo import http
from odoo.http import request
from werkzeug.exceptions import Forbidden
from odoo.exceptions import ValidationError

class CustomPageController(http.Controller):

    @http.route('/custom_route', type='http', auth="public", website=True)
    def custom_page_route(self, **kwargs):
        all_objects = request.env['res.partner'].search([])
        values = {
            "all_objects": all_objects
        }
        return request.render("custom_web_page_task.custom_page", values)

    @http.route('/custom_route/submit', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def web_form_submit(self, **post):
        # Check if email or phone already exists
        existing_email = request.env['custom.web.form'].sudo().search([('email', '=', post.get('email'))], limit=1)
        existing_phone = request.env['custom.web.form'].sudo().search([('phone', '=', post.get('phone'))], limit=1)

        if existing_email:
            return request.render('custom_web_page_task.custom_page', {
                'error_message': 'The email address is already registered.',
                'all_objects': request.env['res.partner'].search([]),
            })

        if existing_phone:
            return request.render('custom_web_page_task.custom_page', {
                'error_message': 'The phone number is already registered.',
                'all_objects': request.env['res.partner'].search([]),
            })

        if request.env.user.id == request.env.ref('base.public_user').id:
            model = 'custom.web.form'
        else:
            model = 'custom.web.form.auth'

            # Create the new record if validation passes
        if post.get('name'):
            name_value=int(post.get('name'))
        else:
            name_value=1
        request.env[model].sudo().create({
            'name': name_value,
            'phone': post.get('phone'),
            'email': post.get('email'),
            'message': post.get('message'),
        })
        return request.redirect('/contactus-thank-you')
