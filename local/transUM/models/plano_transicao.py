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

    cursos_novos = fields.One2many('transum.curso', 'transicao_cursos_novos', 'Cursos Novos')

    transicao_ucs = fields.One2many('transum.plano_transicao_uc', 'plano_transicao', 'Correspondência')


    @api.constrains('designacao', 'transicao_ucs', 'curso_id')
    def _check_plano_curso(self):
        # Campos vazios
        if not self.designacao or not self.curso_id:
            raise models.ValidationError('Um Plano de Transição deve possuir uma designação e um Curso !')
        """ if not self.transicao_ucs:
            raise models.ValidationError('Um Plano de Transição deve possuir pelo menos uma correspondência !') """

        # Plano de Transicao por Curso
        if len(self.env['transum.plano_transicao'].search([('curso_id', '=', self.curso_id.id)])) > 1:
            raise models.ValidationError('O Curso introduzido já está associado a outro Plano de Transição !')

        for uc_transicao in self.transicao_ucs:
            plano_transicao_uc = self.env['transum.plano_transicao_uc'].search([('id', '=', uc_transicao.id)])

            if not plano_transicao_uc.curso_antigo == self.curso_id:
                raise models.ValidationError('A Correspondência deve possuir Unidades Curriculares do Curso Antigo!')

            existe_curso = False
            for curso_novo in self.cursos_novos:
                if plano_transicao_uc.curso_novo.id == curso_novo.id:
                    existe_curso = True 
                    break
            if not existe_curso:
                raise models.ValidationError('A Correspondência deve possuir Unidades Curriculares do Curso Novo!')


    def transitar(self):
        curso = self.env['transum.curso'].search([('id', '=', self.curso_id.id)])

        plano_estudos = self.env['transum.plano_estudos']
        plano_estudos_uc = self.env['transum.plano_estudos_uc']
        proposta_novo_plano = self.env['transum.proposta_novo_plano']
        proposta_transicao = self.env['transum.plano_transicao_uc_mostra']

        count_alunos = 0
        for aluno in curso.alunos:
            if aluno.estado == '1':
                for plano in aluno.planos_atuais:
                    proposta = proposta_novo_plano.create([{
                        'plano_antigo': plano.id, 
                        'plano_transicao': self.id,
                        'transicao_ucs_mostra': []
                    }])
                    proposta_novo_plano.write(proposta)

                    aluno.estado = '2'
                    aluno.proposta_plano_aluno = proposta.id

                    for cn in self.cursos_novos:
                        pl_est_aluno = plano_estudos.create([{
                            'codigo': cn.tipo + '_Novo_Plano_Estudos_' + aluno.nr_mecanografico, 
                            'dc_associada': cn.direcao_curso[0].id, 
                            'proposta_nova': proposta.id
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

                    pros = proposta_novo_plano.search([('id', '=', proposta.id)])

                    flag = False

                    for uc_transicao in self.transicao_ucs:
                        #Verificar na view que não ha N->N

                        #   1 -> 1
                        if len(uc_transicao.uc_antiga) == 1 and len(uc_transicao.uc_nova) == 1:
                            for info_uc in plano.nota_uc:
                                if info_uc.uc.codigo == uc_transicao.uc_antiga[0].codigo:
                                    for plano22 in pros.planos_novos:
                                        if plano22.existe_uc(uc_transicao.uc_nova[0].codigo, info_uc.nota) == True:
                                            break

                                    pl_trans_uc = proposta_transicao.create([{
                                        'uc_antiga': uc_transicao.uc_antiga, 
                                        'uc_nova': uc_transicao.uc_nova, 
                                        'nota_antiga': info_uc.nota if info_uc.nota >= 10 else 0,
                                        'nota_nova': info_uc.nota if info_uc.nota >= 10 else 0,
                                        'curso_novo': uc_transicao.curso_novo.id,
                                        'curso_antigo': uc_transicao.curso_antigo.id,
                                        'proposta': proposta.id
                                    }])
                                    proposta_transicao.write(pl_trans_uc)
                                    break

                        #   1 -> N
                        if len(uc_transicao.uc_antiga) == 1 and len(uc_transicao.uc_nova) > 1:
                            for info_uc in plano.nota_uc:
                                if info_uc.uc.codigo == uc_transicao.uc_antiga[0].codigo:
                                    for plano22 in pros.planos_novos:
                                        for uc_novas in uc_transicao.uc_nova:
                                            if plano22.existe_uc(uc_novas.codigo, info_uc.nota) == True:
                                                continue

                                    pl_trans_uc = proposta_transicao.create([{
                                        'uc_antiga': uc_transicao.uc_antiga,
                                        'uc_nova': uc_transicao.uc_nova,
                                        'nota_antiga': info_uc.nota if info_uc.nota >= 10 else 0,
                                        'nota_nova': info_uc.nota if info_uc.nota >= 10 else 0,
                                        'curso_novo': uc_transicao.curso_novo.id,
                                        'curso_antigo': uc_transicao.curso_antigo.id,
                                        'proposta': proposta.id
                                    }])
                                    proposta_transicao.write(pl_trans_uc)
                                    break

                        # N -> 1
                        if len(uc_transicao.uc_antiga) > 1 and len(uc_transicao.uc_nova) == 1:
                            somatorio = 0.0
                            total = 0
                            flag_line = False
                            for antiga_uc in uc_transicao.uc_antiga:
                                for info_uc in plano.nota_uc:
                                    if info_uc.uc.codigo == antiga_uc.codigo:
                                        if info_uc.nota < 10:
                                            flag = True
                                            flag_line = True
                                        somatorio += info_uc.nota * info_uc.creditos
                                        total += info_uc.creditos

                            media_pesada = somatorio / total
                            if flag_line == True:
                                media_pesada = 0

                            for plano22 in pros.planos_novos:
                                if plano22.existe_uc(uc_transicao.uc_nova[0].codigo, media_pesada) == True:
                                    break

                            pl_trans_uc = proposta_transicao.create([{
                                'atencao': flag_line,
                                'uc_antiga': uc_transicao.uc_antiga,
                                'uc_nova': uc_transicao.uc_nova,
                                'nota_antiga': media_pesada,
                                'nota_nova': media_pesada,
                                'curso_novo': uc_transicao.curso_novo.id,
                                'curso_antigo': uc_transicao.curso_antigo.id,
                                'proposta': proposta.id
                            }])
                            proposta_transicao.write(pl_trans_uc)

                    proposal = proposta_novo_plano.search([('id', '=', proposta.id)])
                    """ for pplano in proposal.planos_novos:
                        if pplano.total_creditos_falta == 0:
                            pplano.active = False """

                    if flag == True:
                        proposal.opcao = '4'
                    else:
                        creditacao = plano.creditos_creditados()
                        if plano.total_creditos_falta + creditacao > plano.total_creditos_feitos - creditacao:
                            proposal.opcao = '2'
                    count_alunos += 1        
                    break
                
        messagem = 'Foram gerados ' + str(count_alunos) + ' Propostas !'
        message_id = self.env['transum.message.wizard'].create({'message': messagem})
        return {
            'name': 'Message',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'transum.message.wizard',
            'res_id': message_id.id,
            'target': 'new'
        }
                    