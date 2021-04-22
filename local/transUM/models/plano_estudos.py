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

    total_creditos_feitos = fields.Integer(compute='_compute_calcula_creditos_feitos', string='Total de Créditos Feitos', default=0)
    total_creditos_falta = fields.Integer(compute='_compute_calcula_creditos_falta', string='Total de Créditos a realizar', default=0)

    def _compute_calcula_creditos_feitos(self):
        for record in self:
            record.total_creditos_feitos = 0
            for pln_stds_c_id in record.nota_uc:
                pln_stds_c = self.env['transum.plano_estudos_uc'].search([('id', '=', pln_stds_c_id.id)])
                if pln_stds_c.nota != 0:
                    record.total_creditos_feitos += pln_stds_c.uc.ects


    def _compute_calcula_creditos_falta(self):
        for record in self:
            record.total_creditos_falta = 0
            for pln_stds_c_id in record.nota_uc:
                pln_stds_c = self.env['transum.plano_estudos_uc'].search([('id', '=', pln_stds_c_id.id)])
                if pln_stds_c.nota == 0:
                    record.total_creditos_falta += pln_stds_c.uc.ects


    @api.constrains('codigo', 'dc_associada', 'aluno_associado', 'nota_uc')
    def _check_plano_estudos(self):
        # Campos vazios & Associacoes
        if not self.codigo:
            raise models.ValidationError('Um Plano de Estudos deve possuir um código !')
        if not self.dc_associada:
            raise models.ValidationError('Um Plano de Estudos deve possuir uma Direção de Curso associada !')
        """if not self.aluno_associado:
            raise models.ValidationError('Um Plano de Estudos deve estar associado a um determinado aluno !')
        if not self.nota_uc:
            raise models.ValidationError('Um Plano de Estudos deve possuir pelos menos uma Unidade Curricular !') """