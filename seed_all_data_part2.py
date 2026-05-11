# -*- coding: utf-8 -*-
"""Seed ALL data Part 2 - Appointment & Visitation."""
import sys, os
from datetime import date, datetime, timedelta

sys.path.append(os.path.abspath('odoo'))
import odoo
odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

    def find(model, name):
        return env[model].search([('name', '=', name)], limit=1)

    def find_pet(name):
        return env['pet_clinic.pet'].search([('name', '=', name)], limit=1)

    def find_product(name):
        return env['product.product'].search([('name', '=', name)], limit=1)

    # Get references
    lok1 = find('pet_clinic.lokasi', 'Cabang Utama Sudirman')
    lok2 = find('pet_clinic.lokasi', 'Cabang Selatan')
    lok3 = find('pet_clinic.lokasi', 'Cabang Bandung')
    doc1 = find('pet_clinic.doctor', 'Drh. Budi Santoso')
    doc2 = find('pet_clinic.doctor', 'Drh. Ani Wijaya')
    doc3 = find('pet_clinic.doctor', 'Drh. Siska Amelia')
    doc4 = find('pet_clinic.doctor', 'Drh. Rendi Pratama')
    doc5 = find('pet_clinic.doctor', 'Drh. Maya Putri')
    par1 = find('pet_clinic.paramedis', 'Rina Marlina')
    par2 = find('pet_clinic.paramedis', 'Joko Anwar')
    par3 = find('pet_clinic.paramedis', 'Dewi Lestari')
    rm1 = find('pet_clinic.room', 'Ruang Periksa 1')
    rm2 = find('pet_clinic.room', 'Ruang Periksa 2')
    rm3 = find('pet_clinic.room', 'Ruang Operasi Utama')
    rm6 = find('pet_clinic.room', 'Grooming Room')

    # Reset sequences
    for code in ['pet_clinic.appointment', 'pet_clinic.visitation', 'pet_clinic.service']:
        seq = env['ir.sequence'].search([('code', '=', code)], limit=1)
        if seq:
            seq.write({'number_next_actual': 1})

    # =============================================
    # APPOINTMENTS
    # =============================================
    appt_data = [
        ('Sinta Dewi', 'Milo', lok1, doc1, rm1, datetime(2026,5,7,9,0), 'confirmed'),
        ('Doni Pratama', 'Buddy', lok1, doc2, rm2, datetime(2026,5,7,10,0), 'confirmed'),
        ('Reza Mahendra', 'Cleo', lok2, doc3, rm1, datetime(2026,5,8,9,0), 'draft'),
        ('Rahmat Hidayat', 'Bella', lok1, doc1, rm1, datetime(2026,5,8,14,0), 'draft'),
        ('Putri Ayu', 'Ciko', lok3, doc4, rm1, datetime(2026,5,9,10,0), 'draft'),
        ('Ahmad Fauzi', 'Molly', lok2, doc3, rm2, datetime(2026,5,9,11,0), 'draft'),
        ('Nadia Safira', 'Daisy', lok3, doc4, rm1, datetime(2026,5,10,9,0), 'draft'),
        ('Bayu Setiawan', 'Suki', lok1, doc5, rm2, datetime(2026,5,10,14,0), 'draft'),
    ]

    for oname, pname, lok, doc, rm, dt, state in appt_data:
        owner = find('pet_clinic.client', oname)
        pet = find_pet(pname)
        if owner and pet:
            appt = env['pet_clinic.appointment'].create({
                'owner_id': owner.id,
                'pet_id': pet.id,
                'location_id': lok.id,
                'doctor_id': doc.id,
                'room_id': rm.id,
                'date': dt,
                'state': state,
            })
            print(f"  [APPT] {appt.name} - {pname} ({oname}) @ {lok.name} - {state}")

    # =============================================
    # VISITATIONS (Kunjungan)
    # =============================================
    visit_data = [
        {
            'owner': 'Sinta Dewi', 'pet': 'Milo', 'lok': lok1, 'doc': doc1, 'par': par1, 'rm': rm1,
            'penanganan': 'rawat_jalan', 'date': datetime(2026,5,5,9,0),
            'anamnesa': 'Kucing tidak mau makan sejak 2 hari lalu, lesu.',
            'keluhan': 'Nafsu makan turun, muntah sesekali.',
            'weight': 4.2, 'temp': 39.1, 'bcs': 4,
            'diagnosis': 'Gangguan pencernaan ringan.', 'therapy': 'Obat anti-emesis + probiotik.',
            'state': 'done',
        },
        {
            'owner': 'Doni Pratama', 'pet': 'Buddy', 'lok': lok1, 'doc': doc2, 'par': par2, 'rm': rm2,
            'penanganan': 'rawat_jalan', 'date': datetime(2026,5,5,10,30),
            'anamnesa': 'Anjing sering menggaruk telinga kiri.',
            'keluhan': 'Garuk-garuk telinga, keluar cairan berwarna cokelat.',
            'weight': 28.5, 'temp': 38.7, 'bcs': 6,
            'diagnosis': 'Otitis Externa.', 'therapy': 'Tetes telinga antibiotik 2x sehari.',
            'state': 'done',
        },
        {
            'owner': 'Reza Mahendra', 'pet': 'Rocky', 'lok': lok2, 'doc': doc3, 'par': par3, 'rm': rm1,
            'penanganan': 'rawat_jalan', 'date': datetime(2026,5,5,14,0),
            'anamnesa': 'Vaksinasi rutin tahunan.',
            'keluhan': 'Vaksinasi ulang (booster) rabies dan distemper.',
            'weight': 22.0, 'temp': 38.5, 'bcs': 5,
            'diagnosis': 'Sehat, siap vaksinasi.', 'therapy': 'Vaksinasi Rabies + Distemper.',
            'state': 'done',
        },
        {
            'owner': 'Rahmat Hidayat', 'pet': 'Simba', 'lok': lok1, 'doc': doc5, 'par': par1, 'rm': rm1,
            'penanganan': 'rawat_jalan', 'date': datetime(2026,5,6,9,0),
            'anamnesa': 'Kucing sering menggaruk badan, bulu rontok di area perut.',
            'keluhan': 'Gatal, bulu rontok, kulit kemerahan.',
            'weight': 6.8, 'temp': 38.9, 'bcs': 5,
            'diagnosis': 'Dermatitis Alergi.', 'therapy': 'Salep anti-jamur + antihistamin oral.',
            'state': 'in_process',
        },
        {
            'owner': 'Ahmad Fauzi', 'pet': 'Coco', 'lok': lok2, 'doc': doc1, 'par': par3, 'rm': rm2,
            'penanganan': 'rawat_jalan', 'date': datetime(2026,5,6,11,0),
            'anamnesa': 'Grooming rutin + pemeriksaan gigi.',
            'keluhan': 'Bulu kusut, perlu grooming dan cek kesehatan gigi.',
            'weight': 5.5, 'temp': 38.4, 'bcs': 6,
            'diagnosis': 'Karang gigi ringan.', 'therapy': 'Scaling gigi + grooming lengkap.',
            'state': 'in_process',
        },
        {
            'owner': 'Nadia Safira', 'pet': 'Hachi', 'lok': lok3, 'doc': doc4, 'par': par3, 'rm': rm1,
            'penanganan': 'rawat_jalan', 'date': datetime(2026,5,6,14,0),
            'anamnesa': 'Anjing pincang pada kaki depan kanan setelah bermain.',
            'keluhan': 'Pincang, enggan berjalan, kesakitan saat kaki dipegang.',
            'weight': 10.2, 'temp': 38.6, 'bcs': 5,
            'diagnosis': 'Sprain (keseleo) ringan.', 'therapy': 'Anti-inflamasi + istirahat 1 minggu.',
            'state': 'draft',
        },
        {
            'owner': 'Bayu Setiawan', 'pet': 'Brownie', 'lok': lok1, 'doc': doc2, 'par': par2, 'rm': rm2,
            'penanganan': 'rawat_jalan', 'date': datetime(2026,5,7,9,0),
            'anamnesa': 'Hamster kurang aktif, mata berair.',
            'keluhan': 'Kurang aktif, mata berair, hidung basah.',
            'weight': 0.12, 'temp': 37.5, 'bcs': 4,
            'diagnosis': 'Flu ringan / respiratory infection.', 'therapy': 'Antibiotik oral dosis kecil.',
            'state': 'draft',
        },
        {
            'owner': 'Putri Ayu', 'pet': 'Nemo', 'lok': lok3, 'doc': doc4, 'par': par3, 'rm': rm1,
            'penanganan': 'rawat_jalan', 'date': datetime(2026,5,7,10,0),
            'anamnesa': 'Ikan cupang tidak aktif, sirip robek.',
            'keluhan': 'Sirip compang-camping, warna pudar.',
            'weight': 0.01, 'temp': 0, 'bcs': 0,
            'diagnosis': 'Fin rot (infeksi sirip).', 'therapy': 'Methylene blue + garam ikan.',
            'state': 'draft',
        },
    ]

    for v in visit_data:
        owner = find('pet_clinic.client', v['owner'])
        pet = find_pet(v['pet'])
        if not (owner and pet):
            continue
        vis = env['pet_clinic.visitation'].create({
            'owner_id': owner.id,
            'pet_id': pet.id,
            'lokasi_pemeriksaan': v['lok'].id,
            'doctor_id': v['doc'].id,
            'paramedis_id': v['par'].id,
            'room_id': v['rm'].id,
            'penanganan': v['penanganan'],
            'date_start': v['date'],
            'date_end': v['date'] + timedelta(hours=1) if v['state'] == 'done' else False,
            'anamnesa': v['anamnesa'],
            'keluhan_tujuan': v['keluhan'],
            'weight': v['weight'],
            'temperature': v['temp'],
            'bcs': v['bcs'],
            'diagnosis': v['diagnosis'],
            'therapy': v['therapy'],
            'state': v['state'],
            'nomor_rekam_medis': f"RM-{pet.id_pet}",
            'status_pasien': 'Terdaftar',
        })
        print(f"  [VISIT] {vis.name} - {v['pet']} ({v['owner']}) - {v['state']}")

    env.cr.commit()
    print("\n=== PHASE 2 DONE: Appointments + Visitations ===")
    print("SEMUA DATA TELAH TERISI LENGKAP!")
