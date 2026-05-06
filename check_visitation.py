import sys
import os

sys.path.append(os.path.abspath('odoo'))

import odoo

odoo.tools.config.parse_config(['-c', 'odoo/odoo.conf', '-d', 'odoo-pet-clinic'])

registry = odoo.registry('odoo-pet-clinic')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Ambil data visitation
    visitations = env['pet_clinic.visitation'].search([])
    
    print(f"Total Visitations: {len(visitations)}")
    for v in visitations:
        print(f"[{v.name}] Pet: {v.pet_id.name}, Owner: {v.owner_id.name}, Doctor: {v.doctor_id.name}, Status: {v.state}")
