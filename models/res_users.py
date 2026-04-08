from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    access_card_ids = fields.One2many(
        'office.access.card',
        'user_id',
        string='Tarjetas de Acceso'
    )

    access_card_count = fields.Integer(
        string='Cantidad de Tarjetas',
        compute='_compute_access_card_count',
        store=True
    )

    @api.depends('access_card_ids')
    def _compute_access_card_count(self):
        for user in self:
            user.access_card_count = len(user.access_card_ids)