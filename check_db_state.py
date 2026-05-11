# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.abspath('odoo'))
import odoo

odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("Checking Product fields...")
    Product = env['product.product']
    fields = Product._fields.keys()
    print(f"qty_available in fields: {'qty_available' in fields}")
    
    print("\nChecking empty tables...")
    models = [
        'pet_clinic.visitation_item',
        'pet_clinic.visitation_barang',
        'pet_clinic.service',
        'pet_clinic.medical_history_line',
        'pet_clinic.appointment',
        'pet_clinic.visitation',
    ]
    for m in models:
        count = env[m].search_count([])
        print(f"{m}: {count} records")

    print("\nChecking installed modules...")
    modules = env['ir.module.module'].search([('state', '=', 'installed')])
    module_names = modules.mapped('name')
    print(f"stock installed: {'stock' in module_names}")
    print(f"point_of_sale installed: {'point_of_sale' in module_names}")
