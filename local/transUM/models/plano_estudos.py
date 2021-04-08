from odoo import models, fields


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