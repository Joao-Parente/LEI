from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Plano_Estudos_UC(models.Model):

    _name = 'transum.plano_estudos_uc'
    _order = 'designacao desc' #isto da warning
    _rec_name = 'designacao'
    _description = 'Plano de Estudos UC'
    active = fields.Boolean('Ativo?', default=True)

    creditacao = fields.Boolean('Creditação', default=False)
    nota = fields.Float('Nota')

    uc = fields.Many2one('transum.uc', 'Unidades Curriculares')

    plano_estudos = fields.Many2one('transum.plano_estudos', 'Plano de Estudos')

    designacao = fields.Char(compute='_compute_designacao', string="Ano - Semestre :: UC -  Nota ou Creditada")

    
    @api.constrains('creditacao', 'nota', 'uc')
    def _check_plano_estudos_uc(self):            
        for record in self:
            # Campos vazios
            if not record.uc :
                raise models.ValidationError('Deve indicar uma Unidade Curricular !')

            # Validar nota
            if not record.creditacao and (record.nota < 0 or record.nota > 20):
                raise models.ValidationError('Nota inválida !')

            # Validar creditação
            if record.creditacao and record.nota != 0:
                raise models.ValidationError('Se foi creditada não é indicado a nota !')
    

    def _compute_designacao(self):
        for record in self:
            if not record.creditacao :
                record.designacao = record.uc.ano + ' ano - ' + record.uc.semestre + 'º Sem. :: ' + record.uc.designacao + ' = Nota: ' + str(record.nota)
            else:
                record.designacao = record.uc.ano + ' ano - ' + record.uc.semestre + 'º Sem. :: ' + record.uc.designacao + ' = Creditada'
