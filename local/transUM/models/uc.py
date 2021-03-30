from odoo import models, fields
class UC(models.Model):

    #_inherits = {'res.users': 'user_id'}
    _name='transum.uc'
    _description = 'Unidade Curricular'
    _order='designacao asc'
    _rec_name = 'codigo_designacao'
    active = fields.Boolean('Active?', default=True)

    codigo = fields.Char('Código UC')
    designacao = fields.Char('Designação')
    ects = fields.Integer('Créditos ECTS', default=5)
    obrigatoria = fields.Boolean('Obrigatória?')
    #ucs_plano_curso = fields.One2many('planum.uc_plano_curso', 'uc_id', 'UCs de Planos de Curso')
    codigo_designacao = fields.Char(compute='_compute_codigo_designacao')