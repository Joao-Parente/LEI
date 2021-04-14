from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Plano_Transicao(models.Model):

    #plano de transicao ligado a um curso?

    _name = 'transum.plano_transicao'
    _order = "designacao desc"
    _rec_name = 'designacao'
    _description = 'Plano de Transição'
    active = fields.Boolean('Ativo?', default=True)

    designacao = fields.Char('Designação')

    transicao_ucs = fields.One2many('transum.plano_transicao_uc', 'plano_transicao', 'Correspondência')

    #plano_curso_antigo = fields.One2Many('transum.plano_curso','','Plano de Curso Antigo')
    #plano_curso_novo = fields.One2Many('transum.plano_curso','','Planos de Curso Novos')

    @api.constrains('designacao', 'transicao_ucs')
    def _check_plano_curso(self):
        # Campos vazios
        if not self.designacao:
            raise models.ValidationError('Um Plano de Transição deve possuir uma designação !')
        if not self.transicao_ucs:
            raise models.ValidationError('Um Plano de Transição deve possuir pelo menos uma correspondência !')

    def transitar(self): 
        todos_os_alunos = self.env['transum.aluno']
        alunos = self.env['transum.aluno'].search([('nr_mecanografico', '=', 'a84829')]) 
        p_estudos = self.env['transum.plano_estudos']
        p_estudo_uc = self.env['transum.plano_estudos_uc']
        p_novo_plano = self.env['transum.proposta_novo_plano']

        for aluno in alunos:

            p_atuais = aluno.planos_atuais
            
            aluno_plano_antigo = None
            aluno_planos_novos = None

            for plano in p_atuais:
                
                proposta_nova = p_novo_plano.create([{
                    'plano_antigo': plano.id,
                    'plano_transicao': self.id 
                }])
                p_novo_plano.write(proposta_nova)

                aluno.proposta_plano_aluno = proposta_nova.id

                stringue = 'novo_plano_a84829'
                pestudosnovo = p_estudos.create([{
                    'codigo': stringue,
                    'dc_associada': plano.dc_associada.id,
                    'aluno_associado': plano.aluno_associado.id,
                    'proposta_nova': proposta_nova.id
                }])
                p_estudo_uc.write(pestudosnovo)
                print('\n\ncriei o plano de estudos -> ' + str(pestudosnovo.id) + ', codigo = ' + pestudosnovo.codigo + '\n\n')
                ucs_feitas = plano.nota_uc

                for t_ucs in self.transicao_ucs:
                    uc_antiga = t_ucs.uc_antiga
                    uc_nova = t_ucs.uc_nova

                    abc = None
                    for antiga_uc in uc_antiga:
                        for uc_info in ucs_feitas:
                            if uc_info.uc.codigo == antiga_uc.codigo:
                                abc = uc_info
                           
                    adada = p_estudo_uc.create([{
                        'creditacao': abc.creditacao,
                        'nota': abc.nota,
                        'uc': uc_nova[0].id,
                        'plano_estudos': pestudosnovo.id
                    }])
                    p_estudo_uc.write(adada)
                        
                    print('\n\nCriou -> ' + str(adada.id) + '\n\n')

                break    

            

