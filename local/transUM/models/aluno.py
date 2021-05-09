from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Aluno(models.Model):

    _inherits = {'res.users': 'user_id'}
    _name = 'transum.aluno'
    _order = "nr_mecanografico desc"
    _rec_name = 'nr_mecanografico'
    _description = "Aluno"
    active = fields.Boolean('Ativo?', default=True)

    nr_mecanografico = fields.Char('Nº Mecanográfico')
    estado = fields.Selection([('1', 'Não Transitado'), ('2', 'Em Transição'), ('3', 'Aceitou a Transição'), ('4', 'Não aceitou a Transição')], default='1')
    ano = fields.Selection([('1', '1º ano'), ('2', '2º ano'), ('3', '3º ano'), ('4', '4º ano'), ('5', '5º ano'), ('6', '6º ano')], default='1')
    estatuto = fields.Selection([('1', 'Estudante'), ('2', 'Trabalhador Estudante'), ('3', 'Estudante Atleta')], default='1')

    curso_id = fields.Many2many('transum.curso', string='Curso')

    planos_atuais = fields.One2many('transum.plano_estudos', 'aluno_associado', 'Atuais')
    plano_historico = fields.One2many('transum.plano_estudos', 'historico_aluno_associado', 'Histórico')

    proposta_plano_aluno = fields.Many2one('transum.proposta_novo_plano', 'Proposta')


    @api.constrains('nr_mecanografico', 'name', 'login', 'password', 'curso_id')
    def _check_aluno(self):
        # Campos vazios
        if not self.nr_mecanografico or not self.name :
            raise models.ValidationError('Um Aluno deve possuir um nº mecanográfico, um email, um nome e uma password !')

        # ID unico
        if len(self.env['transum.aluno'].search([('nr_mecanografico', '=', self.nr_mecanografico)])) > 1:
            raise models.ValidationError('O número mecanográfico introduzido já está associado a outro Aluno !')

        # Curso
        if not self.curso_id:
            raise models.ValidationError('Um Aluno deve possuir pelo menos um Curso !')

        # Existir um plano de curso associado ao Curso
        for curso in self.curso_id:
            curso = self.env['transum.curso'].search([('id', '=', curso.id)])
            if not len(curso.get_plano_curso()) > 0:
                raise models.ValidationError('O Curso escolhido não possui um Plano de Curso associado !')


    @api.model
    def create(self, vals):
        new_record = super().create(vals)

        grouprel = self.env['res.groups'].search([('name', '=', 'Aluno')])
        grouprel.write({'users': [(4, new_record.user_id.id)]})

        return new_record
