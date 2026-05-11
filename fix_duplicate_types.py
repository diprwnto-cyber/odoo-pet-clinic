# -*- coding: utf-8 -*-
"""Hapus Pet Type duplikat yang breed-nya kosong."""
import sys, os
sys.path.append(os.path.abspath('odoo'))
import odoo
odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

    all_types = env['pet_clinic.pet_type'].search([])
    print(f"Total Pet Type sebelum: {len(all_types)}")
    for t in all_types:
        breed_count = len(t.breed_ids)
        print(f"  ID={t.id} | {t.name} | Breeds: {breed_count}")

    # Cari duplikat: group by name
    type_names = {}
    for t in all_types:
        type_names.setdefault(t.name, []).append(t)

    deleted = 0
    for name, records in type_names.items():
        if len(records) > 1:
            # Ada duplikat, simpan yang punya breed terbanyak
            records.sort(key=lambda r: len(r.breed_ids), reverse=True)
            keep = records[0]
            to_delete = records[1:]
            for d in to_delete:
                # Pindahkan pet yang terhubung ke type yang benar
                pets = env['pet_clinic.pet'].search([('type_id', '=', d.id)])
                if pets:
                    pets.write({'type_id': keep.id})
                    print(f"  Pindahkan {len(pets)} pet dari '{d.name}' (ID={d.id}) -> (ID={keep.id})")
                # Pindahkan breed yatim jika ada
                for b in d.breed_ids:
                    b.write({'type_id': keep.id})
                print(f"  [HAPUS] '{d.name}' (ID={d.id}, breeds={len(d.breed_ids)})")
                d.unlink()
                deleted += 1

    # Hapus juga Pet Type bahasa Inggris yang masih tersisa
    eng_types = env['pet_clinic.pet_type'].search([('name', 'in', ['Dog', 'Cat', 'Bird', 'Fish', 'Rabbit'])])
    for et in eng_types:
        pets = env['pet_clinic.pet'].search([('type_id', '=', et.id)])
        if pets:
            # Cari padanan Indonesia
            mapping = {'Dog': 'Anjing', 'Cat': 'Kucing', 'Bird': 'Burung', 'Fish': 'Ikan', 'Rabbit': 'Kelinci'}
            indo = env['pet_clinic.pet_type'].search([('name', '=', mapping.get(et.name, ''))], limit=1)
            if indo:
                pets.write({'type_id': indo.id})
        print(f"  [HAPUS] '{et.name}' (ID={et.id})")
        et.unlink()
        deleted += 1

    remaining = env['pet_clinic.pet_type'].search([])
    print(f"\nTotal Pet Type sesudah: {len(remaining)}")
    for t in remaining:
        print(f"  {t.name} -> {len(t.breed_ids)} breeds")

    env.cr.commit()
    print(f"\nSelesai! Dihapus: {deleted}")
