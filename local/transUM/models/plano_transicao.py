from odoo import models, fields
class Plano_Transicao(models.Model):

    _name='transum.plano_transicao'
    _description = 'Plano de Transicao'
    active = fields.Boolean('Active?', default=True)

    designacao = fields.Char('Designação')
    transicao_ucs = fields.One2many('transum.plano_transicao_uc','plano_transicao','Correspondencia entre Unidades Curriculares')
    #plano_curso_antigo = fields.One2Many('transum.plano_curso','','Plano de Curso Antigo')
    #plano_curso_novo = fields.One2Many('transum.plano_curso','','Planos de Curso Novos')