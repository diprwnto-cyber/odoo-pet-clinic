# -*- coding: utf-8 -*-
"""Seed ALL data - lengkapi semua tabel sesuai struktur."""
import sys, os
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

sys.path.append(os.path.abspath('odoo'))
import odoo
odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

    def get_or_create(model, vals, search_field='name'):
        rec = env[model].search([(search_field, '=', vals[search_field])], limit=1)
        if not rec:
            rec = env[model].create(vals)
        else:
            rec.write(vals)
        return rec

    # =============================================
    # 1. LOKASI (Cabang)
    # =============================================
    lok1 = get_or_create('pet_clinic.lokasi', {'name': 'Cabang Utama Sudirman', 'address': 'Jl. Jendral Sudirman No. 123, Jakarta Pusat'})
    lok2 = get_or_create('pet_clinic.lokasi', {'name': 'Cabang Selatan', 'address': 'Jl. Gatot Subroto No. 45, Jakarta Selatan'})
    lok3 = get_or_create('pet_clinic.lokasi', {'name': 'Cabang Bandung', 'address': 'Jl. Asia Afrika No. 88, Bandung'})

    # =============================================
    # 2. PET TYPES
    # =============================================
    types = {}
    for t in ['Kucing','Anjing','Kelinci','Burung','Hamster','Reptil','Ikan']:
        types[t] = get_or_create('pet_clinic.pet_type', {'name': t})

    # =============================================
    # 3. PET BREEDS (sesuai type)
    # =============================================
    breed_map = {
        'Kucing': ['Persia','Anggora','Maine Coon','British Shorthair','Bengal','Siamese','Ragdoll','Scottish Fold','Sphynx','Domestik / Kampung'],
        'Anjing': ['Golden Retriever','Bulldog','Chihuahua','Poodle','Shiba Inu','Siberian Husky','German Shepherd','Labrador','Beagle','Pomeranian','Corgi','Dachshund','Rottweiler','Doberman'],
        'Kelinci': ['Angora (Kelinci)','Holland Lop','Rex','Netherland Dwarf','Flemish Giant','Mini Lop','Lionhead'],
        'Burung': ['Lovebird','Cockatiel','Parkit / Budgerigar','Kenari','Kakatua','Murai Batu','Perkutut','Beo'],
        'Hamster': ['Syrian Hamster','Campbell Dwarf','Winter White','Roborovski','Chinese Hamster'],
        'Reptil': ['Ball Python','Leopard Gecko','Bearded Dragon','Iguana Hijau','Corn Snake','Red-Eared Slider (Kura-kura)','Sulcata Tortoise'],
        'Ikan': ['Cupang','Koi','Arwana','Mas Koki','Louhan','Discus','Neon Tetra','Oscar'],
    }
    breeds = {}
    for type_name, breed_list in breed_map.items():
        for b in breed_list:
            breeds[b] = get_or_create('pet_clinic.pet_breed', {'name': b, 'type_id': types[type_name].id})

    # =============================================
    # 4. DOCTORS
    # =============================================
    doc1 = get_or_create('pet_clinic.doctor', {'name': 'Drh. Budi Santoso', 'phone': '081234567890', 'specialization': 'Dokter Umum & Bedah', 'lokasi_ids': [(6,0,[lok1.id, lok2.id])]})
    doc2 = get_or_create('pet_clinic.doctor', {'name': 'Drh. Ani Wijaya', 'phone': '081987654321', 'specialization': 'Penyakit Dalam', 'lokasi_ids': [(6,0,[lok1.id])]})
    doc3 = get_or_create('pet_clinic.doctor', {'name': 'Drh. Siska Amelia', 'phone': '081333444555', 'specialization': 'Dokter Gigi Hewan', 'lokasi_ids': [(6,0,[lok2.id, lok3.id])]})
    doc4 = get_or_create('pet_clinic.doctor', {'name': 'Drh. Rendi Pratama', 'phone': '081222333444', 'specialization': 'Bedah Orthopedi', 'lokasi_ids': [(6,0,[lok3.id])]})
    doc5 = get_or_create('pet_clinic.doctor', {'name': 'Drh. Maya Putri', 'phone': '081555666777', 'specialization': 'Dermatologi Hewan', 'lokasi_ids': [(6,0,[lok1.id, lok3.id])]})

    # =============================================
    # 5. PARAMEDIS
    # =============================================
    par1 = get_or_create('pet_clinic.paramedis', {'name': 'Rina Marlina', 'phone': '085711223344', 'lokasi_ids': [(6,0,[lok1.id, lok2.id])]})
    par2 = get_or_create('pet_clinic.paramedis', {'name': 'Joko Anwar', 'phone': '085799887766', 'lokasi_ids': [(6,0,[lok1.id])]})
    par3 = get_or_create('pet_clinic.paramedis', {'name': 'Dewi Lestari', 'phone': '085711445566', 'lokasi_ids': [(6,0,[lok2.id, lok3.id])]})
    par4 = get_or_create('pet_clinic.paramedis', {'name': 'Andi Firmansyah', 'phone': '085722334455', 'lokasi_ids': [(6,0,[lok3.id])]})

    # =============================================
    # 6. GROOMERS
    # =============================================
    gr1 = get_or_create('pet_clinic.groomer', {'name': 'Siti Nurhaliza', 'phone': '087811112222', 'lokasi_ids': [(6,0,[lok1.id, lok2.id])]})
    gr2 = get_or_create('pet_clinic.groomer', {'name': 'Bambang Grooming', 'phone': '087833334444', 'lokasi_ids': [(6,0,[lok2.id, lok3.id])]})
    gr3 = get_or_create('pet_clinic.groomer', {'name': 'Wulan Dari', 'phone': '087855556666', 'lokasi_ids': [(6,0,[lok1.id, lok3.id])]})

    # =============================================
    # 7. ROOMS
    # =============================================
    rm1 = get_or_create('pet_clinic.room', {'name': 'Ruang Periksa 1', 'no_ruangan': 'R-01', 'lokasi_ids': [(6,0,[lok1.id, lok2.id, lok3.id])]})
    rm2 = get_or_create('pet_clinic.room', {'name': 'Ruang Periksa 2', 'no_ruangan': 'R-02', 'lokasi_ids': [(6,0,[lok1.id, lok2.id])]})
    rm3 = get_or_create('pet_clinic.room', {'name': 'Ruang Operasi Utama', 'no_ruangan': 'OP-01', 'lokasi_ids': [(6,0,[lok1.id])]})
    rm4 = get_or_create('pet_clinic.room', {'name': 'Ruang Rawat Inap Kucing', 'no_ruangan': 'RI-K', 'lokasi_ids': [(6,0,[lok1.id, lok3.id])]})
    rm5 = get_or_create('pet_clinic.room', {'name': 'Ruang Rawat Inap Anjing', 'no_ruangan': 'RI-A', 'lokasi_ids': [(6,0,[lok1.id, lok2.id])]})
    rm6 = get_or_create('pet_clinic.room', {'name': 'Grooming Room', 'no_ruangan': 'GR-01', 'lokasi_ids': [(6,0,[lok1.id, lok2.id, lok3.id])]})
    rm7 = get_or_create('pet_clinic.room', {'name': 'Ruang Operasi 2', 'no_ruangan': 'OP-02', 'lokasi_ids': [(6,0,[lok2.id, lok3.id])]})

    # =============================================
    # 8. PROVINSI, KAB/KOTA, KECAMATAN
    # =============================================
    prov1 = get_or_create('pet_clinic.provinsi', {'name': 'DKI Jakarta'})
    prov2 = get_or_create('pet_clinic.provinsi', {'name': 'Jawa Barat'})
    prov3 = get_or_create('pet_clinic.provinsi', {'name': 'Jawa Timur'})

    kab1 = get_or_create('pet_clinic.kab_kota', {'name': 'Jakarta Pusat'})
    kab2 = get_or_create('pet_clinic.kab_kota', {'name': 'Jakarta Selatan'})
    kab3 = get_or_create('pet_clinic.kab_kota', {'name': 'Kota Bandung'})
    kab4 = get_or_create('pet_clinic.kab_kota', {'name': 'Kota Pasuruan'})

    for kec_name, kab in [('Menteng', kab1), ('Tanah Abang', kab1), ('Kebayoran Baru', kab2), ('Tebet', kab2), ('Coblong', kab3), ('Cicendo', kab3), ('Bugul Kidul', kab4), ('Purworejo', kab4)]:
        get_or_create('pet_clinic.kecamatan', {'name': kec_name, 'kab_kota_id': kab.id})

    # =============================================
    # 9. DIAGNOSA
    # =============================================
    diag_data = [
        ('Scabies', 'Infeksi parasit tungau pada kulit.'),
        ('Feline Panleukopenia (FPV)', 'Virus mematikan pada kucing yang menyerang sistem pencernaan dan kekebalan.'),
        ('Rabies', 'Infeksi virus mematikan pada sistem saraf.'),
        ('Diare / Gangguan Pencernaan', 'Gangguan pencernaan akibat makanan atau bakteri.'),
        ('Flu Kucing (Feline Calicivirus)', 'Infeksi saluran pernapasan pada kucing.'),
        ('Parvovirus (CPV)', 'Virus mematikan pada anjing, menyerang saluran cerna.'),
        ('Dermatitis Alergi', 'Peradangan kulit akibat alergi makanan atau lingkungan.'),
        ('Otitis Externa', 'Infeksi telinga luar pada hewan.'),
        ('Fracture / Patah Tulang', 'Patah tulang akibat trauma atau jatuh.'),
        ('Dental Disease', 'Penyakit gigi dan gusi seperti karang gigi atau gingivitis.'),
    ]
    for dn, dd in diag_data:
        get_or_create('pet_clinic.diagnosa', {'name': dn, 'description': dd})

    # =============================================
    # 10. DOSIS
    # =============================================
    dosis_data = [
        ('1x Sehari', 'Diminum 1 kali sehari setelah makan', 1),
        ('2x Sehari', 'Diminum pagi dan malam setelah makan', 2),
        ('3x Sehari', 'Diminum pagi, siang, dan malam', 3),
        ('Oles secukupnya', 'Dioleskan pada area yang luka/sakit', 1),
        ('Injeksi tunggal', 'Diberikan sekali melalui suntikan', 1),
    ]
    for dn, dd, dq in dosis_data:
        get_or_create('pet_clinic.dosis', {'name': dn, 'description': dd, 'quantity': dq})

    # =============================================
    # 11. BANNER, BLOG, EVENT, NOTIF, PROMO
    # =============================================
    get_or_create('pet_clinic.banner', {'name': 'Promo Vaksinasi Mei 2026', 'url': 'https://petclinic.id/promo-vaksinasi'})
    get_or_create('pet_clinic.banner', {'name': 'Grand Opening Cabang Bandung', 'url': 'https://petclinic.id/grand-opening'})
    get_or_create('pet_clinic.banner', {'name': 'Diskon Grooming 30%', 'url': 'https://petclinic.id/diskon-grooming'})

    get_or_create('pet_clinic.blog', {'name': 'Tips Merawat Kucing Persia', 'content': '<p>Kucing Persia membutuhkan perawatan bulu rutin minimal 2x seminggu untuk mencegah bulu kusut dan hairball.</p>'})
    get_or_create('pet_clinic.blog', {'name': 'Panduan Vaksinasi Anjing', 'content': '<p>Vaksinasi dasar anjing meliputi Distemper, Parvovirus, dan Rabies. Jadwal dimulai dari usia 6-8 minggu.</p>'})
    get_or_create('pet_clinic.blog', {'name': 'Nutrisi Tepat untuk Hamster', 'content': '<p>Hamster membutuhkan campuran biji-bijian, sayuran segar, dan protein hewani dalam jumlah kecil.</p>'})

    today = date.today()
    get_or_create('pet_clinic.event', {'name': 'Vaksinasi Massal Gratis', 'date': datetime(2026, 6, 15, 8, 0), 'description': 'Vaksinasi rabies gratis untuk 100 hewan pertama di Cabang Sudirman.'})
    get_or_create('pet_clinic.event', {'name': 'Seminar Nutrisi Hewan', 'date': datetime(2026, 7, 20, 9, 0), 'description': 'Seminar tentang gizi dan nutrisi hewan peliharaan bersama pakar nutrisi.'})
    get_or_create('pet_clinic.event', {'name': 'Pet Adoption Day', 'date': datetime(2026, 8, 10, 10, 0), 'description': 'Acara adopsi hewan dari shelter bekerjasama dengan komunitas pecinta hewan.'})

    get_or_create('pet_clinic.notif', {'name': 'Jadwal Vaksinasi', 'content': 'Hewan peliharaan Anda sudah waktunya divaksinasi ulang. Segera kunjungi klinik kami.', 'type': 'info'})
    get_or_create('pet_clinic.notif', {'name': 'Hasil Lab Tersedia', 'content': 'Hasil pemeriksaan laboratorium hewan Anda sudah tersedia. Silakan hubungi resepsionis.', 'type': 'info'})
    get_or_create('pet_clinic.notif', {'name': 'Peringatan Obat Habis', 'content': 'Stok obat hewan Anda akan habis. Segera isi ulang resep di klinik.', 'type': 'warning'})
    get_or_create('pet_clinic.notif', {'name': 'Kondisi Darurat', 'content': 'Jika hewan Anda menunjukkan tanda darurat, segera bawa ke klinik 24 jam terdekat.', 'type': 'urgent'})

    get_or_create('pet_clinic.promo', {'name': 'Diskon Sterilisasi 20%', 'discount': 20.0, 'date_start': date(2026, 5, 1), 'date_end': date(2026, 5, 31)})
    get_or_create('pet_clinic.promo', {'name': 'Grooming Hemat 30%', 'discount': 30.0, 'date_start': date(2026, 5, 1), 'date_end': date(2026, 6, 30)})
    get_or_create('pet_clinic.promo', {'name': 'Paket Vaksinasi Lengkap', 'discount': 15.0, 'date_start': date(2026, 6, 1), 'date_end': date(2026, 7, 31)})

    # =============================================
    # 12. NOTIF REMINDER, CHECKUP, AFTER SERVICE
    # =============================================
    get_or_create('pet_clinic.notif_reminder', {'name': 'Reminder H-3 Appointment', 'template': 'Yth. {owner}, hewan Anda {pet} memiliki jadwal kunjungan pada {date}. Mohon hadir tepat waktu.', 'days_before': 3})
    get_or_create('pet_clinic.notif_reminder', {'name': 'Reminder H-1 Appointment', 'template': 'Yth. {owner}, besok adalah jadwal kunjungan {pet}. Jangan lupa membawa buku rekam medis.', 'days_before': 1})
    get_or_create('pet_clinic.notif_reminder', {'name': 'Reminder H-7 Vaksinasi', 'template': 'Yth. {owner}, vaksinasi {pet} akan jatuh tempo dalam 7 hari. Segera jadwalkan kunjungan.', 'days_before': 7})

    get_or_create('pet_clinic.notif_reminder_checkup', {'name': 'Checkup Pasca Operasi', 'days_after': 7})
    get_or_create('pet_clinic.notif_reminder_checkup', {'name': 'Checkup Rutin Bulanan', 'days_after': 30})
    get_or_create('pet_clinic.notif_reminder_checkup', {'name': 'Evaluasi Terapi Obat', 'days_after': 14})

    get_or_create('pet_clinic.notif_after_service', {'name': 'Follow Up Grooming', 'days_after': 30})
    get_or_create('pet_clinic.notif_after_service', {'name': 'Follow Up Vaksinasi', 'days_after': 365})
    get_or_create('pet_clinic.notif_after_service', {'name': 'Follow Up Operasi', 'days_after': 7})

    # =============================================
    # 13. CLIENT ACTIVATE & RESET PASSWORD
    # =============================================
    get_or_create('pet_clinic.client_activate', {'name': 'Email Aktivasi Akun', 'template': 'Selamat datang di Pet Clinic! Klik link berikut untuk mengaktifkan akun Anda: {link}'})
    get_or_create('pet_clinic.client_activate', {'name': 'SMS Aktivasi', 'template': 'Kode aktivasi akun Pet Clinic Anda: {code}. Berlaku 24 jam.'})

    get_or_create('pet_clinic.client_reset_password', {'name': 'Email Reset Password', 'template': 'Anda meminta reset password. Klik link berikut: {link}. Abaikan jika bukan Anda.'})
    get_or_create('pet_clinic.client_reset_password', {'name': 'SMS Reset Password', 'template': 'Kode OTP reset password: {code}. Berlaku 15 menit.'})

    # =============================================
    # 14. CLIENTS (Owner)
    # =============================================
    clients_data = [
        ('Sinta Dewi', '081234500001', 'sinta@gmail.com', 'Jl. Menteng Raya No. 10, Jakarta Pusat'),
        ('Doni Pratama', '081234500002', 'doni@gmail.com', 'Jl. Kebon Sirih No. 25, Jakarta Pusat'),
        ('Reza Mahendra', '081234500003', 'reza@gmail.com', 'Jl. Fatmawati No. 33, Jakarta Selatan'),
        ('Rahmat Hidayat', '081234500004', 'rahmat@gmail.com', 'Jl. Cikini Raya No. 5, Jakarta Pusat'),
        ('Putri Ayu', '081234500005', 'putri@gmail.com', 'Jl. Dago No. 77, Bandung'),
        ('Ahmad Fauzi', '081234500006', 'ahmad@gmail.com', 'Jl. Tebet Barat No. 12, Jakarta Selatan'),
        ('Nadia Safira', '081234500007', 'nadia@gmail.com', 'Jl. Braga No. 45, Bandung'),
        ('Bayu Setiawan', '081234500008', 'bayu@gmail.com', 'Jl. Sudirman No. 99, Jakarta Pusat'),
    ]
    clients = {}
    for cn, cp, ce, ca in clients_data:
        clients[cn] = get_or_create('pet_clinic.client', {'name': cn, 'phone': cp, 'email': ce, 'address': ca})

    # =============================================
    # 15. PETS - Hapus data lama yg tidak lengkap, buat ulang
    # =============================================
    # Hapus semua pet lama
    old_pets = env['pet_clinic.pet'].with_context(active_test=False).search([])
    if old_pets:
        # Hapus visitation, appointment, service terkait dulu
        env['pet_clinic.visitation'].search([('pet_id', 'in', old_pets.ids)]).unlink()
        env['pet_clinic.appointment'].search([('pet_id', 'in', old_pets.ids)]).unlink()
        env['pet_clinic.service'].search([('pet_id', 'in', old_pets.ids)]).unlink()
        env['pet_clinic.medical_history_line'].search([('pet_id', 'in', old_pets.ids)]).unlink()
        old_pets.unlink()
        print(f"Deleted {len(old_pets)} old pets and related records.")

    # Reset sequence
    seq = env['ir.sequence'].search([('code', '=', 'pet_clinic.pet')], limit=1)
    if seq:
        seq.write({'number_next_actual': 1})

    pets_data = [
        # (name, owner, type, breed, gender, age_y, age_m, sinyal_amon)
        ('Milo', 'Sinta Dewi', 'Kucing', 'Persia', 'male', 3, 2, 'Baik'),
        ('Luna', 'Sinta Dewi', 'Kucing', 'Anggora', 'female', 2, 5, 'Normal'),
        ('Buddy', 'Doni Pratama', 'Anjing', 'Golden Retriever', 'male', 4, 0, 'Baik'),
        ('Max', 'Doni Pratama', 'Anjing', 'Labrador', 'male', 5, 3, 'Aktif'),
        ('Cleo', 'Reza Mahendra', 'Kucing', 'British Shorthair', 'female', 1, 8, 'Normal'),
        ('Rocky', 'Reza Mahendra', 'Anjing', 'Bulldog', 'male', 3, 6, 'Baik'),
        ('Bella', 'Rahmat Hidayat', 'Anjing', 'Chihuahua', 'female', 2, 0, 'Aktif'),
        ('Simba', 'Rahmat Hidayat', 'Kucing', 'Maine Coon', 'male', 4, 2, 'Baik'),
        ('Ciko', 'Putri Ayu', 'Burung', 'Cockatiel', 'male', 1, 0, 'Normal'),
        ('Kiko', 'Putri Ayu', 'Burung', 'Lovebird', 'male', 0, 9, 'Aktif'),
        ('Nemo', 'Putri Ayu', 'Ikan', 'Cupang', 'male', 0, 6, 'Normal'),
        ('Molly', 'Ahmad Fauzi', 'Kelinci', 'Holland Lop', 'female', 1, 4, 'Baik'),
        ('Coco', 'Ahmad Fauzi', 'Anjing', 'Poodle', 'female', 3, 1, 'Aktif'),
        ('Shiro', 'Nadia Safira', 'Kucing', 'Scottish Fold', 'male', 2, 7, 'Normal'),
        ('Daisy', 'Nadia Safira', 'Anjing', 'Corgi', 'female', 1, 11, 'Baik'),
        ('Hachi', 'Nadia Safira', 'Anjing', 'Shiba Inu', 'male', 3, 0, 'Aktif'),
        ('Brownie', 'Bayu Setiawan', 'Hamster', 'Syrian Hamster', 'male', 0, 8, 'Normal'),
        ('Suki', 'Bayu Setiawan', 'Kucing', 'Siamese', 'female', 2, 3, 'Baik'),
        ('Iggy', 'Bayu Setiawan', 'Reptil', 'Iguana Hijau', 'male', 1, 6, 'Normal'),
        ('Arwa', 'Doni Pratama', 'Ikan', 'Arwana', 'male', 1, 0, 'Baik'),
    ]

    pets = {}
    for pname, oname, tname, bname, gender, ay, am, sa in pets_data:
        dob = today - relativedelta(years=ay, months=am)
        pet = env['pet_clinic.pet'].create({
            'name': pname,
            'owner_id': clients[oname].id,
            'type_id': types[tname].id,
            'breed_id': breeds[bname].id,
            'gender': gender,
            'date_of_birth': dob,
            'sinyal_amon': sa,
            'tgl_pendaftaran': date(2026, 5, 5),
        })
        pets[pname] = pet
        print(f"  [PET] {pet.id_pet} - {pname} ({tname}/{bname}) Owner: {oname}")

    env.cr.commit()
    print("\n=== PHASE 1 DONE: Master Data + Clients + Pets ===")
    print(f"Total pets created: {len(pets)}")
    print("Jalankan seed_all_data_part2.py untuk Appointment & Visitation.")
