from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Docente(models.Model):

    _inherits = {'res.users': 'user_id'}
    _name = 'transum.docente'
    _order = 'nr_mecanografico desc'
    _rec_name = 'nr_mecanografico'
    _description = 'Docente'
    active = fields.Boolean('Ativo?', default=True)

    nr_mecanografico = fields.Char('Nº Mecanográfico')

    direcoes_curso = fields.Many2many('transum.direcao_curso', string='Direções de Curso')

    # record_file = fields.Binary(string='file', attachment=True, help='Upload the file')

    @api.model
    def create(self, vals):
        if not vals['login']:
            raise ValidationError('É obrigatório preencher todos os campos do formulário !')

        new_record = super().create(vals)

        grouprel = self.env['res.groups'].search([('name', '=', 'Docente')])
        grouprel.write({'users': [(4, new_record.user_id.id)]})

        return new_record

    @api.constrains('nr_mecanografico', 'login', 'name')
    def _check_docente(self):
        # Campos vazios
        if not self.nr_mecanografico or not self.login or not self.name:
            raise models.ValidationError('Um Docente deve possuir um nº mecanográfico, um email e um nome !')

        # ID unico
        if len(self.env['transum.docente'].search(
            [('nr_mecanografico', '=', self.nr_mecanografico)])) > 1:
            raise models.ValidationError('O nº mecanográfico introduzido já está associado a outro Docente !')

    def ativar(self):
        for rec in self:
            rec.active = True

    def desativar(self):
        for rec in self:
            rec.active = False