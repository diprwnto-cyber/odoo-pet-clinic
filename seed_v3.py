# -*- coding: utf-8 -*-
"""Seed v3: Fill Visitation Lines, Medical History, and Product Stock."""
import sys
import os
import random
from datetime import datetime, timedelta

sys.path.append(os.path.abspath('odoo'))
import odoo

odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

    # ============================================================
    # 1. SET PRODUCT STOCK (Initial Inventory)
    # ============================================================
    print("Initializing Product Stock...")
    # In Odoo 18, use is_storable=True for products that track stock
    products = env['product.product'].search([('type', '!=', 'service')])
    products.write({'is_storable': True})
    
    warehouse = env['stock.warehouse'].search([], limit=1)
    location = warehouse.lot_stock_id if warehouse else env['stock.location'].search([('usage', '=', 'internal')], limit=1)

    if not location:
        print("Error: No internal stock location found!")
    else:
        for product in products:
            qty = random.randint(50, 200)
            try:
                # Reset old quants to avoid accumulation
                env['stock.quant'].search([('product_id', '=', product.id), ('location_id', '=', location.id)]).unlink()
                
                env['stock.quant'].with_context(inventory_mode=True).create({
                    'product_id': product.id,
                    'location_id': location.id,
                    'inventory_quantity': qty,
                }).action_apply_inventory()
                print(f"  [STOCK] {product.name}: set to {qty}")
            except Exception as e:
                print(f"  [STOCK] Error setting qty for {product.name}: {str(e)}")

    # ============================================================
    # 2. FILL VISITATION LINES (Services, Items, Barang)
    # ============================================================
    print("\nFilling Visitation Lines...")
    visitations = env['pet_clinic.visitation'].search([])
    
    # Get some master data
    services = env['product.product'].search([('type', '=', 'service')])
    items = env['product.product'].search([('type', '!=', 'service')])
    
    for vis in visitations:
        # 2a. Add Services
        if not vis.service_ids:
            s_picks = random.sample(list(services), min(2, len(services)))
            for s in s_picks:
                env['pet_clinic.service'].create({
                    'visitation_id': vis.id,
                    'pet_id': vis.pet_id.id,
                    'nama_pemilik': vis.owner_id.id,
                    'service_type': s.id,
                    'amount': 1,
                })
            print(f"  [VISIT-SVC] Added {len(s_picks)} services to {vis.name}")

        # 2b. Add Items (Visitation Items)
        if not vis.item_ids:
            i_picks = random.sample(list(items), min(2, len(items)))
            for i in i_picks:
                env['pet_clinic.visitation_item'].create({
                    'visitation_id': vis.id,
                    'product_id': i.id,
                    'quantity': random.randint(1, 3),
                    'price': i.list_price,
                })
            print(f"  [VISIT-ITEM] Added {len(i_picks)} items to {vis.name}")

        # 2c. Add Barang/Obat Pulang
        if not vis.barang_ids:
            b_picks = random.sample(list(items), min(1, len(items)))
            for b in b_picks:
                env['pet_clinic.visitation_barang'].create({
                    'visitation_id': vis.id,
                    'product_id': b.id,
                    'quantity': random.randint(1, 2),
                    'price': b.list_price,
                })
            print(f"  [VISIT-BARANG] Added {len(b_picks)} meds to {vis.name}")

        # 2d. Create Medical History Line (if visitation is done)
        if vis.state == 'done':
            existing_hist = env['pet_clinic.medical_history_line'].search([
                ('pet_id', '=', vis.pet_id.id),
                ('date_start', '=', vis.date_start)
            ])
            if not existing_hist:
                env['pet_clinic.medical_history_line'].create({
                    'pet_id': vis.pet_id.id,
                    'date_start': vis.date_start,
                    'doctor_id': vis.doctor_id.id if vis.doctor_id else False,
                    'anamnesa': vis.anamnesa,
                    'diagnosis': vis.diagnosis,
                    'therapy': vis.therapy,
                    'temperature': vis.temperature,
                    'weight': vis.weight,
                    'bcs': vis.bcs,
                    'action': vis.action_field,
                })
                print(f"  [HIST] Created history for {vis.pet_id.name}")

    env.cr.commit()
    print("\n=== SEED V3 DONE ===")
