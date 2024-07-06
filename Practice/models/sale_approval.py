from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleApproval(models.Model):
    _name = 'sale.approval'
    _description = 'sale approval'
    name = fields.Char(
        string="Order Reference" , readonly=True)
    partner_name = fields.Char(string="Customer" , readonly=True)
    date_order = fields.Datetime(
        string="Order Date",
        required=True, copy=False,
        help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.",
        default=fields.Datetime.now,
        readonly=True)
    amount_total = fields.Monetary(string="Total", store=True, readonly=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        readonly=True
    )


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('to_approve', "To Approve"),('sale',)])

    # def action_to_approve(self):
    #     for order in self:
    #         order.state = 'to_approve'

    def action_confirm(self):
        for order in self:
            sales_limit = float(self.env['ir.config_parameter'].sudo().get_param('practice.sales_limit', default=0.0))
            if order.amount_total > sales_limit:
                order.state = 'to_approve'
                self.env['sale.approval'].create({
                    'name': order.name,
                    'partner_name': order.partner_id.name,
                    'date_order': order.date_order,
                    'amount_total': order.amount_total,
                    'currency_id': order.currency_id.id,
                })
            else:
                super(SaleOrder, self).action_confirm()

    def _can_be_confirmed(self):
        self.ensure_one()
        return self.state in {'draft', 'sent','to_approve'}
    def approve_order(self):
        print("aprrove")
        super(SaleOrder, self).action_confirm()
        current_order = self.env['sale.approval'].search([('name','=', self.name)])
        print(current_order)
        if (current_order):
            current_order.unlink()


