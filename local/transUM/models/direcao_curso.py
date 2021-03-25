from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Direcao_Curso(models.Model):
    _name = 'transum.direcao_curso'
    _description = 'Direção de Curso'
    _order = 'codigo desc'
    _rec_name = 'codigo'
    active = fields.Boolean('Active?', default=True)

    codigo = fields.Char('Código')
    #docentes = fields.Many2many('planum.docente', string='Docentes')
    curso_id = fields.Many2one('transum.curso', 'Curso ID')

    