# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
import datetime
from odoo.exceptions import UserError

class Hr_employee_inherit_(models.Model):
    _inherit = "hr.employee"

    def get_overtime(self,id,start_date,end_date):
        
        over_time_rec = self.env['hr.overtime.detail'].search([('employee_id','=',self.id),('start_date','>=',start_date),
                                                                    ('end_date','<=',end_date),('state','=','done')])
        total = 0.0
        for line in over_time_rec : 
            if line.include_in_payroll == True :
                total = total + line.actual_overtime_earned


        return total