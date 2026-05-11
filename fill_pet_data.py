# -*- coding: utf-8 -*-
"""
Fill Missing Pet Data Script
=============================
Melengkapi data pasien (pet) yang masih kosong:
Owner, Pet Type, Breed, Gender, Date of Birth
"""
import sys
import os
from datetime import date
from dateutil.relativedelta import relativedelta

sys.path.append(os.path.abspath('odoo'))

import odoo

odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

    # ── Helper: cari atau buat record ──
    def find(model, name):
        rec = env[model].search([('name', '=', name)], limit=1)
        return rec.id if rec else False

    def find_breed(name, type_name):
        type_id = find('pet_clinic.pet_type', type_name)
        rec = env['pet_clinic.pet_breed'].search(
            [('name', '=', name), ('type_id', '=', type_id)], limit=1
        )
        if not rec:
            rec = env['pet_clinic.pet_breed'].search([('name', '=', name)], limit=1)
        return rec.id if rec else False

    # ── Data lengkap per nama pet ──
    # Format: 'NamaPet': (owner, pet_type, breed, gender, umur_tahun, umur_bulan)
    pet_fill_data = {
        'Coco':   ('Sinta',  'Anjing',  'Poodle',              'female', 3, 2),
        'Miko':   ('Doni',   'Kucing',  'Domestik / Kampung',  'male',   2, 5),
        'Zeus':   ('Reza',   'Anjing',  'German Shepherd',     'male',   4, 0),
        'Snowy':  ('Sinta',  'Kucing',  'Persia',              'female', 1, 8),
        'Luna':   ('Doni',   'Kucing',  'Anggora',             'female', 2, 3),
        'Rocky':  ('Rahmat', 'Anjing',  'Bulldog',             'male',   3, 6),
        'Bella':  ('Sinta',  'Anjing',  'Golden Retriever',    'female', 5, 1),
        'Molly':  ('Reza',   'Kelinci', 'Holland Lop',         'female', 1, 4),
        'Max':    ('Doni',   'Anjing',  'Labrador',            'male',   4, 7),
        'Ciko':   ('Rahmat', 'Burung',  'Cockatiel',           'male',   1, 0),
        'Kiko':   ('Sinta',  'Burung',  'Lovebird',            'male',   0, 9),
        'Choco':  ('Reza',   'Kucing',  'British Shorthair',   'male',   2, 0),
        'testing Dog': ('Sinta', 'Anjing', 'Chihuahua',        'female', 1, 3),
        'wahyu':  ('Doni',   'Ikan',    'Cupang',              'male',   0, 6),
    }

    today = date.today()
    updated_count = 0

    all_pets = env['pet_clinic.pet'].search([])
    print(f"Total pet ditemukan: {len(all_pets)}\n")

    for pet in all_pets:
        fill = pet_fill_data.get(pet.name)
        if not fill:
            # Jika tidak ada di daftar, skip
            continue

        owner_name, type_name, breed_name, gender, age_y, age_m = fill
        vals = {}

        # Owner
        if not pet.owner_id:
            owner_id = find('pet_clinic.client', owner_name)
            if owner_id:
                vals['owner_id'] = owner_id

        # Pet Type
        if not pet.type_id:
            type_id = find('pet_clinic.pet_type', type_name)
            if type_id:
                vals['type_id'] = type_id

        # Breed
        if not pet.breed_id:
            breed_id = find_breed(breed_name, type_name)
            if breed_id:
                vals['breed_id'] = breed_id

        # Gender
        if not pet.gender:
            vals['gender'] = gender

        # Date of Birth (hitung mundur dari usia)
        if not pet.date_of_birth:
            dob = today - relativedelta(years=age_y, months=age_m)
            vals['date_of_birth'] = dob

        if vals:
            pet.write(vals)
            updated_count += 1
            fields_filled = ', '.join(vals.keys())
            print(f"  [UPDATED] {pet.id_pet} - {pet.name} -> {fields_filled}")
        else:
            print(f"  [SKIP]    {pet.id_pet} - {pet.name} (sudah lengkap)")

    # ── Juga perbaiki Pet Type "Dog" -> "Anjing" jika ada ──
    dog_type = env['pet_clinic.pet_type'].search([('name', '=', 'Dog')], limit=1)
    anjing_type = env['pet_clinic.pet_type'].search([('name', '=', 'Anjing')], limit=1)
    if dog_type and anjing_type:
        pets_with_dog = env['pet_clinic.pet'].search([('type_id', '=', dog_type.id)])
        for p in pets_with_dog:
            p.write({'type_id': anjing_type.id})
            # Juga perbaiki breed "Domestic Dog" jika ada
            if p.breed_id and 'Domestic' in p.breed_id.name:
                kampung = env['pet_clinic.pet_breed'].search(
                    [('name', '=', 'Domestik / Kampung'), ('type_id', '=', anjing_type.id)], limit=1
                )
                if kampung:
                    p.write({'breed_id': kampung.id})
            print(f"  [FIX]     {p.id_pet} - {p.name}: Dog -> Anjing")
            updated_count += 1

    env.cr.commit()
    print(f"\nSelesai! Total diupdate: {updated_count}")
