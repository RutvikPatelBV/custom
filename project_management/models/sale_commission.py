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
    # For Scheduler Which is sent monthly report
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
    # def action_cancel(self):
    #     if self.enable_cancel == 'no':
    #         raise UserError(_("fist you need to enable cancel by selecting yes"))
    def action_cancel(self):
        sale_commission_online_obj = self.env['sale.commission.on.line']
        lines_to_delete = sale_commission_online_obj.search([('number', '=', self.name)])
        lines_to_delete.unlink()
        print(self.name)
        # lines_to_delete.unlink()
        res = super()._action_cancel()
        return res
class ResPartner(models.Model):
    _inherit = 'res.partner'
    # sale_order_ids = fields.One2many('sale.order', 'commission_id', string='Sale Orders',compute='calculate_orders')
    percent_commission = fields.Integer(string='Percentage', default=16 , store=True)
    order_value = fields.Float(string='If Cart Value Above' , store=True)
    sale_ids = fields.One2many('sale.order', 'partner_id', string='sales Details')
    total=fields.Float(compute="_compute_total")
    # is_vendor_category = fields.Boolean(string="Is Vendor Category", compute='_compute_is_vendor_category_field')
    def _compute_total(self):
        total=0
        for item in self.sale_ids:
            total=total+item.amount_total
        self.total=round(total,2)

    def calculate_orders(self):
        if self.name:
            print(self.name)
            list_of_order = self.env['sale.order'].search([('user_id.name', '=', self.name)])
            for item in list_of_order:
                print(item)
            self.sale_order_ids = [(6, 0, list_of_order.ids)]
        else:
            self.sale_order_ids = [(5, 0, 0)]
    def print_mail(self):
        template= self.env.ref('project_management.email_customer_template')
        print(template)
        # for rec in self:
        #     template.send_mail(rec.id)
        ctx = {
            'default_model': 'res.partner',
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
    #THIS IS TEG BASED VENDOR FILTER FOR BUTTON
    # @api.depends('category_id')
    # def _compute_is_vendor_category_field(self):
    #     teg_list=[]
    #     for partner in self:
    #         if partner.category_id:
    #             for item in partner.category_id:
    #                 print(item.name)
    #                 if 'Vendor'in teg_list or 'Desk Manufacturers'  in teg_list or 'Office Supplies'in teg_list:
    #                     partner.is_vendor_category=True
    #                 elif not partner.is_vendor_category:
    #                     partner.is_vendor_category = item.name in ['Vendor', 'Desk Manufacturers', 'Office Supplies']
    #                 teg_list.append(item.name)
    #                 print(teg_list)
    #         else:
    #             partner.is_vendor_category = False
