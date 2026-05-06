import sys
import os

sys.path.append(os.path.abspath('odoo'))

import odoo

odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # 1. PET TYPES
    pet_types = ['Kucing', 'Anjing', 'Kelinci', 'Burung', 'Hamster', 'Reptil']
    type_records = {}
    for pt in pet_types:
        existing = env['pet_clinic.pet_type'].search([('name', '=', pt)], limit=1)
        if not existing:
            existing = env['pet_clinic.pet_type'].create({'name': pt})
        type_records[pt] = existing.id

    # 2. PET BREEDS
    pet_breeds = [
        {'name': 'Persia', 'type_id': type_records['Kucing']},
        {'name': 'Anggora', 'type_id': type_records['Kucing']},
        {'name': 'Maine Coon', 'type_id': type_records['Kucing']},
        {'name': 'Domestik / Kampung', 'type_id': type_records['Kucing']},
        {'name': 'Golden Retriever', 'type_id': type_records['Anjing']},
        {'name': 'Bulldog', 'type_id': type_records['Anjing']},
        {'name': 'Chihuahua', 'type_id': type_records['Anjing']},
        {'name': 'Poodle', 'type_id': type_records['Anjing']},
        {'name': 'Angora (Kelinci)', 'type_id': type_records['Kelinci']},
        {'name': 'Lovebird', 'type_id': type_records['Burung']},
    ]
    for pb in pet_breeds:
        if not env['pet_clinic.pet_breed'].search([('name', '=', pb['name'])]):
            env['pet_clinic.pet_breed'].create(pb)

    # 3. DOCTORS
    doctors = [
        {'name': 'Drh. Budi Santoso', 'phone': '081234567890', 'specialization': 'Dokter Umum & Bedah'},
        {'name': 'Drh. Ani Wijaya', 'phone': '081987654321', 'specialization': 'Penyakit Dalam'},
        {'name': 'Drh. Siska Amelia', 'phone': '081333444555', 'specialization': 'Dokter Gigi Hewan'}
    ]
    for doc in doctors:
        if not env['pet_clinic.doctor'].search([('name', '=', doc['name'])]):
            env['pet_clinic.doctor'].create(doc)

    # 4. PARAMEDIS
    paramedis = [
        {'name': 'Rina Marlina', 'phone': '085711223344'},
        {'name': 'Joko Anwar', 'phone': '085799887766'}
    ]
    for par in paramedis:
        if not env['pet_clinic.paramedis'].search([('name', '=', par['name'])]):
            env['pet_clinic.paramedis'].create(par)

    # 5. ROOMS (Ruangan)
    rooms = [
        {'name': 'Ruang Periksa 1', 'no_ruangan': 'R-01'},
        {'name': 'Ruang Periksa 2', 'no_ruangan': 'R-02'},
        {'name': 'Ruang Operasi Utama', 'no_ruangan': 'OP-01'},
        {'name': 'Ruang Rawat Inap Kucing', 'no_ruangan': 'RI-K'},
        {'name': 'Ruang Rawat Inap Anjing', 'no_ruangan': 'RI-A'},
    ]
    for room in rooms:
        if not env['pet_clinic.room'].search([('name', '=', room['name'])]):
            env['pet_clinic.room'].create(room)

    # 6. LOKASI
    lokasi = [
        {'name': 'Cabang Utama Sudirman', 'address': 'Jl. Jendral Sudirman No. 123, Jakarta'},
        {'name': 'Cabang Selatan', 'address': 'Jl. Gatot Subroto No. 45, Jakarta Selatan'}
    ]
    for lok in lokasi:
        if not env['pet_clinic.lokasi'].search([('name', '=', lok['name'])]):
            env['pet_clinic.lokasi'].create(lok)

    # 7. DIAGNOSA UMUM
    diagnosa = [
        {'name': 'Scabies', 'description': 'Infeksi parasit tungau pada kulit.'},
        {'name': 'Feline Panleukopenia (FPV)', 'description': 'Virus mematikan pada kucing yang menyerang sistem pencernaan dan kekebalan.'},
        {'name': 'Rabies', 'description': 'Infeksi virus mematikan pada sistem saraf.'},
        {'name': 'Diare / Gangguan Pencernaan', 'description': 'Gangguan pencernaan akibat makanan atau bakteri.'},
        {'name': 'Flu Kucing (Feline Calicivirus)', 'description': 'Infeksi saluran pernapasan pada kucing.'},
    ]
    for diag in diagnosa:
        if not env['pet_clinic.diagnosa'].search([('name', '=', diag['name'])]):
            env['pet_clinic.diagnosa'].create(diag)

    # 8. DOSIS
    dosis = [
        {'name': '1x Sehari', 'description': 'Diminum 1 kali sehari setelah makan', 'quantity': 1},
        {'name': '2x Sehari', 'description': 'Diminum pagi dan malam setelah makan', 'quantity': 2},
        {'name': '3x Sehari', 'description': 'Diminum pagi, siang, dan malam', 'quantity': 3},
        {'name': 'Oles secukupnya', 'description': 'Dioleskan pada area yang luka/sakit', 'quantity': 1},
    ]
    for dos in dosis:
        if not env['pet_clinic.dosis'].search([('name', '=', dos['name'])]):
            env['pet_clinic.dosis'].create(dos)

    env.cr.commit()
    print("Berhasil memasukkan seluruh data master (Pet Type, Breed, Doctor, Paramedis, Room, Lokasi, Diagnosa, Dosis)!")
