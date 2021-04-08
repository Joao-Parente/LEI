from odoo import models, fields


class UC(models.Model):

    #_inherits = {'res.users': 'user_id'}
    _name = 'transum.uc'
    _order = 'codigo desc'
    _rec_name = 'codigo_designacao'
    _description = 'Unidade Curricular'
    active = fields.Boolean('Active?', default=True)

    ects = fields.Integer('Créditos', default=5)
    designacao = fields.Char('Designação')
    codigo = fields.Char('Código')
    ano = fields.Selection([('1', '1º ano'), ('2', '2º ano'), ('3', '3º ano'), ('4', '4º ano'), ('5', '5º ano')], default='1')
    semestre = fields.Selection([('1', '1º Semestre'), ('2', '2º Semestre')], default='1')
    obrigatoria = fields.Boolean('Obrigatória?', default=True)        
    tem_opcao = fields.Boolean('Tem Opções?')

    uc_opcao = fields.Many2one('transum.uc', string='UC de Opção')
    uc_principal = fields.One2many('transum.uc', 'uc_opcao', string='UC Opcional')

    plano_estudos = fields.One2many('transum.plano_estudos_uc', 'uc', string='Planos de Estudos')
    
    uc_antiga_transicao = fields.Many2one('transum.plano_transicao_uc', string='UC Antiga')
    uc_nova_transicao = fields.Many2one('transum.plano_transicao_uc', string='UC Nova')

    plano_curso = fields.Many2many('transum.plano_curso', string='Plano de Curso')

    codigo_designacao = fields.Char(compute='_compute_codigo_designacao')

    def _compute_codigo_designacao(self):
        for uc in self:
            uc.codigo_designacao = uc.codigo + ' - ' + uc.designacao