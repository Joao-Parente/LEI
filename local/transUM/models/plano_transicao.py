from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Plano_Transicao(models.Model):

    _name = 'transum.plano_transicao'
    _order = "designacao desc"
    _rec_name = 'designacao'
    _description = 'Plano de Transição'
    active = fields.Boolean('Ativo?', default=True)

    designacao = fields.Char('Designação')

    transicao_ucs = fields.One2many('transum.plano_transicao_uc', 'plano_transicao', 'Correspondência')

    #plano_curso_antigo = fields.One2Many('transum.plano_curso','','Plano de Curso Antigo')
    #plano_curso_novo = fields.One2Many('transum.plano_curso','','Planos de Curso Novos')

    @api.constrains('designacao', 'transicao_ucs')
    def _check_plano_curso(self):
        for record in self:
            if not record.designacao:
                raise models.ValidationError('Um Plano de Transição deve possuir uma designação !')
            if not record.transicao_ucs:
                raise models.ValidationError('Um Plano de Transição deve possuir pelo menos uma correspondência !')