from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Docente(models.Model):

    #_inherits = {'res.users': 'user_id'}
    _name = 'transum.docente'
    _order = 'nr_mecanografico desc'
    _rec_name = 'nr_mecanografico'
    _description = 'Docente'
    active = fields.Boolean('Ativo?', default=True)

    nr_mecanografico = fields.Char('Nº Mecanográfico')
    email = fields.Char('Email')
    nome = fields.Char('Nome')

    direcoes_curso = fields.Many2many('transum.direcao_curso',string='Direções de Curso')

    @api.constrains('nr_mecanografico', 'email', 'nome')
    def _check_docente(self):
        for record in self:
            if not record.nr_mecanografico or not record.email or not record.nome:
                raise models.ValidationError('Um Docente deve possuir um nº mecanográfico, um email e um nome !')