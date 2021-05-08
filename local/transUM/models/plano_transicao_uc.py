from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Plano_Transicao_UC(models.Model):

    _name = 'transum.plano_transicao_uc'
    _description = 'Plano de Transicao UC'
    active = fields.Boolean('Ativo?', default=True)

    uc_antiga = fields.One2many('transum.uc', 'uc_antiga_transicao', string='UC Antiga')
    uc_nova = fields.One2many('transum.uc', 'uc_nova_transicao', string='UC Nova')

    curso_antigo = fields.Many2one('transum.curso', 'Curso Antigo', compute='_compute_curso_antigo')
    curso_novo = fields.Many2one('transum.curso', 'Curso Novo', compute='_compute_curso_novo')

    plano_transicao = fields.Many2one('transum.plano_transicao', 'Plano de Transicao Associado')


    def _compute_curso_antigo(self):
        for record in self:
            for antiga in record.uc_antiga:
                antiga_uc = self.env['transum.uc'].search([('id', '=', antiga.id)])
                for pln_crs in antiga_uc.plano_curso:
                    plano = self.env['transum.plano_curso'].search([('id', '=', pln_crs.id)])
                    record.curso_antigo = plano.curso_id.id


    def _compute_curso_novo(self):
        for record in self:
            for nova in record.uc_nova:
                nova_uc = self.env['transum.uc'].search([('id', '=', nova.id)])
                for pln_crs in nova_uc.plano_curso:
                    plano = self.env['transum.plano_curso'].search([('id', '=', pln_crs.id)])
                    record.curso_novo = plano.curso_id.id