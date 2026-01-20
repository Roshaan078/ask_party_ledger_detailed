{
    'name': 'Partner Ledger Detailed',
    'author': 'Asksol',
    'website': 'https://www.asksol.pk',
    'company': 'Asksol',
    'depends': [
                'base',
                'sale',
                'account',
                'accounting_pdf_reports',
                ],
    'data': [
            'security/ir.model.access.csv',
            'wizard/wizard.xml',
            'views/report_temp.xml',
            'views/report_call.xml',
            'views/menu.xml',
            ],
    'installable': True,
    'auto_install': False,
}
