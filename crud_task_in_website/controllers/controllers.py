# controllers/lead_controller.py
from odoo import http
from odoo.http import request

class LeadController(http.Controller):

    @http.route('/my/lead', type='http', auth='user', website=True)
    def lead_list(self, **kw):
        leads = request.env['crud.lead'].sudo().search([])
        return request.render('crud_task_in_website.lead_page', {'leads': leads})

    @http.route('/my/lead/create', type='http', auth='user', website=True)
    def lead_create(self, **kw):
        return request.render('crud_task_in_website.lead_form', {})

    @http.route('/my/lead/save', type='http', auth='user', website=True, methods=['POST'])
    def lead_save(self, **kw):
        request.env['crud.lead'].sudo().create(kw)
        return request.redirect('/my/lead')

    @http.route('/my/lead/edit/<int:lead_id>', type='http', auth='user', website=True)
    def lead_edit(self, lead_id, **kw):
        lead = request.env['crud.lead'].sudo().browse(lead_id)
        return request.render('crud_task_in_website.lead_form', {'lead': lead})

    @http.route('/my/lead/update', type='http', auth='user', website=True, methods=['POST'])
    def lead_update(self, **kw):
        lead_id = int(kw.get('id'))
        lead = request.env['crud.lead'].sudo().browse(lead_id)
        if lead:
            lead.sudo().write(kw)
        return request.redirect('/my/lead')

    @http.route('/my/lead/delete/<int:lead_id>', type='http', auth='user', website=True)
    def lead_delete(self, lead_id, **kw):
        lead = request.env['crud.lead'].sudo().browse(lead_id)
        if lead:
            lead.sudo().unlink()
        return request.redirect('/my/lead')
