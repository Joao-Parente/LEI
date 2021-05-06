from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Plano_Transicao(models.Model):


    _name = 'transum.plano_transicao'
    _order = "designacao desc"
    _rec_name = 'designacao'
    _description = 'Plano de Transição'
    active = fields.Boolean('Ativo?', default=True)

    designacao = fields.Char('Designação')

    curso_id = fields.Many2one('transum.curso', 'Curso')

    cursos_novos = fields.One2many('transum.curso','transicao_cursos_novos','Cursos Novos')

    transicao_ucs = fields.One2many('transum.plano_transicao_uc', 'plano_transicao', 'Correspondência')

    @api.constrains('designacao', 'transicao_ucs', 'curso_id')
    def _check_plano_curso(self):
        # Campos vazios
        if not self.designacao or not self.curso_id:
            raise models.ValidationError('Um Plano de Transição deve possuir uma designação e um curso !')
        if not self.transicao_ucs:
            raise models.ValidationError('Um Plano de Transição deve possuir pelo menos uma correspondência !')
        # Plano de Transicao por Curso
        if len(self.env['transum.plano_transicao'].search([('curso_id', '=', self.curso_id.id)])) > 1:
            raise models.ValidationError('O curso introduzido já está associado a outro Plano de Transição !')
        
        for uc_transicao in self.transicao_ucs:
            plano_transicao_uc = self.env['transum.plano_transicao_uc'].search([('id', '=', uc_transicao.id)])
            if not plano_transicao_uc.curso_antigo.id == self.curso_id.id:
                raise models.ValidationError('A Correspondência deve possuir Unidades Curriculares do Curso Antigo!')
         

    def transitar(self):
        curso = self.env['transum.curso'].search([('id', '=', self.curso_id.id)])
        
        plano_estudos = self.env['transum.plano_estudos']
        plano_estudos_uc = self.env['transum.plano_estudos_uc']
        proposta_novo_plano = self.env['transum.proposta_novo_plano']

        for aluno in curso.alunos:
            if aluno.estado == '1':
                for plano in aluno.planos_atuais:
                    proposta = proposta_novo_plano.create([{
                        'plano_antigo': plano.id,
                        'plano_transicao': self.id 
                    }])
                    proposta_novo_plano.write(proposta)

                    aluno.estado = '2'
                    aluno.proposta_plano_aluno = proposta.id

                    for cn in self.cursos_novos:
                        pl_est_aluno = plano_estudos.create([{
                            'codigo': cn.tipo + '_Novo_Plano_Estudos_' + aluno.nr_mecanografico,
                            'dc_associada': cn.direcao_curso[0].id,
                            'proposta_nova': proposta.id
                            #'aluno_associado': aluno.id
                        }])
                        plano_estudos.write(pl_est_aluno)

                        for uc in cn.plano_curso[0].ucs:
                            pl_est_uc = plano_estudos_uc.create([{
                                'uc': uc.id,
                                'creditacao': False,
                                'nota': 0,
                                'plano_estudos': pl_est_aluno.id
                            }])
                            plano_estudos_uc.write(pl_est_uc)


                       

                        for uc_transicao in self.transicao_ucs:

                            print("hiii" + str(len(uc_transicao.uc_antiga)) +" e noba" + str(len(uc_transicao.uc_antiga)) )

                            #Verificar na view que não ha N->N

                            #   1 -> 1
                            if len(uc_transicao.uc_antiga)==1 and len(uc_transicao.uc_nova)==1 :
                                print("1->1")
                                pros = proposta_novo_plano.search([('id','=',proposta.id)])

                                for info_uc in plano.nota_uc:
                                     if info_uc.uc.codigo == uc_transicao.uc_antiga[0].codigo:

                                        for plano22 in pros.planos_novos:
                                            if plano22.existe_uc(uc_transicao.uc_nova[0].codigo,info_uc.nota) == True:
                                                break

                            #   1 -> N
                            if len(uc_transicao.uc_antiga)==1 and len(uc_transicao.uc_nova)>1 :
                                print("1->N")
                                pros = proposta_novo_plano.search([('id','=',proposta.id)])

                                for info_uc in plano.nota_uc:
                                     if info_uc.uc.codigo == uc_transicao.uc_antiga[0].codigo:

                                        for plano22 in pros.planos_novos:
                                            for uc_novas in uc_transicao.uc_nova:
                                                if plano22.existe_uc(uc_novas.codigo,info_uc.nota) == True:
                                                    print()
                                                  
                               

                            print("N->1")   
                            # N -> 1
                            if len(uc_transicao.uc_antiga)>1 and len(uc_transicao.uc_nova)==1 :
                                print("N->1")

                                somatorio = 0.0
                                total = 0
                                for antiga_uc in uc_transicao.uc_antiga:
                                    for info_uc in plano.nota_uc:
                                         if info_uc.uc.codigo == antiga_uc.codigo:
                                            somatorio += info_uc.nota * info_uc.creditos
                                            total += info_uc.creditos

                                media_pesada = somatorio / total

                                pros = proposta_novo_plano.search([('id','=',proposta.id)])
                                for plano22 in pros.planos_novos:
                                    if plano22.existe_uc(uc_transicao.uc_nova[0].codigo,media_pesada) == True:
                                     break



                    proposal = proposta_novo_plano.search([('id','=',proposta.id)])
                    """ for pplano in proposal.planos_novos:
                        if pplano.total_creditos_falta == 0:
                            pplano.active = False """

                    creditacao = plano.creditos_creditados()
                    if plano.total_creditos_falta + creditacao > plano.total_creditos_feitos - creditacao:
                        proposal.aprovar() 

                    break
            