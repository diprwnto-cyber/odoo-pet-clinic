# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.abspath('odoo'))
import odoo

odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    Product = env['product.template']
    # Check fields that have 'stock' or 'qty' or 'type' or 'storable'
    fields = [f for f in Product._fields.keys() if any(x in f for x in ['stock', 'qty', 'type', 'storable'])]
    print(f"Interesting fields: {fields}")
    
    # Check current values for one product
    p = Product.search([('type', '!=', 'service')], limit=1)
    if p:
        print(f"\nProduct: {p.name}")
        for f in fields:
            try:
                print(f"  {f}: {getattr(p, f)}")
            except:
                pass
