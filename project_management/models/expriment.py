# from odoo import fields, models, api,_
# from  odoo.exceptions import UserError
#
#
# class Expriment(models.Model):
#     _name = 'pms.expriment'
#     _description = 'team experiment'
#
#     team_name = fields.Char(string='Name', required=True)
#     team_member_ids = fields.Many2many('pms.employee', string="Team Member", required=True)
#     assigned_project_ids = fields.Many2one('pms.project', string="Assigned Project")
#     project_manager = fields.Many2one(related='assigned_project_ids.project_manager', string='Project Manager', store=True)
#
# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#     enable_cancel = fields.Selection([('yes','yes'),('no','no')])
#
#     def action_cancel(self):
#         if self.enable_cancel=='no':
#             raise UserError(_("fist you need to enable cancel by selecting yes"))
# class SaleOrderLineInherit(models.Model):
#     _inherit='sale.order.line'
#     custom_name=fields.Char(string="custom name")
#
# class StockPickingInherit(models.Model):
#     _inherit='stock.move'
#     new_ids=fields.Many2one('sale.order.line', default='s')
#     custom_name=fields.Char(string="custom name", related="new_ids.custom_name")
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class Expriment(models.Model):
    _name = 'pms.expriment'
    _description = 'team experiment'

    team_name = fields.Char(string='Name', required=True)
    team_member_ids = fields.Many2many('pms.employee', string="Team Member", required=True)
    assigned_project_ids = fields.Many2one('pms.project', string="Assigned Project")
    project_manager = fields.Many2one(related='assigned_project_ids.project_manager', string='Project Manager',
                                      store=True)


    def recordset_operation(self):
        partner_name = self.env['res.partner'].search([])
        print('partner_name:', partner_name.mapped('phone'))

    @api.model
    def default_get(self, fields):
        res = super(Expriment, self).default_get(fields)
        lst = []
        frnt_dev = self.env['pms.employee'].search([('emp_role', '=', 'frontend_developer')], limit=1)
        for rec in frnt_dev:
            lst.append(rec.id)
        res['team_member_ids'] = [(6, 0, lst)]
        return res

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    enable_cancel = fields.Selection([('yes', 'yes'), ('no', 'no')])
    nick_name = fields.Char(string="Nick Name")

    def action_cancel(self):
        if self.enable_cancel == 'no':
            raise UserError(_("fist you need to enable cancel by selecting yes"))

class StockPickingInherite(models.Model):
    _inherit = 'stock.picking'
    nick_name = fields.Char(string="Nick Name2")

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    custom_name = fields.Char(string="custom name")
    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLineInherit, self)._prepare_procurement_values(group_id)
        values.update({
            'custom_name': self.custom_name
        })
        return values

class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        fields = super(StockRule, self)._get_custom_move_fields()
        fields += ['custom_name','nick_name' ]
        return fields
class StockMoveInherit(models.Model):
    _inherit = 'stock.move'
    custom_name = fields.Char(string="custom name")




