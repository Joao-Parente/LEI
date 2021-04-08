from odoo import models, fields


class Curso(models.Model):

    _name = 'transum.curso'
    _order = "designacao desc"
    _rec_name = 'designacao'
    _description = "Curso"
    active = fields.Boolean('Active?', default=True)

    designacao = fields.Char('Designação')
    departamento = fields.Char('Departamento')
    tipo = fields.Selection([('1', 'Licenciatura'), ('2', 'Mestrado Integrado'), ('3', 'Mestrado')], default=1)

    alunos = fields.Many2many('transum.aluno', string='Alunos')

    direcao_curso = fields.One2many('transum.direcao_curso', 'curso_id', 'Direção de Curso')

    plano_curso = fields.One2many('transum.plano_curso', 'curso_id', 'Plano de Curso')