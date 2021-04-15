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
        # Campos vazios 
        if not self.codigo or not self.curso_id:
            raise models.ValidationError('Uma Direção de Curso deve possuir um código e um curso associado !')
        if not self.docentes:
            raise models.ValidationError('Uma Direção de Curso deve possuir pelo menos um docente !')

        # Codigo unico
        if len(self.env['transum.direcao_curso'].search([('codigo', '=', self.codigo)])) > 1:
            raise models.ValidationError('O código introduzido já está associado a outra Direção de Curso !')

        # DC por curso
        if len(self.env['transum.direcao_curso'].search([('curso_id', '=', self.curso_id.id)])) > 1:
            raise models.ValidationError('O curso seleccionado já possui uma Direção de Curso !')