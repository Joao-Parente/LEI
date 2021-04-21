from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Aluno(models.Model):

    #_inherits = {'res.users': 'user_id'}
    _name = 'transum.aluno'
    _order = "nr_mecanografico desc"
    _rec_name = 'nr_mecanografico'
    _description = "Aluno"
    active = fields.Boolean('Ativo?', default=True)

    nr_mecanografico = fields.Char('Nº Mecanográfico')
    nome = fields.Char('Nome')
    email = fields.Char('Email')
    estado = fields.Selection([('1','Não Transitado'),('2','Em Transição'),('3','Transitado')], default='1')
    ano = fields.Selection([('1','1º ano'),('2','2º ano'),('3','3º ano'),('4','4º ano'),('5','5º ano'),('6','6º ano')], default='1')
    estatuto = fields.Selection([('1','Estudante'),('2','Trabalhador Estudante'),('3','Estudante Atleta')], default='1')

    curso_id = fields.Many2many('transum.curso', string='Curso')

    planos_atuais = fields.One2many('transum.plano_estudos', 'aluno_associado', 'Atuais')
    plano_historico = fields.One2many('transum.plano_estudos', 'historico_aluno_associado', 'Histórico')

    proposta_plano_aluno = fields.Many2one('transum.proposta_novo_plano', 'Proposta')

    @api.model
    def create(self, vals):

        #print('\n\n\n\n\n\nvals -> '+str(vals)+'\n\n\n\n\n\n')

        list_plano_estudos = []
        for c in vals['curso_id']:

            #print('\n\n\n\n\n\nc -> '+str(c[2][0])+'\n\n\n\n\n\n')

            curso = self.env['transum.curso'].search([('id', '=', c[2][0])])

            #print('\n\n\n\n\n\ndepartamento curso -> '+curso.departamento+'\n\n\n\n\n\n')
            # ERRO NA LINHA ABAIXO : unhashable type: 'list
            
            
            
            list_planos_curso = curso.get_plano_curso()
            
            for plano_curso_id in list_planos_curso:
                plano_curso = self.env['transum.plano_curso'].search([('id', '=', plano_curso_id)])
                #print('\n\n\n\n\n\nplano curso codigo-> '+plano_curso.codigo+'\n\n\n\n\n\n')
                pl_est_aluno = self.env['transum.plano_estudos'].create([{
                    'codigo': 'Plano_Estudos_' + vals['nr_mecanografico'] 
                }])
                self.env['transum.plano_estudos'].write(pl_est_aluno)
                
                list_plano_estudos.append(pl_est_aluno.id)

                for uc in plano_curso.ucs:
                    pl_est_uc = self.env['transum.plano_estudos_uc'].create([{
                        'nota': 0.0,
                        'uc': uc.id,
                        'plano_estudos': pl_est_aluno.id
                    }])
                    self.env['transum.plano_estudos_uc'].write(pl_est_uc)
                    #print('\n\n\n\n\n\nestou na 62 plestuc -> '+ str(pl_est_uc) +'\n\n\n\n\n\n')
                            

        # Não sei se está correto.
        print('\n\n\n\n\n\nantes da 68 -> '+str(list_plano_estudos)+'\n\n\n\n\n\n')
        #for abc in
        #vals["planos_atuais"] = list_plano_estudos
        vals["planos_atuais"] = (6, 0, list_plano_estudos)

        return super().create(vals)

    
    @api.constrains('nr_mecanografico', 'email', 'nome')
    def _check_aluno(self):   
        # Campos vazios 
        if not self.nr_mecanografico or not self.email or not self.nome:
            raise models.ValidationError('Um Aluno deve possuir um nº mecanográfico, um email e um nome !')
            
        # ID unico
        if len(self.env['transum.aluno'].search([('nr_mecanografico', '=', self.nr_mecanografico)])) > 1:
            raise models.ValidationError('O nº mecanográfico introduzido já está associado a outro Aluno !')
        
        # Curso deve possuir um P.C
        for c in self.curso_id:
            curso = self.env['transum.curso'].browse(c.id)
            plano_curso = curso.get_plano_curso()
            if not plano_curso:
                raise models.ValidationError('O Curso selecionado não possui um Plano de Curso !')
                            
