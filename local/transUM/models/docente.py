from odoo import models, fields


class Docente(models.Model):

    #_inherits = {'res.users': 'user_id'}
    _name = 'transum.docente'
    _order = 'nr_mecanografico desc'
    _rec_name = 'nr_mecanografico'
    _description = 'Docente'
    active = fields.Boolean('Ativo?', default=True)

    nr_mecanografico = fields.Char('Nº Mecanográfico')    
    email = fields.Char('Email')
    nome = fields.Char('Nome')

    direcoes_curso = fields.Many2many('transum.direcao_curso', string='Direções de Curso')