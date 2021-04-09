from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Direcao_Curso(models.Model):

    _name = 'transum.direcao_curso'
    _order = 'codigo desc'
    _rec_name = 'codigo'
    _description = 'Direção de Curso'
    active = fields.Boolean('Ativo?', default=True)

    codigo = fields.Char('Código')
    
    curso_id = fields.Many2one('transum.curso', 'Curso ID')
    
    docentes = fields.Many2many('transum.docente', string='Docentes')

    planos_estudo = fields.One2many('transum.plano_estudos', 'dc_associada', 'Planos de Estudos do Curso')

    @api.constrains('codigo', 'curso_id', 'docentes')
    def _check_dc(self):
        for record in self:
            if not record.codigo or not record.curso_id:
                raise models.ValidationError('Uma Direção de Curso deve possuir um código e um curso associado !')
            if not record.docentes:
                raise models.ValidationError('Uma Direção de Curso deve possuir pelo menos um docente !')