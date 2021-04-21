from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Plano_Curso(models.Model):

    _name = 'transum.plano_curso'
    _order = 'codigo desc'
    _rec_name = 'codigo'
    _description = 'Plano de Curso'
    active = fields.Boolean('Ativo?', default=True)

    codigo = fields.Char('Código')

    curso_id = fields.Many2one('transum.curso', 'Curso')

    ucs = fields.Many2many('transum.uc', string='Unidades Curriculares')

    # Nao ligado ao plano de transicao
    # plano_antigo = fields.Many2one('transum.plano_transicao','Plano de Curso Antigo')
    # plano_novo = fields.Many2one('transum.plano_transicao','Planos de Curso Novos')

    
    @api.constrains('codigo', 'curso_id', 'ucs')
    def _check_plano_curso(self):
        # Campos vazios
        if not self.codigo or not self.curso_id:
            raise models.ValidationError('Um Plano de Curso deve possuir um código e um curso !')
        if not self.ucs:
            raise models.ValidationError('Um Plano de Curso deve possuir unidades curriculares !')
        
        # ID unico
        if len(self.env['transum.plano_curso'].search([('codigo', '=', self.codigo)])) > 1:
            raise models.ValidationError('O código introduzido já está associado a outro Plano de Curso !')
        
        # PC por curso
        if len(self.env['transum.plano_curso'].search([('curso_id', '=', self.curso_id.id)])) > 1:
            raise models.ValidationError('O curso introduzido já possui um Plano de Curso definido !')

    
    def gerar(self):
        curso = self.env['transum.curso'].search([('id', '=', self.curso_id.id)])

        plano_estudos = self.env['transum.plano_estudos']
        plano_estudos_uc = self.env['transum.plano_estudos_uc']

        for aluno in curso.alunos:
            pl_est_aluno = plano_estudos.create([{
                'codigo': 'Plano_Estudos_' + aluno.nr_mecanografico,
                'dc_associada': curso.direcao_curso[0].id,
                'aluno_associado': aluno.id
            }])
            plano_estudos.write(pl_est_aluno)

            for uc in self.ucs:
                pl_est_uc = plano_estudos_uc.create([{
                    'uc': uc.id,
                    'creditacao': False,
                    'nota': 0,
                    'plano_estudos': pl_est_aluno.id
                }])
                plano_estudos_uc.write(pl_est_uc)
