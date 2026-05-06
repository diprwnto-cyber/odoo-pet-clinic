import sys
import os

sys.path.append(os.path.abspath('odoo'))

import odoo

odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Kategori default 'All'
    category = env['product.category'].search([('name', '=', 'All')], limit=1)
    if not category:
        category = env['product.category'].create({'name': 'All'})
    
    products_data = [
        # Layanan / Jasa (type: 'service')
        {'name': 'Konsultasi Dokter Hewan', 'type': 'service', 'list_price': 100000.0, 'standard_price': 0.0, 'categ_id': category.id},
        {'name': 'Grooming Kucing (Basic)', 'type': 'service', 'list_price': 50000.0, 'standard_price': 10000.0, 'categ_id': category.id},
        {'name': 'Grooming Anjing (Basic)', 'type': 'service', 'list_price': 70000.0, 'standard_price': 15000.0, 'categ_id': category.id},
        {'name': 'Rawat Inap (Per Malam)', 'type': 'service', 'list_price': 150000.0, 'standard_price': 50000.0, 'categ_id': category.id},
        {'name': 'Vaksinasi Rabies', 'type': 'service', 'list_price': 200000.0, 'standard_price': 100000.0, 'categ_id': category.id},
        {'name': 'Operasi Steril Kucing Jantan', 'type': 'service', 'list_price': 300000.0, 'standard_price': 50000.0, 'categ_id': category.id},
        {'name': 'Operasi Steril Kucing Betina', 'type': 'service', 'list_price': 450000.0, 'standard_price': 100000.0, 'categ_id': category.id},
        
        # Obat & Barang (type: 'consu' / Consumable)
        {'name': 'Obat Cacing Drontal (Tablet)', 'type': 'consu', 'list_price': 25000.0, 'standard_price': 15000.0, 'categ_id': category.id},
        {'name': 'Obat Kutu Bravecto', 'type': 'consu', 'list_price': 250000.0, 'standard_price': 200000.0, 'categ_id': category.id},
        {'name': 'Vitamin Nutriplus Gel 120g', 'type': 'consu', 'list_price': 120000.0, 'standard_price': 90000.0, 'categ_id': category.id},
        {'name': 'Kalung Kucing (Collar)', 'type': 'consu', 'list_price': 30000.0, 'standard_price': 15000.0, 'categ_id': category.id},
        {'name': 'Makanan Kucing Royal Canin 1Kg', 'type': 'consu', 'list_price': 150000.0, 'standard_price': 120000.0, 'categ_id': category.id},
        {'name': 'Shampoo Anti Kutu 250ml', 'type': 'consu', 'list_price': 45000.0, 'standard_price': 25000.0, 'categ_id': category.id},
        {'name': 'Suntik Antibiotik', 'type': 'service', 'list_price': 80000.0, 'standard_price': 30000.0, 'categ_id': category.id},
    ]
    
    count = 0
    for data in products_data:
        # Cek apakah sudah ada untuk menghindari duplikat
        existing = env['product.template'].search([('name', '=', data['name'])])
        if not existing:
            env['product.template'].create(data)
            count += 1
            
    env.cr.commit()
    print(f"Berhasil membuat {count} produk klinik hewan!")
