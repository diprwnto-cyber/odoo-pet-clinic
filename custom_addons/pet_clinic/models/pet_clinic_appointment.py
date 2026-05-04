# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PetClinicAppointment(models.Model):
    _name = 'pet_clinic.appointment'
    _description = 'Appointment / Janji Temu'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(
        string='Appointment No.',
        readonly=True,
        copy=False,
        default='New',
        tracking=True,
    )
    owner_id = fields.Many2one(
        'pet_clinic.client', string='Owner', tracking=True,
    )
    pet_id = fields.Many2one(
        'pet_clinic.pet', string='Pet', tracking=True,
    )
    room_id = fields.Many2one(
        'pet_clinic.room', string='Room',
    )
    location_id = fields.Many2one(
        'pet_clinic.lokasi', string='Location',
    )
    service_id = fields.Many2one(
        'product.product', string='Service',
        domain=[('type', '=', 'service')],
    )
    doctor_id = fields.Many2one(
        'pet_clinic.doctor', string='Doctor', tracking=True,
    )
    date = fields.Datetime(
        string='Date', required=True, tracking=True,
    )
    date_stop = fields.Datetime(
        string='Date End',
        compute='_compute_date_stop',
        store=True,
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancel', 'Cancel'),
        ],
        string='Status',
        default='draft',
        tracking=True,
    )
    color = fields.Integer(
        string='Color', compute='_compute_color',
    )

    @api.depends('date')
    def _compute_date_stop(self):
        for rec in self:
            if rec.date:
                rec.date_stop = fields.Datetime.add(
                    rec.date, hours=1,
                )
            else:
                rec.date_stop = False

    def _compute_color(self):
        doctor_colors = {}
        color_idx = 0
        for rec in self:
            if rec.doctor_id:
                if rec.doctor_id.id not in doctor_colors:
                    doctor_colors[rec.doctor_id.id] = color_idx
                    color_idx += 1
                rec.color = doctor_colors[rec.doctor_id.id]
            else:
                rec.color = 0

    @api.onchange('owner_id')
    def _onchange_owner_id(self):
        self.pet_id = False
        if self.owner_id:
            return {
                'domain': {
                    'pet_id': [('owner_id', '=', self.owner_id.id)]
                }
            }
        return {'domain': {'pet_id': []}}

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'pet_clinic.appointment'
                ) or 'New'
        return super().create(vals_list)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_create_visitation(self):
        """Create draft visitation from confirmed appointment."""
        self.ensure_one()
        visitation = self.env['pet_clinic.visitation'].create({
            'owner_id': self.owner_id.id,
            'pet_id': self.pet_id.id,
            'room_id': self.room_id.id if self.room_id else False,
            'lokasi_pemeriksaan': self.location_id.id if self.location_id else False,
            'doctor_id': self.doctor_id.id if self.doctor_id else False,
            'date_start': self.date,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visitation',
            'res_model': 'pet_clinic.visitation',
            'view_mode': 'form',
            'res_id': visitation.id,
        }
