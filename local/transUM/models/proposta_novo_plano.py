from odoo import models, fields


class Proposta_Novo_Plano(models.Model):

    _name = 'transum.proposta_novo_plano'
    _order = 'designacao desc'
    _rec_name = 'designacao'
    _description = 'Proposta De Novo Plano'    
    active = fields.Boolean('Ativo?', default=True)

    plano_antigo = fields.Many2one('transum.plano_estudos', 'Plano de Estudos Antigo')
    planos_novos = fields.One2many('transum.plano_estudos', 'proposta_nova', 'Planos de Estudos Novos')

    aluno = fields.One2many('transum.aluno', 'proposta_plano_aluno', 'Aluno Associado')

    plano_transicao = fields.Many2one('transum.plano_transicao', 'Plano de Transição')

    designacao = fields.Char(compute='_compute_designacao')


    def _compute_designacao(self):
        for record in self:
            record.designacao = 'Proposta de Transição ' + str(record.id)