from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Curso(models.Model):

    _name = 'transum.curso'
    _order = "designacao desc"
    _rec_name = 'designacao'
    _description = "Curso"
    active = fields.Boolean('Ativo?', default=True)

    designacao = fields.Char('Designação')
    departamento = fields.Char('Departamento')
    tipo = fields.Selection([('1', 'Licenciatura'), ('2', 'Mestrado Integrado'), ('3', 'Mestrado')], default='1')

    direcao_curso = fields.One2many('transum.direcao_curso', 'curso_id', 'Direção de Curso')

    alunos = fields.Many2many('transum.aluno', string='Alunos')

    plano_curso = fields.One2many('transum.plano_curso', 'curso_id', 'Planos de Curso')

    plano_transicao = fields.One2many('transum.plano_transicao', 'curso_id', 'Planos de Transição')

    transicao_cursos_novos = fields.Many2one('transum.plano_transicao', 'Cursos Novos')


    @api.constrains('designacao', 'departamento')
    def _check_curso(self):
        # Campos vazios
        if not self.designacao or not self.departamento:
            raise models.ValidationError('Um Curso deve possuir uma designação e um departamento !')


    def get_plano_curso(self) -> list:
        list_plano_curso = []

        for rec in self:
            if not rec.plano_curso:
                return list_plano_curso

            for pc in rec.plano_curso:
                list_plano_curso.append(pc.id)

        return list_plano_curso


    def existe_no_plano_curso(self, uc) -> bool:
        for record in self:
            uc_a_pesquisar = self.env['transum.uc'].search([('id', '=', uc)])

            for pc in record.plano_curso:
                pln_crs = self.env['transum.plano_curso'].search([('id', '=', pc.id)])

                for uc in pln_crs.ucs:
                    if uc.codigo == uc_a_pesquisar.codigo:
                        return True
        return False

    def ativar(self):
        for rec in self:
            rec.active = True

    def desativar(self):
        for rec in self:
            rec.active = False