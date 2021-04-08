from odoo import models, fields


class Plano_Estudos_UC(models.Model):

    _name = 'transum.plano_estudos_uc'
    _order = 'designacao desc'
    _rec_name = 'designacao'
    _description = 'Plano de Estudos UC'
    active = fields.Boolean('Active?', default=True)

    creditacao = fields.Boolean('Creditação', default=False)
    nota = fields.Float('Nota')

    uc = fields.Many2one('transum.uc', 'Unidade Curricular')

    plano_estudos = fields.Many2one('transum.plano_estudos', 'Plano de Estudos')

    designacao = fields.Char(compute='_compute_designacao')

    def _compute_designacao(self):
        for plano_estudos_uc in self:
            if not plano_estudos_uc.creditacao :
                plano_estudos_uc.designacao = plano_estudos_uc.uc.ano + ' ano - ' + plano_estudos_uc.uc.semestre + 'º Sem. :: ' + plano_estudos_uc.uc.designacao + ' =  Nota:' + str(plano_estudos_uc.nota )
            else:
                plano_estudos_uc.designacao = plano_estudos_uc.uc.ano + ' ano - ' + plano_estudos_uc.uc.semestre + 'º Sem. :: ' + plano_estudos_uc.uc.designacaov+ ' = Creditada'