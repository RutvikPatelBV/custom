import base64

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import io
import xlsxwriter


# from odoo.tools.misc import xlsxwriter as xlsxwriter


class ProjectXlsxReport(models.TransientModel):
    _name = 'project.xlsx.report'
    _description = 'Project Report Xslx Wizard'

    file = fields.Binary('Prepared file', readonly=True, attachment=True)
    file_name = fields.Char('File Name', readonly=True)


    def print_project_xlsx_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Project Report')
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
        sheet.merge_range('A1:J1', f'Project Report', title_format)
        sheet.set_row(0, 40)
        sheet.set_row(1, 30)
        # Set column widths
        # sheet1
        sheet.set_column('A:A', 32) #pname
        sheet.set_column('B:B', 16) #pdescription
        sheet.set_column('C:C', 16) #pstart
        sheet.set_column('D:D', 16) #pend
        sheet.set_column('E:E', 16) #pbudget
        sheet.set_column('F:F', 14) #ppriority
        sheet.set_column('G:G', 14) #pmanager
        sheet.set_column('H:H', 14) #tname
        sheet.set_column('I:I', 14) #tstatus
        sheet.set_column('J:J', 8) #tworking

        sheet.write(1, 0, 'Project Name', heading_format)
        sheet.write(1, 1, 'Project Description', heading_format)
        sheet.write(1, 2, 'Project Start Date', heading_format)
        sheet.write(1, 3, 'Project End Date', heading_format)
        sheet.write(1, 4, 'Project Budget', heading_format)
        sheet.write(1, 5, 'Project Priority', heading_format)
        sheet.write(1, 6, 'Project Manager', heading_format)
        sheet.write(1, 7, 'Task Name', heading_format)
        sheet.write(1, 8, 'Task Status', heading_format)
        sheet.write(1, 9, 'Team Working', heading_format)

        project_data=self.env['pms.project.report.sql.query'].search([])

        row=2
        for project in project_data:
            sheet.write(row, 0, project.project_name or '', cell_format)
            sheet.write(row, 1, project.project_description or '', cell_format)
            sheet.write(row, 2, project.project_start_date  or '', date_format)
            sheet.write(row, 3, project.project_end_date or '', date_format)
            sheet.write(row, 4,  f'{project.project_budget} {project.currency_id.symbol} ' or '', cell_format_amount)
            sheet.write(row, 5, dict(project._fields['priority'].selection).get(project.priority, ''), cell_format)
            sheet.write(row, 6, project.project_manager.emp_name or '', cell_format)
            sheet.write(row, 7, project.task_name or '', cell_format)
            sheet.write(row, 8, project.task_status or '', cell_format)
            sheet.write(row, 9, project.no_of_team or 0, cell_format)

            row += 1

        workbook.close()

        # Return the generated file
        output.seek(0)
        file_data = output.read()
        output.close()

        self.write({
            'file': base64.b64encode(file_data),
            'file_name': f'Project Report.xlsx'
        })
        file_name = 'Project_Report.xlsx'

        attachment = self.env['ir.attachment'].create({
            'name': file_name,
            'type': 'binary',
            'datas': base64.b64encode(file_data),
            'store_fname': file_name,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        download_url = f'/web/content/{attachment.id}?download=true'
        return {
            'type': 'ir.actions.act_url',
            'url': download_url,
            'target': 'new',
        }