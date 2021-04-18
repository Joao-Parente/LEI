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

    transicao_ucs = fields.One2many('transum.plano_transicao_uc', 'plano_transicao', 'Correspondência')

    #plano_curso_antigo = fields.One2Many('transum.plano_curso','','Plano de Curso Antigo')
    #plano_curso_novo = fields.One2Many('transum.plano_curso','','Planos de Curso Novos')


    @api.constrains('designacao', 'transicao_ucs')
    def _check_plano_curso(self):
        # Campos vazios
        if not self.designacao or not self.curso_id:
            raise models.ValidationError('Um Plano de Transição deve possuir uma designação e um curso !')
        if not self.transicao_ucs:
            raise models.ValidationError('Um Plano de Transição deve possuir pelo menos uma correspondência !')


    def transitar(self):
        curso = self.env['transum.curso'].search([('id', '=', self.curso_id.id)])
        
        plano_estudos = self.env['transum.plano_estudos']
        plano_estudos_uc = self.env['transum.plano_estudos_uc']
        proposta_novo_plano = self.env['transum.proposta_novo_plano']

        for aluno in curso.alunos:

            for plano in aluno.planos_atuais:
                proposta = proposta_novo_plano.create([{
                    'plano_antigo': plano.id,
                    'plano_transicao': self.id 
                }])
                proposta_novo_plano.write(proposta)

                aluno.proposta_plano_aluno = proposta.id

                plano_novo = plano_estudos.create([{
                    'codigo': 'Novo_Plano_' + plano.codigo,
                    'dc_associada': plano.dc_associada.id,
                    'proposta_nova': proposta.id
                }])
                plano_estudos.write(plano_novo)


                for uc_transicao in self.transicao_ucs:
                    transicao = None
                    
                    for antiga_uc in uc_transicao.uc_antiga:
                        for info_uc in plano.nota_uc:
                            if info_uc.uc.codigo == antiga_uc.codigo:
                                transicao = info_uc
                           
                    uc_plano = plano_estudos_uc.create([{
                        'creditacao': transicao.creditacao,
                        'nota': transicao.nota,
                        'uc': uc_transicao.uc_nova[0].id,
                        'plano_estudos': plano_novo.id
                    }])
                    plano_estudos_uc.write(uc_plano)
                        
                break