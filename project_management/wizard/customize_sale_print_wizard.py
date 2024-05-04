from odoo import fields, models, api


class CustomizeSalePrintWizard(models.TransientModel):
    _name = 'customize.sale.print.wizard'
    _description = 'customize sale print wizard'
    order_lines = fields.Many2many(
        comodel_name='sale.order.line',
        string="Order Lines",
     )
    order_id=fields.Many2one('sale.order', 'order_id')


    def print_report(self):
           return  self.print_customize_qweb_report()

    def print_customize_qweb_report(self):
        print(self.order_id)
        return self.env.ref('sale.action_report_saleorder').report_action(self.order_id)

