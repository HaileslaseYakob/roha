# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.

from dateutil.rrule import DAILY, rrule
from odoo import api, fields, models, _
from datetime import datetime, date
import pytz
from odoo.exceptions import UserError, Warning
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class Holidays(models.Model):
    _name = "hr.overtime.holidays"
    _description = "Holidays list"

    name = fields.Char("Holiday name")
    holiday_date = fields.Date(string="Date")


class OvertimeRules(models.Model):
    _name = "hr.overtime.rules"
    _description = "Overtime rules"

    name = fields.Char("Overtime rule ref.")
    holiday_perminute= fields.Integer(string="Holiday per minute")
    weekends_perminute= fields.Integer(string="Weekends per minute")
    weekdays_perminute= fields.Integer(string="Weekdays per minute")


class OvertimeMaster(models.Model):
    _name = "hr.overtime.master"
    _description = "Overtime Request"

    def calculate_overtime(self):
        list_overtime_detail = []
        list_overtime_detail.append((5, 0, 0))
        user_tz = self.env.context.get('tz') or self.env.user.tz
        local = pytz.timezone(user_tz)


        for re in self.overtime_summary:
            startDate = pytz.utc.localize(re.start_date).astimezone(local)
            endDate = pytz.utc.localize(re.end_date).astimezone(local)

            rule_id = re.employee_id.overtime_rule_id.id
            over_time_rule = self.env['hr.overtime.rules'].search(
                [('id', '=', rule_id)])
            weekdayspay = 0.0
            weekendspay = 0.0
            holidayspay = 0.0
            for line in over_time_rule:
                weekdayspay=line.weekdays_perminute
                weekendspay = line.weekends_perminute
                holidayspay = line.holiday_perminute

            over_time_holidays = self.env['hr.overtime.holidays'].search(
                [])
            list_holidays=[]
            for overtime_holiday in over_time_holidays:
                list_holidays.append(overtime_holiday.holiday_date)

            for i in rrule(DAILY, dtstart=startDate, until=endDate):
                # print(i.strftime('%Y/%m/%d'), sep='\n')
                time_delta = datetime.combine(date.today(), startDate.time()) - datetime.combine(date.today(),
                                                                                                 endDate.time())
                total_seconds = time_delta.total_seconds()
                hour = startDate.time().hour
                minute = startDate.time().minute
                startingTime = float('%s.%s' % (hour, minute))

                hour = endDate.time().hour
                minute = endDate.time().minute
                endingTime = float('%s.%s' % (hour, minute))

                overtime_earned=0.0
                if i.date() in list_holidays:
                    overtime_earned=(total_seconds / 60) * holidayspay
                else:
                    overtime_earned=(total_seconds / 60) * weekdayspay

                obje = {
                    'employee_id': re.employee_id.id,
                    'overtime_date': i.date(),
                    'starting_time': startingTime,
                    'ending_time': endingTime,
                    'overtime_earned': overtime_earned,
                    'difference_min': total_seconds / 60}
                list_overtime_detail.append((0, 0, obje))
        self.overtime_detail = list_overtime_detail

    @api.constrains('end_date', 'start_date')
    def check_end_date(self):
        if self.end_date < self.start_date:
            raise Warning(_('End Date must be after the Start Date!!'))

    def confirm_action(self):

        self.write({'state': 'first_approve'})
        return

    def first_approve_action(self):
        self.write({'state': 'hr_approve',
                    'dept_manager_id': self.env.user.id,
                    'dept_approve_date': fields.datetime.now()})
        return

    def hr_approve_action(self):
        self.write({'state': 'done',
                    'hr_approve_by_id': self.env.user.id,
                    'hr_approve_date': fields.datetime.now()})
        return

    def refuse_action(self):
        self.write({'state': 'refuse'})
        return

    name = fields.Char(string="Reference")
    department_id = fields.Many2one('hr.department', string="Department",
                                    default=lambda self: self.env.user.employee_id.department_id, required=True)
    requested_id = fields.Many2one('res.users', string="Requested By", default=lambda self: self.env.user)
    requested_date = fields.Datetime(string="Approve Date", readonly=True, default=fields.datetime.now())

    gm_approve_date = fields.Datetime(string="Approve Date", readonly=True)
    gm_approve_by_id = fields.Many2one('res.users', string="Approve By", readonly=True)

    hr_approve_date = fields.Datetime(string="Approve Date", readonly=True)
    hr_approve_by_id = fields.Many2one('res.users', string="Approve By", readonly=True)

    dept_approve_date = fields.Datetime(string="Department Approve Date", readonly=True)
    dept_manager_id = fields.Many2one('res.users', string="Department Manager", readonly=True)

    include_in_payroll = fields.Boolean(string="Include In Payroll", default=True)
    notes = fields.Text(string="Notes")
    state = fields.Selection([('new', 'New'), ('first_approve', 'Waiting For First Approve'),
                              ('hr_approve', 'Waiting For Department Approve'),
                              ('done', 'Done'), ('refuse', 'Refuse')], string="State", default='new')
    overtime_detail = fields.One2many('hr.overtime.detail', 'overtime_master_id', string="Overtime Detail")
    overtime_summary = fields.One2many('hr.overtime.summary', 'overtime_master_id', string="Overtime summary")


class OvertimeSummary(models.Model):
    _name = "hr.overtime.summary"
    _description = "Overtime Summary"

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    overtime_rule_id=fields.Many2one('hr.overtime.rules', related='employee_id.overtime_rule_id', string="Overtime", readonly=True)
    overtime_master_id = fields.Many2one('hr.overtime.master')
    start_date = fields.Datetime(string="Start Date", required=True)
    end_date = fields.Datetime(string="End Date", required=True)


class OvertimeDetail(models.Model):
    _name = "hr.overtime.detail"
    _description = "Overtime detail"

    def _compute_num_of_hours(self):
        # for line in self:
        # 	if line.start_date and line.end_date:
        # 		diff = line.end_date - line.start_date
        # 		days, seconds = diff.days, diff.seconds
        # 		hours = days * 24 + seconds // 3600
        # 		line.num_of_hours = hours
        return

    overtime_master_id = fields.Many2one('hr.overtime.master')
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    overtime_date = fields.Date(string="Start Date", required=True, default=fields.datetime.now())
    starting_time = fields.Float(string="Starting Time", required=True)
    ending_time = fields.Float(string="Ending Time", required=True)
    difference_min = fields.Float(string="Difference", required=True)
    overtime_earned = fields.Float(string="Overtime Earned", required=True)
