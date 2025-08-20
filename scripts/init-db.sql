-- Initialize La Vida Luca Database
-- This script sets up the basic database structure for development

-- Create database for testing if it doesn't exist
SELECT 'CREATE DATABASE lavidaluca_test'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'lavidaluca_test')\gexec

-- Grant permissions to postgres user
GRANT ALL PRIVILEGES ON DATABASE lavidaluca_dev TO postgres;
GRANT ALL PRIVILEGES ON DATABASE lavidaluca_test TO postgres;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create basic tables if they don't exist (will be handled by Alembic migrations)
-- This is just for initial development setup