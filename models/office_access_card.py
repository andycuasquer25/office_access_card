from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OfficeAccessCard(models.Model):
    _name = 'office.access.card'
    _description = 'Office Access Card'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string='Nombre',
        required=True,
        tracking=True
    )
    card_type = fields.Selection(
        [
            ('general', 'General'),
            ('restricted', 'Restringida'),
            ('visitor', 'Visitante'),
        ],
        string='Tipo de Tarjeta',
        required=True,
        tracking=True,
        default='general'
    )
    card_number = fields.Char(
        string='Número de Tarjeta',
        required=True,
        tracking=True,
        copy=False
    )
    issue_date = fields.Date(
        string='Fecha de Emisión',
        tracking=True,
        default=fields.Date.context_today
    )
    user_id = fields.Many2one(
        'res.users',
        string='Responsable',
        tracking=True
    )
    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('active', 'Activa'),
            ('blocked', 'Bloqueada'),
        ],
        string='Estado',
        default='draft',
        required=True,
        tracking=True
    )
    notes = fields.Text(
        string='Observaciones'
    )

    _sql_constraints = [
        (
            'office_access_card_number_unique',
            'unique(card_number)',
            'El número de tarjeta debe ser único.'
        )
    ]

    @api.model
    def create(self, vals):
        if vals.get('name'):
            vals['name'] = vals['name'].upper()
        return super(OfficeAccessCard, self).create(vals)

    def write(self, vals):
        if vals.get('name'):
            vals['name'] = vals['name'].upper()

        for rec in self:
            if rec.state == 'active' and 'card_number' in vals:
                raise ValidationError(
                    _('No se puede cambiar el número de una tarjeta activa.')
                )

        return super(OfficeAccessCard, self).write(vals)

    def action_activate_card(self):
        for rec in self:
            rec.state = 'active'

    def action_block_card(self):
        for rec in self:
            if rec.state != 'blocked' and not rec.notes:
                raise ValidationError(
                    _('Debes colocar una observación antes de bloquear la tarjeta.')
                )
            rec.state = 'blocked'

    def action_set_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_send_chatter_message(self):
        for rec in self:
            rec.message_post(
                body=_('Se realizó una validación manual de la tarjeta de acceso.')
            )