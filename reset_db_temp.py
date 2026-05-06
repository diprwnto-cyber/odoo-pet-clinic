#!/usr/bin/env python3
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="odoo",
        password="adiganteng00",
        host="localhost",
        port=5432
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    # Disallow connections
    try:
        cur.execute('ALTER DATABASE "odoo-pet-clinic" WITH ALLOW_CONNECTIONS false')
        print("Disabled connections")
    except Exception as e:
        print(f"Note: {e}")
    
    # Try to drop with CASCADE/FORCE
    try:
        cur.execute('DROP DATABASE IF EXISTS "odoo-pet-clinic"')
        print("✓ Database 'odoo-pet-clinic' dropped successfully")
    except Exception as e:
        print(f"Drop failed: {e}")
        print("Trying alternative method...")
        raise
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)
