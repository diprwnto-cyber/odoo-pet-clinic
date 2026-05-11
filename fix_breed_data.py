# -*- coding: utf-8 -*-
"""
Fix Breed Data Script
=====================
Memperbaiki data breed yang ada di database agar setiap breed
terhubung dengan Pet Type yang benar, dan menambahkan breed baru
yang lebih lengkap & realistis per jenis hewan.
"""
import sys
import os

sys.path.append(os.path.abspath('odoo'))

import odoo

odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

    # ── 1. Pastikan semua Pet Type ada ──
    pet_types = ['Kucing', 'Anjing', 'Kelinci', 'Burung', 'Hamster', 'Reptil', 'Ikan']
    type_map = {}
    for pt in pet_types:
        rec = env['pet_clinic.pet_type'].search([('name', '=', pt)], limit=1)
        if not rec:
            rec = env['pet_clinic.pet_type'].create({'name': pt})
        type_map[pt] = rec.id

    # ── 2. Data breed lengkap yang benar per jenis hewan ──
    breed_data = {
        'Kucing': [
            'Persia', 'Anggora', 'Maine Coon', 'British Shorthair',
            'Bengal', 'Siamese', 'Ragdoll', 'Scottish Fold',
            'Sphynx', 'Domestik / Kampung',
        ],
        'Anjing': [
            'Golden Retriever', 'Bulldog', 'Chihuahua', 'Poodle',
            'Shiba Inu', 'Siberian Husky', 'German Shepherd', 'Labrador',
            'Beagle', 'Pomeranian', 'Corgi', 'Dachshund',
            'Rottweiler', 'Doberman', 'Domestik / Kampung',
        ],
        'Kelinci': [
            'Angora (Kelinci)', 'Holland Lop', 'Rex', 'Netherland Dwarf',
            'Flemish Giant', 'Mini Lop', 'Lionhead',
        ],
        'Burung': [
            'Lovebird', 'Cockatiel', 'Parkit / Budgerigar', 'Kenari',
            'Kakatua', 'Murai Batu', 'Perkutut', 'Beo',
        ],
        'Hamster': [
            'Syrian Hamster', 'Campbell Dwarf', 'Winter White',
            'Roborovski', 'Chinese Hamster',
        ],
        'Reptil': [
            'Ball Python', 'Leopard Gecko', 'Bearded Dragon',
            'Iguana Hijau', 'Corn Snake', 'Red-Eared Slider (Kura-kura)',
            'Sulcata Tortoise',
        ],
        'Ikan': [
            'Cupang', 'Koi', 'Arwana', 'Mas Koki',
            'Louhan', 'Discus', 'Neon Tetra', 'Oscar',
        ],
    }

    created = 0
    updated = 0

    for type_name, breeds in breed_data.items():
        type_id = type_map[type_name]
        for breed_name in breeds:
            existing = env['pet_clinic.pet_breed'].search(
                [('name', '=', breed_name)], limit=1
            )
            if existing:
                # Perbaiki type_id jika belum benar
                if existing.type_id.id != type_id:
                    existing.write({'type_id': type_id})
                    updated += 1
                    print(f"  [UPDATE] '{breed_name}' -> {type_name}")
            else:
                env['pet_clinic.pet_breed'].create({
                    'name': breed_name,
                    'type_id': type_id,
                })
                created += 1
                print(f"  [CREATE] '{breed_name}' -> {type_name}")

    # ── 3. Perbaiki breed lama yang type_id-nya kosong (orphan) ──
    orphan_breeds = env['pet_clinic.pet_breed'].search([('type_id', '=', False)])
    if orphan_breeds:
        print(f"\n⚠ Ditemukan {len(orphan_breeds)} breed tanpa Pet Type:")
        for ob in orphan_breeds:
            print(f"  - '{ob.name}' (ID: {ob.id}) -- TIDAK DIHAPUS, silakan assign manual di Odoo.")

    env.cr.commit()
    print(f"\n✅ Selesai! Created: {created}, Updated: {updated}")
    print("Silakan restart Odoo dan refresh browser untuk melihat hasilnya.")
