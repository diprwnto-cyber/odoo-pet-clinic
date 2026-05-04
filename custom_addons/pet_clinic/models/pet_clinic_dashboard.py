# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta


class PetClinicDashboard(models.TransientModel):
    _name = 'pet_clinic.dashboard'
    _description = 'Pet Clinic Dashboard'

    lokasi_id = fields.Many2one(
        'pet_clinic.lokasi', string='Lokasi',
    )
    date_from = fields.Date(
        string='Date From',
        default=lambda self: fields.Date.today().replace(day=1),
    )
    date_to = fields.Date(
        string='Date To',
        default=fields.Date.today,
    )
