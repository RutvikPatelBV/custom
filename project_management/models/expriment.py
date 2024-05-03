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

from odoo.exceptions import ValidationError


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
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for line in order.order_line:
                if not line.is_available:
                    raise ValidationError("One or more products in the order are not available in sufficient quantity.")
        return res
    def button_method_name(self):
        pass
class StockPickingInherite(models.Model):
    _inherit = 'stock.picking'
    nick_name = fields.Char(string="Nick Name2" , related='sale_id.nick_name')


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    custom_name = fields.Char(string="custom name")
    is_available = fields.Boolean(string="Is Available", compute="_compute_available_or_not" )

    @api.depends('product_uom_qty', 'order_id.partner_id')
    def _compute_available_or_not(self):
        for rec in self:
            product = rec.product_id
            print('>>>>>>>>>>>>>>>>>>>>>>p',product)
            if product:
                product_tmpl_id = product.product_tmpl_id
                print('>>>>>>>>>>>>>>>>>>>ptid',product_tmpl_id)
                virtual_available = self.env['product.template'].browse(product_tmpl_id.id).virtual_available
                rec.is_available = rec.product_uom_qty <= virtual_available
            else:
                rec.is_available = False


    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLineInherit, self)._prepare_procurement_values(group_id)
        values.update({
            'custom_name': self.custom_name,
            'nike_name': self.order_id.nick_name,
        })
        return values


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        fields = super(StockRule, self)._get_custom_move_fields()
        fields += ['custom_name', 'nick_name']
        return fields


class StockMoveInherit(models.Model):
    _inherit = 'stock.move'
    custom_name = fields.Char(string="custom name")
