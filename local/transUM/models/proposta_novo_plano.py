from odoo import models, fields


class Proposta_Novo_Plano(models.Model):

    _name = 'transum.proposta_novo_plano'
    _order = 'designacao desc'
    _rec_name = 'designacao'
    _description = 'Proposta De Novo Plano'
    active = fields.Boolean('Ativo?', default=True)

    opcao = fields.Selection([('1', 'Sim'), ('2', 'Não'), ('3', 'Já aceitou'), ('4','Necessita de Atenção')], string='Tem Opção?', default='1')

    plano_antigo = fields.Many2one('transum.plano_estudos', 'Plano Antigo ID')
    ucs_plano_antigo = fields.One2many('transum.plano_estudos_uc', 'plano_estudos', string='Plano de Estudos UCs', related='plano_antigo.nota_uc')
    planos_novos = fields.One2many('transum.plano_estudos', 'proposta_nova', 'Planos Novos')

    aluno = fields.One2many('transum.aluno', 'proposta_plano_aluno', 'Aluno Associado')

    plano_transicao = fields.Many2one('transum.plano_transicao', 'Plano de Transição')
    ucs_plano_transicao = fields.One2many('transum.plano_transicao_uc', 'plano_transicao', string='Plano de Transição UCs', related='plano_transicao.transicao_ucs')

    transicao_ucs_mostra = fields.One2many('transum.plano_transicao_uc_mostra', 'proposta', string='Correspondência')

    designacao = fields.Char(compute='_compute_designacao')


    def _compute_designacao(self):
        for record in self:
            record.designacao = 'Proposta de Transição ' + str(record.id)


    def aprovar(self):
        alunos = self.env['transum.aluno']
        planos_estudos = self.env['transum.plano_estudos']

        for aluno_id in self.aluno:
            aluno = alunos.search([('id', '=', aluno_id.id)])

            for plano_novo in self.planos_novos:
                plano_novo.aluno_associado = aluno.id

            pln_antg = planos_estudos.search([('id', '=', self.plano_antigo.id)])
            pln_antg.aluno_associado = None
            pln_antg.historico_aluno_associado = aluno.id

            aluno.estado = '3'
            self.opcao = '3'

            # Mudar de curso !!!


    def rejeitar(self):
        for aluno_id in self.aluno:
            aluno = self.env['transum.aluno'].search([('id', '=', aluno_id.id)])
        