from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Administrador(models.Model):

    _inherits = {'res.users': 'user_id'}
    _name = "transum.administrador"
    _order = "name desc"
    _rec_name = 'name'
    _description = "Administrador"
    active = fields.Boolean("Ativo?", default=True)

    @api.model
    def create(self, vals):
        if not vals['login']:
            raise ValidationError('É obrigatório preencher todos os campos do formulário !')

        new_record = super().create(vals)

        grouprel = self.env['res.groups'].search([('name', '=', 'Administrador')])
        grouprel.write({'users': [(4, new_record.user_id.id)]})

        return new_record

    @api.constrains('login')
    def check_administrador(self):
        if not self.login:
            raise ValidationError('O email e o nome são campos obrigatórios !')

    def ativar(self):
        for rec in self:
            rec.active = True

    def desativar(self):
        for rec in self:
            rec.active = False