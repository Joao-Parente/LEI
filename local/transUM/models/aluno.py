from odoo import models, fields
class Aluno(models.Model):

    #_inherits = {'res.users': 'user_id'}
    _name='transum.aluno'
    _description = 'Aluno'
    _order = 'name desc'
    active = fields.Boolean('Active?', default=True)

    nr_mecanografico = fields.Char('Nº Mecanográfico')
    name = fields.Char('Nome')
    email = fields.Char('Email')
    estado = fields.Selection([('1','Não Transitado'),('2','Em Transição'),('3','Transitado')], default='1')
    ano = fields.Selection([('1','1º ano'),('2','2º ano'),('3','3º ano'),('4','4º ano'),('5','5º ano'),('6','6º ano')], default='1')
    estatuto = fields.Selection([('1','Estudante'),('2','Trabalhador Estudante'),('3','Estudante Atleta')], default='1')
    curso_id = fields.Many2one('transum.curso', 'Curso')