# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PetClinicClient(models.Model):
    _name = 'pet_clinic.client'
    _description = 'Client / Pemilik Hewan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id_client desc'

    id_client = fields.Char(
        string='Client ID',
        readonly=True,
        copy=False,
        default='New',
        tracking=True,
    )
    name = fields.Char(string='Name', required=True, tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    address = fields.Char(string='Address', tracking=True)
    pet_ids = fields.One2many(
        'pet_clinic.pet', 'owner_id', string='Pets',
    )
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('id_client', 'New') == 'New':
                vals['id_client'] = self.env['ir.sequence'].next_by_code(
                    'pet_clinic.client'
                ) or 'New'
        return super().create(vals_list)

    def name_get(self):
        result = []
        for rec in self:
            name = f"[{rec.id_client}] {rec.name}" if rec.id_client else rec.name
            result.append((rec.id, name))
        return result
