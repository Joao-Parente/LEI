from odoo import models, fields
class Docente(models.Model):

    #_inherits = {'res.users': 'user_id'}
    _name='transum.docente'
    _description = 'Docente'
    _order = 'name desc'
    active = fields.Boolean('Active?', default=True)

    nr_mecanografico = fields.Char('Nº Mecanográfico')
    name = fields.Char('Nome')
    email = fields.Char('Email')
    direcoes_curso = fields.Many2many('transum.direcao_curso', string='DirecoesCurso')
    

