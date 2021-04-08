from odoo import fields, models


class Administrador(models.Model):
    
    _inherits = {"res.users": "user_id"}
    _name = "transum.administrador"
    _order = "nome desc"
    _rec_name = 'nome'
    _description = "Administrador"
    active = fields.Boolean("Active?", default=True)

    nome = fields.Char('Nome')
