from odoo import fields, models, api


class CustomizeSalePrintWizard(models.TransientModel):
    _name = 'customize.sale.print.wizard'
    _description = 'customize sale print wizard'
    order_lines = fields.Many2many(
        comodel_name='sale.order.line',
        string="Order Lines",
    )

    @api.model
    def default_get(self, fields):
        res = super(CustomizeSalePrintWizard, self).default_get(fields)
        active_id = self._context.get('active_id')
        if active_id:
            sale_order = self.env['sale.order'].browse(active_id)
            res['order_lines'] = [(6, 0, sale_order.order_line.ids)]
        return res


    def print_report(self):
           pass

