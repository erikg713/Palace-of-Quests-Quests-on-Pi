-- ============================
-- Role & Permissions Setup Script for Palace of Quests
-- ============================

-- SECURITY NOTE:
--   Do NOT use plain-text passwords in production.
--   Consider using a secure password management method or environment variables.

-- === 1. Create ROLE if not exists ===
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'gameuser') THEN
        CREATE ROLE gameuser LOGIN PASSWORD 'REPLACE_WITH_STRONG_PASSWORD';
    END IF;
END;
$$ LANGUAGE plpgsql;

-- === 2. Grant Database Connectivity ===
-- (Add additional databases here if needed)
GRANT CONNECT ON DATABASE piquest_db TO gameuser;
GRANT CONNECT ON DATABASE palaceofquests_db TO gameuser;

-- === 3. Grant Table Permissions ===
-- TIP: For tighter security, grant privileges per-table instead of all tables.
-- Example for specific tables:
-- GRANT SELECT, INSERT, UPDATE ON public.quest_data TO gameuser;
-- GRANT SELECT, INSERT, UPDATE ON public.reward_data TO gameuser;

-- To grant on all current and future tables in the schema:
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN SELECT datname FROM pg_database WHERE datname IN ('piquest_db','palaceofquests_db') LOOP
        EXECUTE format('
            GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO gameuser;
            ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE ON TABLES TO gameuser;
        ');
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- === 4. Documentation ===
-- gameuser: Used by the game backend to access and modify quest/reward data.
-- Restricted to only necessary actions for enhanced security.
-- Update passwords and privileges as your schema evolves.

-- === 5. Cleanup Example (Optional) ===
-- To remove the role if needed:
-- DROP ROLE IF EXISTS gameuser;
