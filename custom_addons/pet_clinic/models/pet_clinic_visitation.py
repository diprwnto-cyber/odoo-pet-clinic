# -*- coding: utf-8 -*-
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class PetClinicVisitation(models.Model):
    _name = 'pet_clinic.visitation'
    _description = 'Visitation / Kunjungan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(
        string='Visitation No.',
        readonly=True,
        copy=False,
        default='New',
        tracking=True,
    )
    nomor_rekam_medis = fields.Char(
        string='Nomor Rekam Medis', tracking=True,
    )
    owner_id = fields.Many2one(
        'pet_clinic.client', string='Owner', tracking=True,
    )
    pet_id = fields.Many2one(
        'pet_clinic.pet', string='Pet', tracking=True,
    )
    umur = fields.Char(
        string='Umur', compute='_compute_umur', store=True,
    )
    penanganan = fields.Selection(
        [('rawat_jalan', 'Rawat Jalan'), ('rawat_inap', 'Rawat Inap')],
        string='Penanganan',
        tracking=True,
    )
    room_id = fields.Many2one(
        'pet_clinic.room', string='Room', tracking=True,
        domain="[('lokasi_ids', '=?', lokasi_pemeriksaan)]",
    )
    price_list_id = fields.Many2one(
        'product.pricelist', string='Price List',
    )
    status_pasien = fields.Char(string='Status Pasien')

    # Right side header fields
    receptionist_id = fields.Many2one(
        'res.users', string='Receptionist',
        default=lambda self: self.env.user,
    )
    date_start = fields.Datetime(
        string='Date Start', default=fields.Datetime.now, tracking=True,
    )
    date_end = fields.Datetime(string='Date End', tracking=True)
    lokasi_pemeriksaan = fields.Many2one(
        'pet_clinic.lokasi', string='Lokasi Pemeriksaan',
    )
    lokasi_pendaftaran = fields.Char(string='Lokasi Pendaftaran')
    awal = fields.Char(string='Awal')
    id_so = fields.Many2one(
        'sale.order', string='Sale Order', readonly=True,
    )
    reminder_checkup = fields.Boolean(string='Reminder Checkup')

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('in_process', 'In Process'),
            ('done', 'Done'),
            ('cancel', 'Cancel'),
        ],
        string='Status',
        default='draft',
        tracking=True,
    )

    # Medical Records Tab
    doctor_id = fields.Many2one(
        'pet_clinic.doctor', string='Doctor', tracking=True,
        domain="[('lokasi_ids', '=?', lokasi_pemeriksaan)]",
    )
    paramedis_id = fields.Many2one(
        'pet_clinic.paramedis', string='Paramedis',
        domain="[('lokasi_ids', '=?', lokasi_pemeriksaan)]",
    )

    # Anamnesa Section
    anamnesa = fields.Text(string='Anamnesa')
    populasi_hewan = fields.Char(string='Populasi Hewan')
    lama_pemeliharaan = fields.Char(string='Lama Pemeliharaan')
    makan = fields.Char(string='Makan')
    minum = fields.Char(string='Minum')
    tempat_air_minum = fields.Char(string='Tempat Air Minum')

    keluhan_tujuan = fields.Text(string='Keluhan/Tujuan Kunjungan')
    sistem_pemeliharaan = fields.Char(string='Sistem Pemeliharaan')
    asal_hewan = fields.Char(string='Asal Hewan')
    jenis_makanan = fields.Char(string='Jenis Makanan')
    sumber_air_minum = fields.Char(string='Sumber Air Minum')

    # Pet Condition Section
    weight = fields.Float(string='Weight (Kg)')
    bcs = fields.Integer(string='BCS (1-9)')
    respiratory_rate = fields.Char(string='Respiratory Rate')
    warna_mukosa = fields.Char(string='Warna Mukosa')
    feces = fields.Char(string='Feces (1-7)')
    serumen_telinga = fields.Char(string='Serumen Telinga')
    nasal_discharge = fields.Char(string='Nasal Discharge')
    pemeriksaan_lainnya = fields.Text(string='Pemeriksaan Lainnya')
    diagnosis = fields.Text(string='Diagnosis')
    action_field = fields.Text(string='Action')

    temperature = fields.Float(string='Temperature (°C)')
    pulse_rate = fields.Char(string='Pulse Rate')
    fecal_scoring = fields.Char(string='Fecal Scoring (1-7)')
    dehidrasi = fields.Char(string='Dehidrasi')
    urin = fields.Char(string='Urin')
    ocular_discharge = fields.Char(string='Ocular Discharge')
    saliva = fields.Char(string='Saliva')
    diagnosa_sementara = fields.Text(string='Diagnosa Sementara')
    therapy = fields.Text(string='Therapy')

    # Tab lines
    service_ids = fields.One2many(
        'pet_clinic.service', 'visitation_id', string='Services',
    )
    item_ids = fields.One2many(
        'pet_clinic.visitation_item', 'visitation_id', string='Items',
    )
    barang_ids = fields.One2many(
        'pet_clinic.visitation_barang', 'visitation_id',
        string='Barang/Obat Pulang',
    )

    # Note
    note = fields.Text(string='Note')

    # Computed totals
    service_subtotal = fields.Float(
        string='Services Subtotal',
        compute='_compute_totals',
        store=True,
    )
    item_subtotal = fields.Float(
        string='Items Subtotal',
        compute='_compute_totals',
        store=True,
    )
    barang_subtotal = fields.Float(
        string='Barang/Obat Pulang Subtotal',
        compute='_compute_totals',
        store=True,
    )
    total_amount = fields.Float(
        string='Total',
        compute='_compute_totals',
        store=True,
    )

    # Smart button counts
    service_count = fields.Integer(
        compute='_compute_service_count', store=True,
    )
    item_count = fields.Integer(
        compute='_compute_item_count', store=True,
    )
    sale_order_count = fields.Integer(
        compute='_compute_sale_order_count',
    )

    @api.depends('pet_id.date_of_birth')
    def _compute_umur(self):
        today = fields.Date.today()
        for rec in self:
            if rec.pet_id and rec.pet_id.date_of_birth:
                rd = relativedelta(today, rec.pet_id.date_of_birth)
                rec.umur = f"{rd.years} Tahun, {rd.months} Bulan"
            else:
                rec.umur = ''

    @api.depends(
        'service_ids.total_price',
        'item_ids.total_price',
        'barang_ids.total_price',
    )
    def _compute_totals(self):
        for rec in self:
            rec.service_subtotal = sum(
                rec.service_ids.mapped('total_price')
            )
            rec.item_subtotal = sum(rec.item_ids.mapped('total_price'))
            rec.barang_subtotal = sum(
                rec.barang_ids.mapped('total_price')
            )
            rec.total_amount = (
                rec.service_subtotal
                + rec.item_subtotal
                + rec.barang_subtotal
            )

    @api.depends('service_ids')
    def _compute_service_count(self):
        for rec in self:
            rec.service_count = len(rec.service_ids)

    @api.depends('item_ids')
    def _compute_item_count(self):
        for rec in self:
            rec.item_count = len(rec.item_ids)

    def _compute_sale_order_count(self):
        for rec in self:
            rec.sale_order_count = 1 if rec.id_so else 0

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
                    'pet_clinic.visitation'
                ) or 'New'
        return super().create(vals_list)

    def action_check(self):
        self.write({'state': 'in_process'})

    def action_done(self):
        self.write({
            'state': 'done',
            'date_end': fields.Datetime.now(),
        })
        # Create medical history line
        for rec in self:
            if rec.pet_id:
                self.env['pet_clinic.medical_history_line'].create({
                    'pet_id': rec.pet_id.id,
                    'date_start': rec.date_start,
                    'doctor_id': rec.doctor_id.id if rec.doctor_id else False,
                    'anamnesa': rec.anamnesa,
                    'diagnosis': rec.diagnosis,
                    'therapy': rec.therapy,
                    'temperature': rec.temperature,
                    'weight': rec.weight,
                    'bcs': rec.bcs,
                    'action': rec.action_field,
                })

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_create_sale_order(self):
        """Buat Sale Order dari data visitation."""
        self.ensure_one()
        order_lines = []

        # Add services
        for service in self.service_ids:
            if service.service_type:
                order_lines.append((0, 0, {
                    'product_id': service.service_type.id,
                    'name': service.service_type.name,
                    'product_uom_qty': service.amount or 1,
                    'price_unit': service.total_price / service.amount if service.amount else service.total_price,
                }))

        # Add items
        for item in self.item_ids:
            if item.product_id:
                order_lines.append((0, 0, {
                    'product_id': item.product_id.id,
                    'name': item.product_id.name,
                    'product_uom_qty': item.quantity,
                    'price_unit': item.price,
                }))

        partner = self.env['res.partner'].search(
            [('name', '=', self.owner_id.name)], limit=1,
        )
        if not partner:
            partner = self.env['res.partner'].create({
                'name': self.owner_id.name,
                'phone': self.owner_id.phone,
                'email': self.owner_id.email,
            })

        sale_order = self.env['sale.order'].create({
            'partner_id': partner.id,
            'order_line': order_lines,
            'origin': self.name,
        })
        self.id_so = sale_order.id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': sale_order.id,
        }

    def action_view_sale_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.id_so.id,
        }

    def action_view_services(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Services',
            'res_model': 'pet_clinic.service',
            'view_mode': 'list,form',
            'domain': [('visitation_id', '=', self.id)],
        }

    def action_view_items(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Items',
            'res_model': 'pet_clinic.visitation_item',
            'view_mode': 'list,form',
            'domain': [('visitation_id', '=', self.id)],
        }


class PetClinicVisitationItem(models.Model):
    _name = 'pet_clinic.visitation_item'
    _description = 'Visitation Item'

    visitation_id = fields.Many2one(
        'pet_clinic.visitation', string='Visitation', ondelete='cascade',
    )
    product_id = fields.Many2one(
        'product.product', string='Item',
    )
    simple_name = fields.Char(string='Simple Name')
    category_id = fields.Many2one(
        'product.category', string='Category',
        related='product_id.categ_id', store=True,
    )
    quantity = fields.Float(string='Quantity', default=1)
    uom_id = fields.Many2one(
        'uom.uom', string='Unit of Measure',
        related='product_id.uom_id', store=True,
    )
    price = fields.Float(string='Price')
    total_price = fields.Float(
        string='Total Price',
        compute='_compute_total_price',
        store=True,
    )

    @api.depends('quantity', 'price')
    def _compute_total_price(self):
        for rec in self:
            rec.total_price = rec.quantity * rec.price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.simple_name = self.product_id.name
            self.price = self.product_id.list_price


class PetClinicVisitationBarang(models.Model):
    _name = 'pet_clinic.visitation_barang'
    _description = 'Barang / Obat Pulang'

    visitation_id = fields.Many2one(
        'pet_clinic.visitation', string='Visitation', ondelete='cascade',
    )
    product_id = fields.Many2one(
        'product.product', string='Item',
    )
    name = fields.Char(string='Name')
    quantity = fields.Float(string='Quantity', default=1)
    uom_id = fields.Many2one(
        'uom.uom', string='Unit of Measure',
        related='product_id.uom_id', store=True,
    )
    price = fields.Float(string='Price')
    total_price = fields.Float(
        string='Total Price',
        compute='_compute_total_price',
        store=True,
    )

    @api.depends('quantity', 'price')
    def _compute_total_price(self):
        for rec in self:
            rec.total_price = rec.quantity * rec.price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.price = self.product_id.list_price
