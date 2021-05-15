from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Plano_Transicao_UC_Mostra(models.Model):
    _name = 'transum.plano_transicao_uc_mostra'
    _description = 'Plano de Transicao UC Mostra'
    active = fields.Boolean('Ativo?', default=True)

    atencao = fields.Boolean(default=False, string='Rever')

    """ uc_antiga = fields.One2many('transum.uc', 'uc_antiga_transicao_mostra', string='UC Antiga')
    uc_nova = fields.One2many('transum.uc', 'uc_nova_transicao_mostra', string='UC Nova') """

    uc_antiga = fields.Many2many('transum.uc','plano_transicao_uc_mostra_antiga','plano_transicao_uc_mostra_id','uc_id', string='UC Antiga')
    uc_nova = fields.Many2many('transum.uc','plano_transicao_uc_mostra_nova','plano_transicao_uc_mostra_id','uc_id', string='UC Nova')

    nota_antiga = fields.Float('Nota Antiga')
    nota_nova = fields.Float('Nota Nova')

    curso_antigo = fields.Many2one('transum.curso', 'Curso Antigo')
    antigo_curso_designacao = fields.Char('Designação', related='curso_antigo.designacao')
    antigo_curso_tipo = fields.Selection([('1', 'Licenciatura'), ('2', 'Mestrado Integrado'), ('3', 'Mestrado')], default='1', related='curso_antigo.tipo')
    str_antigo_curso = fields.Char(compute='_compute_str_antigo_curso')

    curso_novo = fields.Many2one('transum.curso', 'Curso Novo')
    novo_curso_designacao = fields.Char('Designação', related='curso_novo.designacao')
    novo_curso_tipo = fields.Selection([('1', 'Licenciatura'), ('2', 'Mestrado Integrado'), ('3', 'Mestrado')], default='1', related='curso_novo.tipo')
    str_novo_curso = fields.Char(compute='_compute_str_novo_curso')

    proposta = fields.Many2one('transum.proposta_novo_plano', 'Proposta')


    def _compute_str_antigo_curso(self):
        for ptum in self:
            if ptum.antigo_curso_tipo == '1':
                ptum.str_antigo_curso = ptum.antigo_curso_designacao + ' :: Licenciatura \n'
            elif ptum.antigo_curso_tipo == '2':
                ptum.str_antigo_curso = ptum.antigo_curso_designacao + ' :: Mestrado Integrado \n'
            elif ptum.antigo_curso_tipo == '3':
                ptum.str_antigo_curso = ptum.antigo_curso_designacao + ' :: Mestrado \n'

    def _compute_str_novo_curso(self):
        for ptum in self:
            if ptum.novo_curso_tipo == '1':
                ptum.str_novo_curso = ptum.novo_curso_designacao + ' :: Licenciatura \n'
            elif ptum.novo_curso_tipo == '2':
                ptum.str_novo_curso = ptum.novo_curso_designacao + ' :: Mestrado Integrado \n'
            elif ptum.novo_curso_tipo == '3':
                ptum.str_novo_curso = ptum.novo_curso_designacao + ' :: Mestrado \n'