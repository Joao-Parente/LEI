from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Plano_Estudos(models.Model):

    _name = 'transum.plano_estudos'
    _order = 'codigo desc'
    _rec_name = 'codigo'
    _description = 'Plano de Estudos'
    active = fields.Boolean('Ativo?', default=True)

    codigo = fields.Char('Código')

    dc_associada = fields.Many2one('transum.direcao_curso', 'Direção de Curso')

    aluno_associado = fields.Many2one('transum.aluno', 'Aluno')
    historico_aluno_associado = fields.Many2one('transum.aluno', 'Histórico do Aluno')

    proposta_antiga = fields.One2many('transum.proposta_novo_plano', 'plano_antigo', 'Plano de Estudos Antigo')
    proposta_nova = fields.Many2one('transum.proposta_novo_plano', 'Propostas Novos Planos Novas')

    nota_uc = fields.One2many('transum.plano_estudos_uc', 'plano_estudos', string='Unidades Curriculares')

    @api.constrains('codigo', 'dc_associada', 'aluno_associado', 'nota_uc')
    def _check_plano_estudos(self):
        for record in self:
            if not record.codigo:
                raise models.ValidationError('Um Plano de Estudos deve possuir um código !')
            if not record.dc_associada:
                raise models.ValidationError('Um Plano de Estudos deve possuir uma Direção de Curso associada !')
            if not record.aluno_associado:
                raise models.ValidationError('Um Plano de Estudos deve estar associado a um determinado aluno !')
            if not record.nota_uc:
                raise models.ValidationError('Um Plano de Estudos deve possuir pelos menos uma Unidade Curricular !')