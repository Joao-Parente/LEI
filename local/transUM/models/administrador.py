from odoo import fields, models


class Administrador(models.Model):

    _inherits = {"res.users": "user_id"}
    _name = "transum.administrador"
    _order = "name desc"
    _rec_name = 'name'
    _description = "Administrador"
    active = fields.Boolean("Ativo?", default=True)
