from odoo.exceptions import Warning
from odoo import models, fields, api, _


class HrEmployeeContract(models.Model):
    _inherit = 'hr.contract'

    def _get_default_notice_days(self):
        if self.env['ir.config_parameter'].get_param(
                'hr_resignation.notice_period'):
            return self.env['ir.config_parameter'].get_param(
                'hr_resignation.no_of_days')
        else:
            return 0

    @api.depends('salary_level_id')
    def _compute_wage(self):
        for rec in self:
            rec.wage = rec.salary_level_id.wage

    @api.onchange('salary_grade_id')
    def _campus_onchange(self):
        res = {}
        res['domain'] = {'salary_level_id': [('salary_grade_id', '=', self.salary_grade_id.id)]}
        return res

    salary_grade_id = fields.Many2one('hr.grade', related='job_id.salary_grade_id', readonly=True,
                                      string="Salary Structure Type")
    salary_level_id = fields.Many2one('hr.grade.levels', readonly=False,
                                      string="Salary level")
    structure_type_id = fields.Many2one('hr.payroll.structure.type', related='job_id.structure_type_id', readonly=False,
                                        string="Salary Structure Type")
    notice_days = fields.Integer(string="Notice Period", default=_get_default_notice_days)

    wage = fields.Monetary('Wage', compute="_compute_wage",store=True,
                           help="Employee's monthly gross wage.")
