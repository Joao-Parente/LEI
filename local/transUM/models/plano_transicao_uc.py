from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Plano_Transicao_UC(models.Model):

    _name = 'transum.plano_transicao_uc'
    _description = 'Plano de Transicao UC'
    active = fields.Boolean('Ativo?', default=True)

    uc_antiga = fields.One2many('transum.uc', 'uc_antiga_transicao', string='UC Antiga')
    uc_nova = fields.One2many('transum.uc', 'uc_nova_transicao', string='UC Nova')

    curso_antigo = fields.Many2one('transum.curso', 'Curso Antigo')
    curso_novo = fields.Many2one('transum.curso', 'Curso Novo')

    plano_transicao = fields.Many2one('transum.plano_transicao', 'Plano de Transicao Associado')

    #plano_curso_antigo = fields.One2Many('transum.plano_curso','','Plano de Curso Antigo')
    #plano_curso_novo = fields.One2Many('transum.plano_curso','','Planos de Curso Novos')


    @api.constrains('uc_antiga', 'uc_nova', 'curso_antigo', 'curso_novo')
    def _check_plano_transicao_uc(self):
        for record in self:
            for antiga_uc in record.uc_antiga:
                antigo_curso = self.env['transum.curso'].search([('id', '=', record.curso_antigo.id)])
                if not antigo_curso.existe_no_plano_curso(antiga_uc.id):
                    raise models.ValidationError('A Unidade Curricular Antiga introduzida não está presente no plano de curso do Curso Antigo !')

            for nova_uc in record.uc_nova:
                novo_curso = self.env['transum.curso'].search([('id', '=', record.curso_novo.id)])
                if not novo_curso.existe_no_plano_curso(nova_uc.id):
                    raise models.ValidationError('A Unidade Curricular Nova introduzida não está presente no plano de curso do Curso Novo !')