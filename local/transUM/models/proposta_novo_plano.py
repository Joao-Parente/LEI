from odoo import models, fields, api


class Proposta_Novo_Plano(models.Model):

    _name = 'transum.proposta_novo_plano'
    _order = 'designacao desc'
    _rec_name = 'designacao'
    _description = 'Proposta De Novo Plano'
    active = fields.Boolean('Ativo?', default=True)

    opcao = fields.Selection([('1', 'Tem opção de escolha.'), ('2', 'Não possui opção de escolha.'), ('3', 'Aceitou a transição.'), ('4','Necessita de atenção.'), ('5', 'Rejeitou a transição.'), ('6', 'Aguardar pela assinatura.'), ('7', 'Aprovar assinatura.')], string='Observações', default='6')

    plano_antigo = fields.Many2one('transum.plano_estudos', 'Plano Antigo ID')    
    ucs_plano_antigo = fields.One2many('transum.plano_estudos_uc', 'plano_estudos', string='Plano de Estudos UCs', related='plano_antigo.nota_uc')

    planos_novos = fields.One2many('transum.plano_estudos', 'proposta_nova', 'Planos Novos')

    aluno = fields.One2many('transum.aluno', 'proposta_plano_aluno', 'Aluno Associado')

    plano_transicao = fields.Many2one('transum.plano_transicao', 'Plano de Transição')
    antigo_curso = fields.Many2one('transum.curso', 'Curso', related='plano_transicao.curso_id')
    antigo_curso_designacao = fields.Char('Designação', related='antigo_curso.designacao')
    antigo_curso_tipo = fields.Selection([('1', 'Licenciatura'), ('2', 'Mestrado Integrado'), ('3', 'Mestrado')], default='1', related='antigo_curso.tipo')
    str_antigo_curso = fields.Char(compute='_compute_str_antigo_curso')
    novos_cursos = fields.One2many('transum.curso', 'transicao_cursos_novos', 'Cursos Novos', related='plano_transicao.cursos_novos')
    ucs_plano_transicao = fields.One2many('transum.plano_transicao_uc', 'plano_transicao', string='Plano de Transição UCs', related='plano_transicao.transicao_ucs')

    transicao_ucs_mostra = fields.One2many('transum.plano_transicao_uc_mostra', 'proposta', string='Correspondência')

    designacao = fields.Char(compute='_compute_designacao', string='Proposta de Transição')

    record_file = fields.Binary(string='file', attachment=True, help='Upload the file')
    upload = fields.Boolean(string='Submeter?', default=False)

    def write(self, vals):
        if 'record_file' in vals:
            if not self.upload:
                self.upload = True
                self.opcao = '7'

        return super().write(vals)

    def _compute_designacao(self):
        for record in self:
            record.designacao = 'Proposta de Transição ' + str(record.id)
    
    def _compute_str_antigo_curso(self):
        for pnp in self:
            if pnp.antigo_curso_tipo == '1':
                pnp.str_antigo_curso = pnp.antigo_curso_designacao + ' :: Licenciatura \n'
            elif pnp.antigo_curso_tipo == '2':
                pnp.str_antigo_curso = pnp.antigo_curso_designacao + ' :: Mestrado Integrado \n'
            elif pnp.antigo_curso_tipo == '3':
                pnp.str_antigo_curso = pnp.antigo_curso_designacao + ' :: Mestrado \n'

    def aprovar(self):
        alunos = self.env['transum.aluno']
        direcoes_curso = self.env['transum.direcao_curso']
        planos_estudos = self.env['transum.plano_estudos']
        planos_transicao = self.env['transum.plano_transicao']

        for aluno_id in self.aluno:
            aluno = alunos.search([('id', '=', aluno_id.id)])
            
            list_cursos = []
            for plano_novo in self.planos_novos:
                plano_novo.aluno_associado = aluno.id
                
                dc = direcoes_curso.search([('id', '=', plano_novo.dc_associada.id)])        
                list_cursos.append(dc.curso_id.id)

            pln_antg = planos_estudos.search([('id', '=', self.plano_antigo.id)])
            pln_antg.aluno_associado = None
            pln_antg.historico_aluno_associado = aluno.id          

            #aluno.curso_id = [(6, 0, list_cursos)] 
            aluno.curso_id = list_cursos
            aluno.estado = '3'
            self.opcao = '3'

    def rejeitar(self):
        for aluno_id in self.aluno:
            aluno = self.env['transum.aluno'].search([('id', '=', aluno_id.id)])                
            aluno.estado = '4'
            self.opcao = '5'


    def aprovar_from_list(self):
        for rec in self:
            if rec.opcao != '1' and rec.opcao != '2':
                raise models.ValidationError('Not working' + str(rec.designacao))
            rec.aprovar()