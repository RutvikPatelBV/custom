from odoo import models, fields, api


class SaleCommission(models.Model):
    _name = 'sale.commission'
    _description = 'this have all commission details'
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        store=True
    )

    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    total_order=fields.Integer()
    total_commission=fields.Integer()
    sale_order_ids = fields.One2many('sale.commission.on.line', 'commission_id', string='Sale Orders',compute='calculate_orders')


    # @api.depends('user_id','start_date','end_date')
    def calculate_orders(self):
        if self.user_id:
            # print(self.user_id.name)
            list_of_order=self.env['sale.commission.on.line'].search([('salesperson_id.name','=',self.user_id.name),('create_date','>=',self.start_date),('create_date','<=',self.end_date)])
            # for item in list_of_order:
            #     print(item)
            self.total_order=len(list_of_order)
            self.total_commission=round(sum(order.total_commission for order in list_of_order),2)
            self.sale_order_ids=[(6, 0, list_of_order.ids)]
        else:
            self.sale_order_ids= [(5, 0, 0)]


class SaleCommissionOnline(models.Model):
    _name='sale.commission.on.line'
    _description='All about commission which is online'
    number=fields.Char(string='Number')
    customer_id = fields.Many2one('res.partner', string='Customer')
    salesperson_id = fields.Many2one(comodel_name='res.users', string="Salesperson", readonly=True)
    total_amount = fields.Float(string='Total Amount')
    create_date = fields.Datetime(string="Creation Date", index=True, readonly=True)
    order_value = fields.Integer(string='If Cart Value Above', readonly=True)
    percentage = fields.Float(string='Percentage', readonly=True)
    total_commission = fields.Float(string='Total Commission', store=True)
    commission_id = fields.Many2one('sale.commission', string='Commission')



class SaleOrder(models.Model):
    _inherit = 'sale.order'
    percent_commission = fields.Integer(string='Percentage', default=16, readonly=True)
    commission = fields.Float(string='Commission', compute="_compute_commission")
    def action_confirm(self):
        sale_commission_online_obj = self.env['sale.commission.on.line']
        for order in self:
            if order.user_id.order_value < order.amount_total:
                total_commission = order.amount_total * (order.user_id.percent_commission / 100)
            else:
                total_commission = 0
        order_data = {
            'number':self.name,
            'customer_id': self.partner_id.id,
            'salesperson_id': self.user_id.id,
            'total_amount': self.amount_total,
            'create_date': self.date_order,
            'order_value':self.user_id.order_value,
            'percentage':self.user_id.percent_commission,
            'total_commission': total_commission
        }
        print(total_commission)
        print(self.user_id.order_value)
        sale_commission_online_obj.create(order_data)
        res = super(SaleOrder, self).action_confirm()
        return res

    @api.depends('amount_total')
    def _compute_commission(self):
        for rec in self:
            rec.commission = rec.amount_total * (rec.percent_commission / 100)
class ResPartner(models.Model):
    _inherit = 'res.partner'
    # sale_order_ids = fields.One2many('sale.order', 'commission_id', string='Sale Orders',compute='calculate_orders')
    percent_commission = fields.Integer(string='Percentage', default=16 , store=True)
    order_value = fields.Float(string='If Cart Value Above' , store=True)
    def calculate_orders(self):
        if self.name:
            print(self.name)
            list_of_order = self.env['sale.order'].search([('user_id.name', '=', self.name)])
            for item in list_of_order:
                print(item)
            self.sale_order_ids = [(6, 0, list_of_order.ids)]
        else:
            self.sale_order_ids = [(5, 0, 0)]