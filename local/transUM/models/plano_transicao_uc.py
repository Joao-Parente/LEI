from odoo import models, fields
class Plano_Transicao_UC(models.Model):

    _name='transum.plano_transicao_uc'
    _description = 'Plano de Transicao UC'
    active = fields.Boolean('Active?', default=True)

    #Many2Many não funciona para ambas ao mesmo tempo, usou-se one2many aqui e many2one na uc
    #Só que isso quer dizer que varias ucs só podem estar num plano de transição
    #Se tivermos cursos que reutilizem ucs dá mal
    uc_antiga = fields.One2many('transum.uc','uc_antiga_transicao',string='Unidade Curricular Antiga')
    uc_nova = fields.One2many('transum.uc','uc_nova_transicao',string='Unidade Curricular Nova')
    
    plano_transicao = fields.Many2one('transum.plano_transicao','Plano de Transicao Associado')

    #plano_curso_antigo = fields.One2Many('transum.plano_curso','','Plano de Curso Antigo')
    #plano_curso_novo = fields.One2Many('transum.plano_curso','','Planos de Curso Novos')