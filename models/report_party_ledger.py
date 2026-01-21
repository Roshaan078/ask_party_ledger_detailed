from odoo import api, models, _
from odoo.exceptions import UserError
import time

class ReportPartyLedger(models.AbstractModel):
    _name = 'report.ask_party_ledger_detailed.report_party_ledger'
    _description = 'Party Ledger Detailed Report (SQL Based)'

    def _get_lines(self, data, partner):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        target_move = data['form']['target_move']

        move_states = ("posted",) if target_move == 'posted' else ("draft", "posted")

        self.env.cr.execute("""
            WITH opening_balance AS (
                SELECT
                    aml.date AS date,
                    j.code::text AS journal,
                    m.name::text AS document,
                    NULL::text AS product,
                    0::numeric AS quantity,
                    0::numeric AS price_unit,
                    COALESCE(aml.debit,0)::numeric AS debit,
                    COALESCE(aml.credit,0)::numeric AS credit
                FROM account_move_line aml
                JOIN account_move m ON aml.move_id = m.id
                JOIN account_journal j ON m.journal_id = j.id
                JOIN account_account acc ON aml.account_id = acc.id
                WHERE aml.partner_id = %s
                  AND m.state IN %s
                  AND m.name ILIKE 'OpBal%%'
                  AND acc.account_type IN ('asset_receivable','liability_payable')
            ),

            product_lines AS (
                SELECT
                    aml.date AS date,
                    j.code::text AS journal,
                    m.name::text AS document,
                    pt.name->>'en_US' AS product,
                    COALESCE(aml.quantity,0)::numeric AS quantity,
                    COALESCE(aml.price_unit,0)::numeric AS price_unit,
                    CASE
                        WHEN m.move_type IN ('out_invoice','in_invoice')
                        THEN ABS(COALESCE(aml.price_subtotal,0))::numeric
                        ELSE 0
                    END AS debit,
                    CASE
                        WHEN m.move_type IN ('out_refund','in_refund')
                        THEN ABS(COALESCE(aml.price_subtotal,0))::numeric
                        ELSE 0
                    END AS credit
                FROM account_move_line aml
                JOIN account_move m ON aml.move_id = m.id
                JOIN account_journal j ON m.journal_id = j.id
                LEFT JOIN product_product pp ON aml.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                WHERE aml.partner_id = %s
                  AND m.state IN %s
                  AND aml.date BETWEEN %s AND %s
                  AND aml.product_id IS NOT NULL
            ),

            payment_lines AS (
                SELECT
                    aml.date AS date,
                    j.code::text AS journal,
                    m.name::text AS document,
                    NULL::text AS product,
                    0::numeric AS quantity,
                    0::numeric AS price_unit,
                    COALESCE(aml.debit,0)::numeric AS debit,
                    COALESCE(aml.credit,0)::numeric AS credit
                FROM account_move_line aml
                JOIN account_move m ON aml.move_id = m.id
                JOIN account_journal j ON m.journal_id = j.id
                JOIN account_account acc ON aml.account_id = acc.id
                WHERE aml.partner_id = %s
                  AND m.state IN %s
                  AND aml.date BETWEEN %s AND %s
                  AND acc.account_type IN ('asset_receivable','liability_payable')
                  AND m.move_type NOT IN ('out_invoice','in_invoice','out_refund','in_refund')
                  AND m.name NOT ILIKE 'OpBal%%'
            ),

            all_lines AS (
                SELECT * FROM opening_balance
                UNION ALL
                SELECT * FROM product_lines
                UNION ALL
                SELECT * FROM payment_lines
            )

            SELECT
                date,
                journal,
                document,
                product,
                quantity,
                price_unit,
                debit,
                credit,
                SUM(debit - credit) OVER (
                    ORDER BY date, document, product NULLS LAST
                ) AS running_balance
            FROM all_lines
            ORDER BY date, document, product NULLS LAST
        """, (
            partner.id, move_states,
            partner.id, move_states, date_from, date_to,
            partner.id, move_states, date_from, date_to
        ))

        return self.env.cr.dictfetchall()

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data or not data.get('form'):
            raise UserError(_("Missing form data"))

        partners = self.env['res.partner'].browse(data['form']['partner_ids'])

        return {
            'doc_ids': partners.ids,
            'doc_model': 'res.partner',
            'docs': partners,
            'data': data,
            'time': time,
            'get_lines': self._get_lines,
        }
