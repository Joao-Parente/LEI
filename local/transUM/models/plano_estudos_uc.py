from odoo import models, fields
class Plano_Estudos_UC(models.Model):

    #_inherits = {'res.users': 'user_id'}
    _name='transum.plano_estudos_uc'
    _description = 'Plano de Estudos UC'
    active = fields.Boolean('Active?', default=True)

    uc = fields.Many2one('transum.uc','Unidade Curricular')
    creditacao = fields.Boolean('Creditação', default=False)
    nota = fields.Float('Nota')
    plano_estudos = fields.Many2one('transum.plano_estudos','Plano de Estudos')
