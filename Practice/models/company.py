from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Company(models.Model):
    _name = 'practice.company'
    _description = 'Company Model'

    seq = fields.Char(default=lambda self: _('New'), copy=False, readonly=True, required=True)
    name = fields.Char(string="Name", required=True)
    associated_emp_ids = fields.One2many(
        comodel_name='practice.practice',
        inverse_name='associated_company_id',
        string='Associated Employee',
        required=False,
        readonly=True
    )
    display_name = fields.Char(compute="_compute_display_name")
    work_count = fields.Integer(string="Work Count", compute="compute_work")
    is_licenced = fields.Boolean(string="Have Licence")
    allocated_equipments = fields.One2many(comodel_name='practice.equipment.allocate.line',
                                              inverse_name='allocated_company_id',
                                              string='Allocated Equipment',
                                              required=False)
    # name_of_equipment=fields.Many2one('practice.equipment')

    @api.depends('seq', 'name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.seq or ''}-{rec.name or ''}"

    @api.model
    def create(self, vals):
        if vals.get('seq', _("New")) == _("New"):
            vals['seq'] = self.env['ir.sequence'].next_by_code('company.seq') or _("New")
        res = super(Company, self).create(vals)
        if vals.get('is_licenced', False):
            licence_company_obj = self.env['practice.licenced.company']
            licence_company_obj.create({
                'seq': res.seq,
                'name': res.name,
                # Include any other necessary fields for practice.licenced.company
            })
        return res

    @api.onchange('is_licenced')
    def for_change_in_licence(self):
        if not self.is_licenced:
            record = self.env['practice.licenced.company'].search([('seq', '=', self.seq)])
            if record:
                record.unlink()
        elif self.is_licenced:
            licence_company_obj = self.env['practice.licenced.company']
            existing_record = licence_company_obj.search([('seq', '=', self.seq)])
            if not existing_record:
                vals = {
                    'seq': self.seq,
                    'name': self.name,
                    # Include any other necessary fields for practice.licenced.company
                }
                licence_company_obj.create(vals)

    # @api.depends('associated_emp_ids')
    def compute_work(self):
        for rec in self:
            rec.work_count = self.env['practice.work'].search_count([('work_to_company_id', '=', rec.id)])

    def action_open_work_from_company(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Total Work',
            'res_model': 'practice.work',
            'domain': [('work_to_company_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }

    class EquipmentAllocateLine(models.Model):
        _name = 'practice.equipment.allocate.line'
        _description = 'Equipment Allocate Line Model'

        name_of_equipment = fields.Many2one('practice.equipment')
        qty=fields.Integer(string="Quantity")
        price_per_unit = fields.Integer(string="Price per unit" , related="name_of_equipment.price_per_unit")
        allocated_company_id = fields.Many2one('practice.company')
        total_amount=fields.Integer(string="Total Amount" , compute="_compute_total_amount")
        is_paid=fields.Selection( [('paid', 'Payment Done'), ('unpaid', 'Payment Remaining')] ,string="Payment Status")
        is_paid=fields.Selection( [('paid', 'Payment Done'), ('unpaid', 'Payment Remaining')] ,string="Payment Status")

        @api.depends('qty')
        def _compute_total_amount(self):
            for rec in self:
                if rec.qty:
                    rec.total_amount=rec.qty*rec.price_per_unit
                else:
                    rec.total_amount=0


        @api.onchange('qty')
        def check_qty(self):
            for rec in self:
                if rec.qty>rec.name_of_equipment.qty:
                    raise ValidationError(_(f"{rec.name_of_equipment.name} is Only {rec.name_of_equipment.qty} available"))

        # @api.onchange('field_name')
        # def onchange_method(self):
        #     self.field_name = ''
