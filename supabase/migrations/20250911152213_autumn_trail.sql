-- Initialize database with required extensions and basic setup

-- Create extensions if they don't exist
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create database user if not exists (for development)
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'chatgpt_user') THEN

      CREATE ROLE chatgpt_user LOGIN PASSWORD 'chatgpt_password';
   END IF;
END
$do$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE chatgpt_orders TO chatgpt_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO chatgpt_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO chatgpt_user;

-- Set timezone
SET timezone = 'UTC';
