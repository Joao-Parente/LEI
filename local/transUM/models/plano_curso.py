from odoo import models, fields
class Plano_Curso(models.Model):

    #_inherits = {'res.users': 'user_id'}
    _name='transum.plano_curso'
    _description = 'Plano de Curso'
    _order='codigo asc'
    _rec_name = 'codigo'
    active = fields.Boolean('Active?', default=True)

    codigo = fields.Char('Código Plano de Curso')
    curso_id = fields.Many2one('transum.curso','Curso Associado')
    ucs = fields.Many2many('transum.uc', string='Unidades Curriculares') 
    
    #plano_antigo = fields.Many2one('transum.plano_transicao','Plano de Curso Antigo')
    #plano_novo = fields.Many2one('transum.plano_transicao','Planos de Curso Novos')

   