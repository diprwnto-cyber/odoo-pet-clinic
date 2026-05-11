# -*- coding: utf-8 -*-
"""Assign lokasi ke semua product service + tambah service baru jika perlu."""
import sys, os
sys.path.append(os.path.abspath('odoo'))
import odoo
odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

    # Ambil semua lokasi
    all_lokasi = env['pet_clinic.lokasi'].search([])
    lok_ids = all_lokasi.ids
    print(f"Lokasi: {[l.name for l in all_lokasi]}")

    lok_map = {l.name: l.id for l in all_lokasi}
    lok_sudirman = lok_map.get('Cabang Utama Sudirman', False)
    lok_selatan = lok_map.get('Cabang Selatan', False)
    lok_bandung = lok_map.get('Cabang Bandung', False)

    # Daftar service yang harus ada
    services = [
        ('Konsultasi Umum', 50000, lok_ids),
        ('Vaksinasi Rabies', 150000, lok_ids),
        ('Vaksinasi Distemper', 175000, lok_ids),
        ('Sterilisasi Jantan', 500000, [lok_sudirman, lok_selatan]),
        ('Sterilisasi Betina', 750000, [lok_sudirman, lok_selatan]),
        ('Operasi Minor', 400000, [lok_sudirman, lok_bandung]),
        ('Operasi Mayor', 1500000, [lok_sudirman]),
        ('Grooming Basic', 100000, lok_ids),
        ('Grooming Premium', 200000, [lok_sudirman, lok_bandung]),
        ('Scaling Gigi', 300000, [lok_sudirman, lok_selatan]),
        ('Rawat Inap (per hari)', 200000, [lok_sudirman, lok_selatan]),
        ('Rontgen / X-Ray', 250000, [lok_sudirman]),
        ('USG', 350000, [lok_sudirman, lok_bandung]),
        ('Cek Darah Lengkap', 200000, lok_ids),
        ('Cek Feses', 75000, lok_ids),
        ('Tetes Telinga', 50000, lok_ids),
        ('Suntik Antibiotik', 100000, lok_ids),
        ('Pemasangan Infus', 150000, [lok_sudirman, lok_selatan]),
    ]

    # Cari/buat category "Pet Clinic Services"
    categ = env['product.category'].search([('name', '=', 'Pet Clinic Services')], limit=1)
    if not categ:
        categ = env['product.category'].create({'name': 'Pet Clinic Services'})

    created = 0
    updated = 0
    for sname, price, loks in services:
        loks = [l for l in loks if l]  # filter False
        tmpl = env['product.template'].search([('name', '=', sname)], limit=1)
        if tmpl:
            tmpl.write({
                'type': 'service',
                'list_price': price,
                'categ_id': categ.id,
                'lokasi_ids': [(6, 0, loks)],
            })
            updated += 1
            print(f"  [UPDATE] {sname} -> Rp{price:,.0f}")
        else:
            tmpl = env['product.template'].create({
                'name': sname,
                'type': 'service',
                'list_price': price,
                'categ_id': categ.id,
                'lokasi_ids': [(6, 0, loks)],
            })
            created += 1
            print(f"  [CREATE] {sname} -> Rp{price:,.0f}")

    # Juga assign lokasi ke service lama yang belum punya
    old_services = env['product.template'].search([
        ('type', '=', 'service'), ('lokasi_ids', '=', False)
    ])
    for s in old_services:
        s.write({'lokasi_ids': [(6, 0, lok_ids)]})
        print(f"  [FIX] {s.name} -> semua cabang")

    env.cr.commit()
    print(f"\nSelesai! Created: {created}, Updated: {updated}")
