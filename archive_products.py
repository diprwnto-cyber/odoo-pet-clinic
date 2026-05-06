import sys
import os

# Menambahkan path odoo agar bisa diimport
sys.path.append(os.path.abspath('odoo'))

import odoo

# Load konfigurasi
odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

# Connect ke database
registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Cari semua produk yang ada saat ini
    products = env['product.template'].search([('active', '=', True)])
    
    count = 0
    for product in products:
        # Kita matikan status active-nya (diarsipkan)
        product.active = False
        count += 1
        
    env.cr.commit()
    print(f"Berhasil mengarsipkan {count} produk demo/bawaan!")
