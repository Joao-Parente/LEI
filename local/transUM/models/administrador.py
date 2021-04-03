from odoo import fields, models

class Administrador(models.Model):
    _inherits = {'res.users': 'user_id'}
    _name = 'transum.administrador'
    _description = 'Administrador'
    _order = 'name desc'
    active = fields.Boolean('Active?', default=True)
