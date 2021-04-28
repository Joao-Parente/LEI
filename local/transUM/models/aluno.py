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
    # nome = fields.Char('Nome')
    #email = fields.Char('Email')
    estado = fields.Selection([('1','Não Transitado'),('2','Em Transição'),('3','Transitado')], default='1')
    ano = fields.Selection([('1','1º ano'),('2','2º ano'),('3','3º ano'),('4','4º ano'),('5','5º ano'),('6','6º ano')], default='1')
    estatuto = fields.Selection([('1','Estudante'),('2','Trabalhador Estudante'),('3','Estudante Atleta')], default='1')

    curso_id = fields.Many2many('transum.curso', string='Curso')

    planos_atuais = fields.One2many('transum.plano_estudos', 'aluno_associado', 'Atuais')
    plano_historico = fields.One2many('transum.plano_estudos', 'historico_aluno_associado', 'Histórico')

    proposta_plano_aluno = fields.Many2one('transum.proposta_novo_plano', 'Proposta')

    
    @api.constrains('nr_mecanografico', 'email', 'nome')
    def _check_aluno(self):   
        # Campos vazios
        #if not self.nr_mecanografico or not self.email or not self.nome:
        if not self.nr_mecanografico :
            raise models.ValidationError('Um Aluno deve possuir um nº mecanográfico, um email e um nome !')
            
        # ID unico
        if len(self.env['transum.aluno'].search([('nr_mecanografico', '=', self.nr_mecanografico)])) > 1:
            raise models.ValidationError('O nº mecanográfico introduzido já está associado a outro Aluno !')


    @api.model
    def create(self, vals):

        new_record = super().create(vals)

        grouprel=self.env['res.groups'].search([('name', '=', 'Aluno')])
        grouprel.write({
            'users': [(4, new_record.user_id.id)]
        })

        return new_record