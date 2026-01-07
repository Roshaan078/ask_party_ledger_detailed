{
    'name': 'Partner Ledger Detailed',
    'author': 'Asksol',
    'website': 'https://www.asksol.pk',
    'company': 'ItechResources',
    'depends': [
                'base',
                'sale',
                'account',
                'accounting_pdf_reports',
#                 'account_accountant',      
                ],
    'data': [
            'wizard/wizard.xml',
            'views/report_temp.xml',
            'views/report_call.xml'
            ],
    'installable': True,
    'auto_install': False,
    'price':'20.0',
    'currency': 'EUR',
}
