from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Direcao_Curso(models.Model):

    _name = 'transum.direcao_curso'
    _order = 'codigo desc'
    _rec_name = 'codigo'
    _description = 'Direção de Curso'
    active = fields.Boolean('Ativo?', default=True)

    codigo = fields.Char('Código')

    curso_id = fields.Many2one('transum.curso', 'Curso ID')
    curso_designacao = fields.Char('Designação', related='curso_id.designacao')
    curso_departamento = fields.Char('Departamento', related='curso_id.departamento')
    curso_tipo = fields.Selection([('1', 'Licenciatura'), ('2', 'Mestrado Integrado'), ('3', 'Mestrado')], related='curso_id.tipo')

    docentes = fields.Many2many('transum.docente', string='Docentes')

    planos_estudo = fields.One2many('transum.plano_estudos', 'dc_associada', 'Planos de Estudos')


    @api.model
    def create(self, vals):
        new_record = super().create(vals)
        grouprel = self.env['res.groups'].search([('name', '=', 'Direcao de Curso')])

        for docente_id in vals['docentes'][0][2]:
            docente = self.env['transum.docente'].browse(docente_id)
            grouprel.write({'users': [(4, docente.user_id.id)]})

        return new_record


    def write(self, vals):
        grouprel_docente = self.env['res.groups'].search([('name', '=', 'Docente')])
        grouprel_dc = self.env['res.groups'].search([('name', '=', 'Direcao de Curso')])

        if 'docentes' in vals:
            lista_ids_antiga = [d.user_id.id for d in self.docentes]
            lista_ids_nova = [self.env['transum.docente'].browse(d).user_id.id for d in vals['docentes'][0][2]]

            # Não permitir que o docente se remova a ele próprio
            if self._uid not in lista_ids_nova and self._uid in lista_ids_antiga:
                raise ValidationError('Não é possível remover-se a si próprio da Direção de Curso. Contacte o Administrador para este efeito.')

            docentes_remover = [d for d in self.docentes if d.user_id.id not in lista_ids_nova]
            docentes_ids_adicionar = [d for d in lista_ids_nova if d not in lista_ids_antiga]

            # Remover docentes antigos
            for docente in docentes_remover:
                if len(docente.direcoes_curso) <= 1:
                    grouprel_dc.write({'users': [(3, docente.user_id.id)]})
                    grouprel_docente.write({'users': [(4, docente.user_id.id)]})

            # Adicionar novos docentes
            for docente_id in docentes_ids_adicionar:
                grouprel_dc.write({'users': [(4, docente_id)]})
                grouprel_docente.write({'users': [(3, docente_id)]})

        return super().write(vals)


    @api.constrains('codigo', 'curso_id', 'docentes')
    def _check_dc(self):
        # Campos vazios
        if not self.codigo or not self.curso_id:
            raise models.ValidationError('Uma Direção de Curso deve possuir um código e um curso associado !')

        if not self.docentes:
            raise models.ValidationError('Uma Direção de Curso deve possuir pelo menos um docente !')

        # Codigo unico
        if len(self.env['transum.direcao_curso'].search([('codigo', '=', self.codigo)])) > 1:
            raise models.ValidationError('O código introduzido já está associado a outra Direção de Curso !')

        # DC por curso
        if len(self.env['transum.direcao_curso'].search([('curso_id', '=', self.curso_id.id)])) > 1:
            raise models.ValidationError('O curso seleccionado já possui uma Direção de Curso !')
