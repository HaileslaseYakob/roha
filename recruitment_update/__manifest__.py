{
    'name': 'Recruitment Update',
    'version': '13.0.2.0.0',
    'summary': """Customizing recruitment """,
    'description': 'This module helps you to add more information to recruitment.',
    'category': 'Generic Modules/Human Resources',
    'author': 'BlueHawk consulting',
    'company': 'BlueHawk consulting',
    'depends': ['base', 'hr', 'mail', 'hr_recruitment','hr_employee_updation'],
    'data': [
        'security/ir.model.access.csv',
        'views/recruit_update.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
