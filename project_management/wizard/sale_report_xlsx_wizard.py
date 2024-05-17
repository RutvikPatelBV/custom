import base64

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import io
import xlsxwriter


# from odoo.tools.misc import xlsxwriter as xlsxwriter


class SaleReportXslxWizard(models.TransientModel):
    _name = 'sale.report.xslx.wizard'
    _description = 'Sale Report Xslx Wizard'

    start_date = fields.Date(string="Start Date" , required=True)
    end_date = fields.Date(string="End Date" , required=True)
    file = fields.Binary('Prepared file', readonly=True, attachment=True)
    file_name = fields.Char('File Name', readonly=True)

    @api.constrains('start_date', 'end_date')
    def check_date(self):
        for record in self:
            if record.start_date > record.end_date:
                raise ValidationError(_("Entered End Date is must be after Start Date"))

    def print_sale_report(self):

        # Create an in-memory output file for the new workbook
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Sales Report')
        heading_format = workbook.add_format({
            'bold': True,
            'border': 1,
            'font_size': 12,
            'valign': 'vcenter',
            'align': 'center',
            'text_wrap': True,
            'bg_color': '#98ABEE',
            'color': '#201658'
        })
        title_format = workbook.add_format({
            'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#201658',
            'color': '#98ABEE', 'num_format': 'dd-mm-yyyy'
        })
        date_format = workbook.add_format({
            'border': 1, 'num_format': 'dd-mm-yyyy',
            'color': '#201658',
            'bg_color': '#EEF5FF'
        })
        cell_format = workbook.add_format({
            'border': 1,
            'text_wrap': True,
            'color': '#201658',
            'bg_color': '#EEF5FF'
        })
        cell_format_amount = workbook.add_format({
            'border': 1,
            'text_wrap': True,
            'num_format': '#,##0.00',
            'align': 'right',
            'color': '#201658',
            'bg_color': '#EEF5FF'
        })
        sheet.merge_range('A1:G1', f'Sales Report from {self.start_date} to {self.end_date}', title_format)
        sheet.set_row(0, 40)
        sheet.set_row(1, 30)
        # Set column widths
        # sheet1
        sheet.set_column('A:A', 8)
        sheet.set_column('B:B', 16)
        sheet.set_column('C:C', 34)
        sheet.set_column('D:D', 14)
        sheet.set_column('E:E', 16)
        sheet.set_column('F:F', 25)
        sheet.set_column('G:G', 16)

        sheet.write(1, 0, 'id', heading_format)
        sheet.write(1, 1, 'Name', heading_format)
        sheet.write(1, 2, 'Email', heading_format)
        sheet.write(1, 3, 'Order Date', heading_format)
        sheet.write(1, 4, 'Sales Person', heading_format)
        # sheet.write(1, 5, 'Company', heading_format)
        sheet.write(1, 5, 'Invoice Status', heading_format)
        sheet.write(1, 6, 'Order Value', heading_format)

        # Sample data fetching
        sales = self.env['sale.order'].search(
            [('date_order', '>=', self.start_date), ('date_order', '<=', self.end_date)])


        row = 2
        for sale in sales:
            sheet.write(row, 0, sale.name or '', cell_format)
            sheet.write(row, 1, sale.partner_id.name or '', cell_format)
            sheet.write(row, 2, sale.partner_id.email or '', cell_format)
            sheet.write(row, 3, sale.date_order or '', date_format)
            sheet.write(row, 4, sale.user_id.name or '', cell_format)
            # sheet.write(row, 5, sale.company_id.name or '', cell_format)
            sheet.write(row, 5, dict(sale._fields['invoice_status'].selection).get(sale.invoice_status, ''),
                        cell_format)
            sheet.write(row, 6, f'{sale.amount_total} {sale.currency_id.symbol} ' or '', cell_format_amount)

            row += 1
        # sheet2
        sheet2 = workbook.add_worksheet('Invoice Report')
        invoices = self.env['account.move'].search(
            [('invoice_date', '>=', self.start_date), ('invoice_date', '<=', self.end_date)])
        sheet2.merge_range('A1:F1', f'Invoice Report from {self.start_date} to {self.end_date}', title_format)
        sheet2.set_row(0, 40)
        sheet2.set_row(1, 30)

        sheet2.set_column('A:A', 20)
        sheet2.set_column('B:B', 34)
        sheet2.set_column('C:C', 34)
        sheet2.set_column('D:D', 14)
        sheet2.set_column('E:E', 14)
        sheet2.set_column('F:F', 16)

        sheet2.write(1, 0, 'Number', heading_format)
        sheet2.write(1, 1, 'Customer', heading_format)
        sheet2.write(1, 2, 'Invoice Date', heading_format)
        sheet2.write(1, 3, 'Due Date', heading_format)
        sheet2.write(1, 4, 'Tex', heading_format)
        sheet2.write(1, 5, 'Total', heading_format)

        row = 2
        for invoice in invoices:
            sheet2.write(row, 0, invoice.name or '', cell_format)
            sheet2.write(row, 1, invoice.invoice_partner_display_name or '', cell_format)
            sheet2.write(row, 2, invoice.invoice_date or '', date_format)
            sheet2.write(row, 3, invoice.invoice_date_due or '', date_format)
            sheet2.write(row, 4, f' {invoice.amount_untaxed_signed} {invoice.currency_id.symbol}' or '', cell_format_amount)
            sheet2.write(row, 5, f'{invoice.amount_total_signed} {invoice.currency_id.symbol}' or '', cell_format_amount)
            row += 1

        workbook.close()

        # Return the generated file
        output.seek(0)
        file_data = output.read()
        output.close()

        self.write({
            'file': base64.b64encode(file_data),
            'file_name': f'{self.start_date} to {self.end_date}.xlsx'
        })
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=%s&id=%s&field=file&download=true&filename=%s' % (
                self._name, self.id, self.file_name),
            'target': 'new',
        }