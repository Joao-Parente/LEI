from odoo import models, fields
class Direcao_Curso(models.Model):

    _name = 'transum.direcao_curso'
    _description = 'Direção de Curso'
    _order = 'codigo desc'
    _rec_name = 'codigo'
    active = fields.Boolean('Active?', default=True)

    codigo = fields.Char('Código')
    docentes = fields.Many2many('transum.docente', string='Docentes')
    curso_id = fields.Many2one('transum.curso', 'Curso ID')
    planos_estudo = fields.One2many('transum.plano_estudos','dc_associada','Planos de Estudos do Curso')
