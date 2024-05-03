from odoo import fields, models, api


class CustomizeSalePrintWizard(models.TransientModel):
    _name = 'customize.sale.print.wizard'
    _description = 'customize sale print wizard'
    # _inherit = 'sale.order'
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High'), ('3', 'Very High'), ('4', 'Urgent')],
                                string="Project Priority")
    # product=self.env['sale.order.line'].get.context('active_id').
    # order_line = fields.One2many(
    #     comodel_name='sale.order.line',
    #     inverse_name='order_id',
    #     string="Order Lines",
    #     copy=True, auto_join=True)
    def print_report(self):
        self.env['pms.project'].browse(self._context.get('active_id')).update({'priority': self.priority})
        return True
