from odoo.exceptions import Warning
from odoo import models, fields, api, _

# class ExpenseUpdate(models.Model):
#     _inherit = 'hr.expense'
#
#
#     suspense_id = fields.Many2one('hr.suspense', string="Related Suspense")

class RecruitUpdate(models.Model):
    _name = 'recruit.update'
    _description = 'Employee suspense'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_employee_domain(self):
        employee = self.env['hr.employee'].search(
            [('user_id', '=', self.env.user.id)], limit=1)
        domain = [('id', '=', employee.id)]
        if self.env.user.has_group('hr.group_hr_user'):
            domain = []
        return domain

    name = fields.Char(string='Reference')
    job_id = fields.Many2one('hr.job', string="Job Title")
    department_id = fields.Many2one('hr.department',
                                  domain=_get_employee_domain, default=lambda self: self.env.user.employee_id.department_id, string="Requesting Department")
    education = fields.Char(string='Education')
    experience = fields.Char(string='Experience')
    date_required = fields.Date(string='Date required')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('any', 'Any')
    ], groups="hr.group_hr_user", default="male", tracking=True)
    age = fields.Char(string='Age')
    no_employees = fields.Integer(string='Number of Employees')
    additional=fields.Boolean("Additional")
    replacement = fields.Boolean("Replacement")
    recruitment_reason=fields.Char("Recruitment reason")
    state = fields.Selection([
        ('draft', 'Unconfirmed'), ('cancel', 'Cancelled'),
        ('dept', 'Dept. Approved'), ('hr', 'HR Approved'),
        ('confirm', 'GM Confirmed'), ('done', 'Done')],
        string='Status', default='draft', readonly=True, required=True, copy=False,
        help="If event is created, the status is 'Draft'. If event is confirmed for the particular dates the status is set to 'Confirmed'. If the event is over, the status is set to 'Done'. If event is cancelled the status is set to 'Cancelled'.")

    def button_draft(self):
        self.write({'state': 'draft'})

    def button_cancel(self):
        self.write({'state': 'cancel'})

    def button_done(self):
        self.job_id.no_of_recruitment = self.no_employees
        self.job_id.state='recruit'
        self.write({'state': 'done'})

    def button_dept(self):
        self.write({'state': 'dept'})

    def button_hr(self):
        self.write({'state': 'hr'})

    def button_confirm(self):
        self.write({'state': 'confirm'})



