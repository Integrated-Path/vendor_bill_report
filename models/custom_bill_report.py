from odoo import models, api, fields

class CustomBillReport(models.Model):
    _name = 'report.vendor_bill_report.report_vendor_bill_custom'
    _description = 'Accounting Model for Custom Bill Report'


    invoice_line_id = fields.Many2one(
        comodel_name="account.move.line",
        string='Linked Invoice Line')


    @api.model
    def _get_report_values(self, docids, data=None):
        
        wizard = self.env['accounting.report.wizard'].browse(docids) # docids contains the ID of the wizard that called this report

        analytic_accounts = wizard._get_analytic_accounts()   #we're getting the selected analytic_account coming from the wizard calling this report


        domain = [
            ('move_type', '=', 'in_invoice'),
            ('state', '=', 'posted'),
            ('invoice_date', '>=', wizard.date_from),
            ('invoice_date', '<=', wizard.date_to),
        ]
        
        if analytic_accounts:                                                   #Filtering only the selected analytic_account's Lines
            domain.append(('invoice_line_ids.analytic_distribution', 'in', [str(id) for id in analytic_accounts.ids]))

        # Search for the actual accounting documents
        docs = self.env['account.move'].search(domain, order='invoice_date asc')

        # Returning a dictionary of values to the QWeb XML view
        return {
            'doc_ids': docids,
            'doc_model': 'accounting.report.wizard',
            'wizard': wizard,
            'docs': docs, #This is what report_vendor_bill_custom t tag loops through
        }
