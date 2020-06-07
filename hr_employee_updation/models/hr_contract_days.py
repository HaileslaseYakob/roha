from odoo.exceptions import Warning
from odoo import models, fields, api, _


class HrEmployeeContract(models.Model):
    _inherit = 'hr.contract'


    @api.depends('wagez')
    def _compute_wage(self):
        if self.wagez:
            if self.wage:
                if self.wage < 1:
                    self.wage=self.wagez
            else:
                self.wage = self.wagez




    def _get_default_notice_days(self):
        if self.env['ir.config_parameter'].get_param(
                'hr_resignation.notice_period'):
            return self.env['ir.config_parameter'].get_param(
                            'hr_resignation.no_of_days')
        else:
            return 0

    structure_type_id = fields.Many2one('hr.payroll.structure.type',related='job_id.structure_type_id',readonly=False, string="Salary Structure Type")
    notice_days = fields.Integer(string="Notice Period", default=_get_default_notice_days)
    wagez = fields.Monetary('Wage',related='job_id.wage',readonly=False, required=True, tracking=True, help="Employee's monthly gross wage.")
    wage = fields.Monetary('Wage',compute="_compute_wage", readonly=False, required=True, store=True,
                            help="Employee's monthly gross wage.")