from odoo import models, fields, api
from datetime import timedelta
import io
import base64
from odoo.tools.misc import xlsxwriter

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    def xlsx_report_generator(self,start_date, end_date,sale_orders):
        # Create an in-memory output file for the new workbook
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        # Common formats
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

        # Sheet 1: Sales per Salesperson
        sheet1 = workbook.add_worksheet('Sales per Salesperson')
        sheet1.merge_range('A1:E1', f'Sales Report from {start_date} to {end_date} for {sale_orders[0].user_id.name}', title_format)
        sheet1.set_row(0, 40)
        sheet1.set_row(1, 30)
        sheet1.set_column('A:A', 14)
        sheet1.set_column('B:B', 20)
        sheet1.set_column('C:C', 14)
        sheet1.set_column('D:D', 25)
        sheet1.set_column('E:E', 16)

        sheet1.write(1, 0, 'Order Ref', heading_format)
        sheet1.write(1, 1, 'Customer', heading_format)
        sheet1.write(1, 2, 'Order Date', heading_format)
        sheet1.write(1, 3, 'Invoice Status', heading_format)
        sheet1.write(1, 4, 'Order Value', heading_format)

        row = 2
        for sale in sale_orders:
            sheet1.write(row, 0, sale.name or '', cell_format)
            sheet1.write(row, 1, sale.partner_id.name or '', cell_format)
            sheet1.write(row, 2, sale.date_order or '', date_format)
            sheet1.write(row, 3, dict(sale._fields['invoice_status'].selection).get(sale.invoice_status, ''),
                         cell_format)
            sheet1.write(row, 4, f'{sale.amount_total} {sale.currency_id.symbol}' or '', cell_format_amount)
            row += 1

        # Sheet 2: Sales per Customer
        sheet2 = workbook.add_worksheet('Product Sale Report')
        sheet2.merge_range('A1:E1', f'Sales Report from {start_date} to {end_date}', title_format)
        sheet2.set_row(0, 40)
        sheet2.set_row(1, 30)
        sheet2.set_column('A:A', 25)
        sheet2.set_column('B:B', 20)
        sheet2.set_column('C:C', 14)
        sheet2.set_column('D:D', 16)
        sheet2.set_column('E:E', 25)


        sheet2.write(1, 0, 'Product', heading_format)
        sheet2.write(1, 1, 'Unit Price', heading_format)
        sheet2.write(1, 2, 'Quantity', heading_format)
        sheet2.write(1, 3, 'Sub Total', heading_format)
        sheet2.write(1, 4, 'Total With Tax', heading_format)
        # sheet2.write(1, 3, 'Salesperson', heading_format)
        # sheet2.write(1, 4, 'Invoice Status', heading_format)
        # sheet2.write(1, 5, 'Order Value', heading_format)
        product_sales = {}
        for order in sale_orders:
            for line in order.order_line:
                product_name = line.product_id.name
                if product_name in product_sales:
                    product_sales[product_name]['unit_price'] += line.price_unit
                    product_sales[product_name]['sub_total'] += line.price_subtotal
                    product_sales[product_name]['qty'] += line.product_uom_qty
                    product_sales[product_name]['price_with_tax'] += line.price_total
                else:
                    product_sales[product_name] = {'unit_price': line.price_unit, 'sub_total': line.price_subtotal,'qty': line.product_uom_qty ,'price_with_tax':line.price_total}

        # Write data for Product-wise Sales worksheet
        row = 2
        print(product_sales)
        for product, data in product_sales.items():
            sheet2.write(row, 0, product, cell_format)
            sheet2.write(row, 1, data['unit_price'], cell_format_amount)
            sheet2.write(row, 2, data['qty'], cell_format_amount)
            sheet2.write(row, 3, data['sub_total'], cell_format_amount)
            sheet2.write(row, 4, data['price_with_tax'], cell_format_amount)
            row += 1

        # Sheet 3: Sales per Product
        # sheet3 = workbook.add_worksheet('Sales per Product')
        # sheet3.merge_range('A1:G1', f'Sales Report from {start_date} to {end_date}', title_format)
        # sheet3.set_row(0, 40)
        # sheet3.set_row(1, 30)
        # sheet3.set_column('A:A', 8)
        # sheet3.set_column('B:B', 34)
        # sheet3.set_column('C:C', 14)
        # sheet3.set_column('D:D', 16)
        # sheet3.set_column('E:E', 25)
        # sheet3.set_column('F:F', 16)
        #
        # sheet3.write(1, 0, 'ID', heading_format)
        # sheet3.write(1, 1, 'Product', heading_format)
        # sheet3.write(1, 2, 'Order Date', heading_format)
        # sheet3.write(1, 3, 'Salesperson', heading_format)
        # sheet3.write(1, 4, 'Customer', heading_format)
        # sheet3.write(1, 5, 'Order Value', heading_format)
        #
        # row = 2
        # for sale in sales:
        #     for line in sale.order_line:
        #         sheet3.write(row, 0, sale.id or '', cell_format)
        #         sheet3.write(row, 1, line.product_id.name or '', cell_format)
        #         sheet3.write(row, 2, sale.date_order or '', date_format)
        #         sheet3.write(row, 3, sale.user_id.name or '', cell_format)
        #         sheet3.write(row, 4, sale.partner_id.name or '', cell_format)
        #         sheet3.write(row, 5, f'{line.price_total} {sale.currency_id.symbol}' or '', cell_format_amount)
        #         row += 1

        workbook.close()

        # Return the generated file
        output.seek(0)
        file_data = output.read()
        output.close()

        return file_data


    def monthly_sale_report(self):
        # Get today's date
        today = fields.Date.today()

        # Calculate first day and last day of the current month
        first_day_of_current_month = today.replace(day=1)
        last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_last_month = last_day_of_last_month.replace(day=1)

        # Search for orders within the last month
        orders = self.env['sale.order'].search([
            ('date_order', '>=', first_day_of_last_month),
            ('date_order', '<=', last_day_of_last_month)
        ])


        # Group orders by customer
        sale_orders_dict = {}
        for order in orders:
            if order.user_id in sale_orders_dict:
                sale_orders_dict[order.user_id].append(order)
            else:
                sale_orders_dict[order.user_id] = [order]

        for sale, sale_orders in sale_orders_dict.items():
            # Prepare email content
            # Generate the report for the last month
            file_data = self.xlsx_report_generator(first_day_of_last_month, last_day_of_last_month,sale_orders)
            attachment_name = f'Sales_Report_{first_day_of_last_month}_to_{last_day_of_last_month}.xlsx'

            # Prepare and send the email
            attachment_data = {
                'name': attachment_name,
                'datas': base64.b64encode(file_data),
                'res_model': 'mail.compose.message',
                'res_id': 0,
            }
            mail_values = {
                'email_to': sale.email,
                'attachment_ids': [(0, 0, attachment_data)],
            }
            template = self.env.ref('project_management.monthly_report_mail_template')
            if mail_values['email_to']==sale.email:
                template.send_mail(sale.id, force_send=True,
                                   email_values=mail_values)


