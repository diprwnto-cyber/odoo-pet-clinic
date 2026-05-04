SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'odoo-pet-clinic' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS "odoo-pet-clinic";
CREATE DATABASE "odoo-pet-clinic" OWNER odoo;
