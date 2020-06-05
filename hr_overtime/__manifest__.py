# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Employee Overtime Request and Payroll in Odoo',
    'version': '13.0.0.3',
    'category': 'human resources',
    'summary': 'HR Overtime Request Payroll with overtime worksheet employee overtime request employee Multiple Overtime Requests hr employee overtime request with payslip overtime request with payroll integration Employee Payslip overtime timesheet hr overtime timesheet',
    'description': """
	Overtime Requests And Payroll Integration
This module add below features which can be used to manage overtime requests:
  * Overtime Requests: This will be request by employee.
  * Multiple Overtime Requests: This request can be created by HR Manager or Department Manager on behalf of multiple employees together.
  * Integrate Overtime Requests in Employee Payslips: This will show payslip lines in payslip of employee.
Note: This module add new group called "Department Manager(Overtime)" under Usability group.
HR Overtime Request and Payroll
Currently module will use fixed cost of employee on salary rule. Means you have to use fixed cost price / hour to calculate overtime allowance.
For manage employee overtime multiple request, whole process, approvals and intregrated with Payroll in odoo.

employee overtime multiple request
Overtime Request
Employee Overtime
Employee Overtime Request



Menus:
Human Resources/Overtimes
Human Resources/Overtimes/Overtime Requests
Human Resources/Overtimes/Overtime Requests to Approve
Human Resources/Overtimes/Overtime Requests to Approve By Department
Human Resources/Overtimes/Multiple Overtime Requests
Human Resources/Overtimes/Multiple Requests to Approve
Human Resources/Overtimes/Multiple Requests to Approve By Department
	 """,
    'author': 'BrowseInfo',
    'website': 'http://www.browseinfo.in',
    "price": 10,
    "currency": 'EUR',
    'depends': ['base','hr','hr_payroll','hr_payroll_account'],
    'demo': ['data/overtime_rule.xml'],
    'data': [
                'security/ir.model.access.csv',
                'views/multiple_overtime_request.xml'
                ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'live_test_url':'',
    "live_test_url":'https://youtu.be/KOfQd5WVAwI',
    "images":["static/description/banner.png"],
}
