from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Plano_Transicao_UC_Mostra(models.Model):
    _name = 'transum.plano_transicao_uc_mostra'
    _description = 'Plano de Transicao UC Mostra'
    active = fields.Boolean('Ativo?', default=True)

    uc_antiga = fields.One2many('transum.uc', 'uc_antiga_transicao_mostra', string='UC Antiga')
    uc_nova = fields.One2many('transum.uc', 'uc_nova_transicao_mostra', string='UC Nova')

    nota_antiga= fields.Float('Nota Antiga')
    nota_nova= fields.Float('Nota Nova')

    curso_antigo = fields.Many2one('transum.curso', 'Curso Antigo')
    curso_novo = fields.Many2one('transum.curso', 'Curso Novo')

    plano_transicao_mostra = fields.Many2one('transum.plano_transicao', 'Plano de Transicao Associado')
