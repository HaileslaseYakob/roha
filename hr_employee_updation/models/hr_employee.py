# -*- coding: utf-8 -*-
###################################################################################
#    A part of Open HRMS Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Jesni Banu (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
from datetime import datetime, timedelta
from odoo import models, fields, _, api

GENDER_SELECTION = [('male', 'Male'),
                    ('female', 'Female'),
                    ('other', 'Other')]


class HrSubcity(models.Model):
    """Table for keep employee family information"""

    _name = 'hr.employee.subcity'
    _description = 'Subcity'
    name = fields.Char(string='Sub city')


class HrWoreda(models.Model):
    """Table for keep employee family information"""

    _name = 'hr.employee.woreda'
    _description = 'Woreda'
    name = fields.Char(string='Woreda')


class EmployeeRelationInfo(models.Model):
    """Table for keep employee family information"""

    _name = 'hr.employee.relation'

    name = fields.Char(string="Relationship", help="Relationship with the employee")


class HrKebele(models.Model):
    """Table for keep employee family information"""

    _name = 'hr.employee.kebele'
    _description = 'Kebele'
    name = fields.Char(string='Kebele')


class HrEmployeeFamilyInfo(models.Model):
    """Table for keep employee family information"""

    _name = 'hr.employee.family'
    _description = 'HR Employee Family'

    employee_id = fields.Many2one('hr.employee', string="Employee", help='Select corresponding Employee',
                                  invisible=1)
    member_name = fields.Char(string='Name')
    birth_date = fields.Date(string="DOB", tracking=True)


class HrEmployeeFEmergencyContact(models.Model):
    """Table for keep employee family information"""

    _name = 'hr.employee.emergency'
    _description = 'HR Employee Emergency contact info'

    employee_id = fields.Many2one('hr.employee', string="Employee", help='Select corresponding Employee',
                                  invisible=1)
    relation_id = fields.Many2one('hr.employee.relation', string="Relation", help="Relationship with the employee")
    contact_name = fields.Char(string='Name')
    contact_phone = fields.Char(string='Phone No')
    subcity = fields.Many2one('hr.employee.subcity', string="Subcity")
    woreda = fields.Many2one('hr.employee.woreda', string="Woreda")
    kebele = fields.Many2one('hr.employee.kebele', string="Kebele")
    house_no = fields.Char(string="House No")


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    overtime_rule_id = fields.Many2one('hr.overtime.rules', string="Overtime")
    personal_mobile = fields.Char(string='Mobile', related='address_home_id.mobile', store=True,
                                  help="Personal mobile number of the employee")
    mothername = fields.Char(string='Mother Name')
    subcity = fields.Many2one('hr.employee.subcity', string="Subcity")
    woreda = fields.Many2one('hr.employee.woreda', string="Woreda")
    kebele = fields.Many2one('hr.employee.kebele', string="Kebele")
    house_no = fields.Char(string="House No")

    joining_date = fields.Date(string='Joining Date',
                               help="Employee joining date computed from the contract start date",
                               compute='compute_joining', store=True)
    id_attachment_id = fields.Many2many('ir.attachment', 'id_attachment_rel', 'id_ref', 'attach_ref',
                                        string="Attachment", help='You can attach the copy of your Id')
    passport_attachment_id = fields.Many2many('ir.attachment', 'passport_attachment_rel', 'passport_ref', 'attach_ref1',
                                              string="Attachment",
                                              help='You can attach the copy of Passport')
    fam_ids = fields.One2many('hr.employee.family', 'employee_id', string='Family', help='Family Information')
    emergency_contact_ids = fields.One2many('hr.employee.emergency', 'employee_id', string='Emergency contact',
                                            help='Emergency contact info')

    @api.depends('contract_id')
    def compute_joining(self):
        if self.contract_id:
            date = min(self.contract_id.mapped('date_start'))
            self.joining_date = date
        else:
            self.joining_date = False

    @api.onchange('spouse_complete_name', 'spouse_birthdate')
    def onchange_spouse(self):
        relation = self.env.ref('hr_employee_updation.employee_relationship')
        lines_info = []
        spouse_name = self.spouse_complete_name
        date = self.spouse_birthdate
        if spouse_name and date:
            lines_info.append((0, 0, {
                'member_name': spouse_name,
                'relation_id': relation.id,
                'birth_date': date,
            })
                              )
            self.fam_ids = [(6, 0, 0)] + lines_info


class SalaryGrade(models.Model):
    _name = "hr.grade"
    _description = "Salary Grade"

    name = fields.Char("Grade name")
    salary_grade_levels=fields.One2many('hr.grade.levels','salary_grade_id',"Grade Levels")


class SalaryGradeLevels(models.Model):
    _name = "hr.grade.levels"
    _description = "Grade levels"

    salary_grade_id = fields.Many2one('hr.grade', string='Grade')
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    name = fields.Char("Level name")
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    wage = fields.Monetary('Wage', required=True, tracking=True, help="Employee's monthly gross wage.")


class HrEmployee(models.Model):
    _inherit = 'hr.job'

    no_of_recruitment = fields.Integer(string='Expected New', copy=False,
        help='Number of new employees you expect to recruit.', default=1)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    salary_grade_id = fields.Many2one('hr.grade', string="Grade")
    structure_type_id = fields.Many2one('hr.payroll.structure.type', string="Salary Structure Type")
    scheduled_on_budget = fields.Integer("Scheduled on Budget")

    @api.depends('scheduled_on_budget','no_of_employee')
    def _compute_vaccant(self):
       for cur in self:
            if not cur.scheduled_on_budget:
                cur.scheduled_on_budget=0

            vaccants = cur.scheduled_on_budget - cur.no_of_employee
            if vaccants < 1:
               vaccants=0
            cur.vaccant=vaccants

    vaccant = fields.Integer("vaccant", compute='_compute_vaccant',store=True)
