import sys
import os
import csv

sys.path.append(os.path.abspath('odoo'))

import odoo

odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    visitations = env['pet_clinic.visitation'].search([])
    
    with open('visitation_export.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Header
        writer.writerow(['Visitation No', 'Nomor Rekam Medis', 'Owner', 'Pet', 'Umur', 'Penanganan', 'Room', 'Status Pasien', 'Doctor', 'Status'])
        
        # Data
        for v in visitations:
            writer.writerow([
                v.name or '',
                v.nomor_rekam_medis or '',
                v.owner_id.name if v.owner_id else '',
                v.pet_id.name if v.pet_id else '',
                v.umur or '',
                v.penanganan or '',
                v.room_id.name if v.room_id else '',
                v.status_pasien or '',
                v.doctor_id.name if v.doctor_id else '',
                v.state or ''
            ])
            
    print("Berhasil membuat file visitation_export.csv")
