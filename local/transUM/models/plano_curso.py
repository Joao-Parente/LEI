from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Plano_Curso(models.Model):

    _name = 'transum.plano_curso'
    _order = 'codigo desc'
    _rec_name = 'codigo'
    _description = 'Plano de Curso'
    active = fields.Boolean('Ativo?', default=True)

    codigo = fields.Char('Código')

    curso_id = fields.Many2one('transum.curso', 'Curso')

    ucs = fields.Many2many('transum.uc', string='Unidades Curriculares')

    # Nao ligado ao plano de transicao
    # plano_antigo = fields.Many2one('transum.plano_transicao','Plano de Curso Antigo')
    # plano_novo = fields.Many2one('transum.plano_transicao','Planos de Curso Novos')

    @api.constrains('codigo', 'curso_id', 'ucs')
    def _check_plano_curso(self):
        for record in self:
            if not record.codigo or not record.curso_id:
                raise models.ValidationError('Um Plano de Curso deve possuir um código e um curso !')
            if not record.ucs:
                raise models.ValidationError('Um Plano de Curso deve possuir unidades curriculares !')