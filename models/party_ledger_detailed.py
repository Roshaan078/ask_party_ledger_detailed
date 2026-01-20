from odoo import api, models, _
from odoo.exceptions import UserError
import time

class PartyLedgerDetailed(models.Model):
    _name = "party.ledger.detailed"
    _description = "Party Ledger Detailed"

    # This model is just a placeholder for the report
    # No fields needed; report is generated via wizard and SQL
