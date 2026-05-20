from odoo import models, fields, _
from odoo.exceptions import UserError

class AccountingReportWizard(models.TransientModel):
    _name = 'accounting.report.wizard'
    _description = 'Accounting Report Wizard'

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Project / Analytic Account',
        help="Leave empty to show all projects with markup"
    )

    date_from = fields.Date(
        string='From',
        required=True,
        default=lambda self: fields.Date.context_today(self).replace(month=1, day=1),
    )

    date_to = fields.Date(
        string='To',
        required=True,
        default=lambda self: fields.Date.context_today(self),
    )

    def _get_analytic_accounts(self):     #This will return the account with markup_percentage.
        if self.analytic_account_id:
            return self.analytic_account_id
        
        return self.env['account.analytic.account'].search([('markup_percentage', '>', 0)])

    def action_print_button(self):   #Validating the data entered by the user and triggering the report action if all goes well.
        self.ensure_one()
        
        if self.date_from > self.date_to:
            raise UserError(_("'From' date must be before 'To' date."))
        if not self.analytic_account_id:
            raise UserError(_("You must choose a project."))

        return self.env.ref('vendor_bill_report.action_report_custom_bills').report_action(self)