from odoo import api, fields, models

class PartyLedgerDetailedWizard(models.TransientModel):
    _name = "party.ledger.detailed"
    _description = "Wizard for Party Ledger Detailed Report"

    # Add all fields used in your XML
    company_id = fields.Many2one('res.company', string="Company")
    target_move = fields.Selection([
        ('posted', 'Posted Entries'),
        ('all', 'All Entries'),
    ], string="Target Moves", default='posted')
    result_selection = fields.Selection([
        ('customer', 'Receivable Accounts'),
        ('supplier', 'Payable Accounts'),
        ('all', 'Receivable & Payable Accounts'),
    ], string="Accounts", default='all')
    # amount_currency = fields.Boolean(string="Amount in Currency")
    reconciled = fields.Boolean(string=" Reconciled", default=True)
    
    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)
    journal_ids = fields.Many2many('account.journal', string="Journals", default=lambda self: self.env['account.journal'].search([]))
    partner_ids = fields.Many2many('res.partner', string="Partners")

    # Button method
    def check_report(self):
        data = {
            'form': {
                'company_id': self.company_id.id,
                'target_move': self.target_move,
                'result_selection': self.result_selection,
                # 'amount_currency': self.amount_currency,
                'reconciled': self.reconciled,
                'date_from': self.date_from,
                'date_to': self.date_to,
                'journal_ids': self.journal_ids.ids,
                'partner_ids': self.partner_ids.ids,
            }
        }
        return self.env.ref('ask_party_ledger_detailed.action_report_partnerledger_detailed').report_action(self, data=data)
