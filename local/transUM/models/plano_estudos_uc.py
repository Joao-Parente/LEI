from odoo import models, fields


class Plano_Estudos_UC(models.Model):

    _name = 'transum.plano_estudos_uc'
    _order = 'designacao desc'
    _rec_name = 'designacao'
    _description = 'Plano de Estudos UC'
    active = fields.Boolean('Ativo?', default=True)

    creditacao = fields.Boolean('Creditação', default=False)
    nota = fields.Float('Nota')

    uc = fields.Many2one('transum.uc', 'Unidades Curriculares')

    plano_estudos = fields.Many2one('transum.plano_estudos', 'Plano de Estudos')

    designacao = fields.Char(compute='_compute_designacao', string="Ano - Semestre :: UC -  Nota ou Creditada")

    def _compute_designacao(self):
        for plano_estudos_uc in self:
            if not plano_estudos_uc.creditacao :
                plano_estudos_uc.designacao = plano_estudos_uc.uc.ano + ' ano - ' + plano_estudos_uc.uc.semestre + 'º Sem. :: ' + plano_estudos_uc.uc.designacao + ' = Nota: ' + str(plano_estudos_uc.nota)
            else:
                plano_estudos_uc.designacao = plano_estudos_uc.uc.ano + ' ano - ' + plano_estudos_uc.uc.semestre + 'º Sem. :: ' + plano_estudos_uc.uc.designacao + ' = Creditada'