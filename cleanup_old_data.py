# -*- coding: utf-8 -*-
"""Hapus semua data lama yang kosong/tidak lengkap."""
import sys, os

sys.path.append(os.path.abspath('odoo'))
import odoo
odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

    # Daftar client baru yang TIDAK boleh dihapus
    keep_clients = [
        'Sinta Dewi', 'Doni Pratama', 'Reza Mahendra', 'Rahmat Hidayat',
        'Putri Ayu', 'Ahmad Fauzi', 'Nadia Safira', 'Bayu Setiawan',
    ]

    # 1. Hapus visitation kosong/lama (tanpa owner atau pet)
    bad_vis = env['pet_clinic.visitation'].with_context(active_test=False).search([
        '|', ('owner_id', '=', False), ('pet_id', '=', False)
    ])
    if bad_vis:
        print(f"Menghapus {len(bad_vis)} visitation kosong...")
        for v in bad_vis:
            print(f"  - {v.name}")
        bad_vis.unlink()

    # 2. Hapus appointment kosong/lama
    bad_appt = env['pet_clinic.appointment'].with_context(active_test=False).search([
        '|', ('owner_id', '=', False), ('pet_id', '=', False)
    ])
    if bad_appt:
        print(f"Menghapus {len(bad_appt)} appointment kosong...")
        bad_appt.unlink()

    # 3. Hapus client lama yang BUKAN milik daftar baru
    old_clients = env['pet_clinic.client'].with_context(active_test=False).search([
        ('name', 'not in', keep_clients)
    ])
    if old_clients:
        # Hapus pet terkait dulu
        for cl in old_clients:
            pets = env['pet_clinic.pet'].with_context(active_test=False).search([('owner_id', '=', cl.id)])
            if pets:
                # Hapus visitation, appointment, service, medical history terkait
                env['pet_clinic.visitation'].with_context(active_test=False).search([('pet_id', 'in', pets.ids)]).unlink()
                env['pet_clinic.appointment'].with_context(active_test=False).search([('pet_id', 'in', pets.ids)]).unlink()
                env['pet_clinic.service'].with_context(active_test=False).search([('pet_id', 'in', pets.ids)]).unlink()
                env['pet_clinic.medical_history_line'].search([('pet_id', 'in', pets.ids)]).unlink()
                pets.unlink()
        print(f"Menghapus {len(old_clients)} client lama:")
        for cl in old_clients:
            print(f"  - {cl.id_client} {cl.name}")
        old_clients.unlink()

    # 4. Hapus Pet Type "Dog" jika ada (duplikat bahasa Inggris)
    for old_type in ['Dog', 'Cat', 'Bird', 'Fish', 'Rabbit']:
        t = env['pet_clinic.pet_type'].search([('name', '=', old_type)])
        if t:
            # Pindahkan breed yang terhubung
            t.unlink()
            print(f"  Hapus Pet Type duplikat: {old_type}")

    # 5. Hapus breed yang type_id-nya kosong
    orphan_breeds = env['pet_clinic.pet_breed'].search([('type_id', '=', False)])
    if orphan_breeds:
        print(f"Menghapus {len(orphan_breeds)} breed tanpa type:")
        for ob in orphan_breeds:
            print(f"  - {ob.name}")
        orphan_breeds.unlink()

    env.cr.commit()
    print("\nPembersihan selesai! Data lama sudah dihapus.")
