# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.abspath('odoo'))
import odoo

odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    field = env['product.template']._fields['type']
    print(f"Selection values for product.template.type: {field.selection}")
