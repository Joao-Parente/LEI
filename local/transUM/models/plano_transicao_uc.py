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
            

    @api.model
    def create(self, vals):
        new_record = super().create(vals)

        for nova in new_record.uc_nova:
            nova_uc = self.env['transum.uc'].search([('id', '=', nova.id)])
            for nv_pln_crs in nova_uc.plano_curso:
                nv_plano = self.env['transum.plano_curso'].search([('id', '=', nv_pln_crs.id)])
                new_record.curso_novo = nv_plano.curso_id.id
        
        for antiga in new_record.uc_antiga:
            antiga_uc = self.env['transum.uc'].search([('id', '=', antiga.id)])
            for atg_pln_crs in antiga_uc.plano_curso:
                atg_plano = self.env['transum.plano_curso'].search([('id', '=', atg_pln_crs.id)])
                new_record.curso_antigo = atg_plano.curso_id.id

        return new_record