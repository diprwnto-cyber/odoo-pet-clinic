# -*- coding: utf-8 -*-
"""Fill Cost (standard_price) untuk semua product di master data."""
import sys
import os

sys.path.append(os.path.abspath('odoo'))

import odoo

odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

    # Mapping nama product -> standard_price (cost)
    # Cost dihitung ~40-60% dari harga jual untuk jasa, ~60-80% untuk barang
    cost_map = {
        # === DARI master_data.xml (product.product) ===
        # Services (Pet Clinic Services)
        'Konsultasi Dokter Hewan': 30000,
        'Vaksinasi': 90000,
        'Obat Cacing': 30000,
        'Grooming Basic': 35000,
        'Grooming Premium': 60000,
        'Tindakan Minor': 100000,
        'Pemeriksaan Laboratorium': 80000,
        'Pet Hotel Per Hari': 50000,

        # Medicine (Pet Clinic Medicine)
        'Antibiotik Hewan': 25000,
        'Vitamin Hewan': 18000,

        # Supplies (Pet Clinic Supplies)
        'Pet Shampoo': 30000,

        # === DARI seed_products.py (product.template) ===
        # Services
        'Grooming Kucing (Basic)': 10000,
        'Grooming Anjing (Basic)': 15000,
        'Rawat Inap (Per Malam)': 50000,
        'Vaksinasi Rabies': 100000,
        'Operasi Steril Kucing Jantan': 50000,
        'Operasi Steril Kucing Betina': 100000,
        'Suntik Antibiotik': 30000,

        # Consumables
        'Obat Cacing Drontal (Tablet)': 15000,
        'Obat Kutu Bravecto': 200000,
        'Vitamin Nutriplus Gel 120g': 90000,
        'Kalung Kucing (Collar)': 15000,
        'Makanan Kucing Royal Canin 1Kg': 120000,
        'Shampoo Anti Kutu 250ml': 25000,
    }

    updated = 0
    skipped = 0

    # Update product.template (covers all products)
    all_templates = env['product.template'].search([])
    print(f"\nTotal product.template ditemukan: {len(all_templates)}")
    print("=" * 60)

    for tmpl in all_templates:
        name = tmpl.name
        if name in cost_map:
            old_cost = tmpl.standard_price
            new_cost = cost_map[name]
            tmpl.standard_price = new_cost
            status = f"UPDATED {old_cost:>10,.0f} -> {new_cost:>10,.0f}"
            updated += 1
        else:
            old_cost = tmpl.standard_price
            if old_cost == 0:
                # Product tidak ada di mapping, isi default 40% dari list_price
                new_cost = round(tmpl.list_price * 0.4, -3)  # Bulatkan ke ribuan
                if new_cost > 0:
                    tmpl.standard_price = new_cost
                    status = f"AUTO-FILL (40%) {old_cost:>10,.0f} -> {new_cost:>10,.0f}"
                    updated += 1
                else:
                    status = f"SKIPPED (list_price=0)"
                    skipped += 1
            else:
                status = f"ALREADY HAS COST: {old_cost:>10,.0f}"
                skipped += 1

        print(f"  [{tmpl.type:>7}] {name:<40} | list_price: {tmpl.list_price:>10,.0f} | {status}")

    env.cr.commit()
    print("=" * 60)
    print(f"\nDONE! Updated: {updated}, Skipped: {skipped}")
    print(f"Total products: {len(all_templates)}")
