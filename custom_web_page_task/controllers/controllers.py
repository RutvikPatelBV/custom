from odoo import http
from odoo.http import request,Response
from werkzeug.exceptions import  Forbidden
class CustomPageController(http.Controller):

    @http.route('/custom_route', type='http', auth="public", website=True)
    def custom_page_route(self, **kwargs):
        return  request.render("custom_web_page_task.custom_page")