from odoo import models, fields
class Plano_Estudos(models.Model):

    _name='transum.plano_estudos'
    _description = 'Plano de Estudos'
    _order='codigo asc'
    _rec_name = 'codigo'
    active = fields.Boolean('Active?', default=True)

    codigo = fields.Char('Código Plano de Estudos')
    nota_uc = fields.One2many('transum.plano_estudos_uc','plano_estudos', string='Unidades Curriculares')
    aluno_associado = fields.Many2one('transum.aluno','Aluno Associado')
    historico_aluno_associado = fields.Many2one('transum.aluno','Histórico Aluno Associado')
    dc_associada = fields.Many2one('transum.direcao_curso','Direção de Curso Associada')