from odoo import models, fields
class UC(models.Model):

    #_inherits = {'res.users': 'user_id'}
    _name='transum.uc'
    _description = 'Unidade Curricular'
    _order='designacao asc'
    _rec_name = 'codigo'
    active = fields.Boolean('Active?', default=True)

    codigo = fields.Char('Código UC')
    designacao = fields.Char('Designação')
    ects = fields.Integer('Créditos ECTS', default=5)
    obrigatoria = fields.Boolean('Obrigatória?', default=True)
    tem_opcao = fields.Boolean('Tem Opções?')
    ano = fields.Selection([('1','1º ano'),('2','2º ano'),('3','3º ano'),('4','4º ano'),('5','5º ano')], default='1')
    semestre = fields.Selection([('1','1º Semestre'),('2','2º Semestre')], default='1')
    uc_opcao = fields.Many2one('transum.uc', string='UC de Opção')
    uc_principal = fields.One2many('transum.uc','uc_opcao', string='UC Opcional')
    plano_curso = fields.Many2many('transum.plano_curso', string='Plano de Curso')
    plano_estudos = fields.One2many('transum.plano_estudos_uc','uc', string='UC Associada')
    uc_antiga_transicao = fields.Many2one('transum.plano_transicao_uc', string='UC Antiga')
    uc_nova_transicao = fields.Many2one('transum.plano_transicao_uc', string='UC Nova')
