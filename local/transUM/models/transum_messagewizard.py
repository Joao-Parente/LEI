from odoo import models, fields

class TransumMessageWizard(models.TransientModel):
    _name = 'transum.message.wizard'
    _description = "Show Message"

    message = fields.Text('Message', required=True)

    def action_close(self):
        return {'type': 'ir.actions.act_window_close'}