-- ============================
-- Table: enemies
-- Purpose: Stores all enemy types for the metaverse game
-- ============================

CREATE TABLE IF NOT EXISTS enemies (
    id SERIAL PRIMARY KEY,                              -- Unique enemy identifier
    enemy_name VARCHAR(100) NOT NULL UNIQUE,            -- Enemy's name, must be unique
    description TEXT,                                   -- Detailed description
    level INT NOT NULL CHECK (level >= 1),              -- Enemy's level, minimum 1
    health INT NOT NULL CHECK (health > 0),             -- Health pool, must be positive
    attack_power INT NOT NULL DEFAULT 10 CHECK (attack_power >= 0), -- Base attack strength
    defense INT NOT NULL DEFAULT 5 CHECK (defense >= 0),            -- Base defense value
    loot JSONB NOT NULL DEFAULT '[]',                   -- Loot as JSON array, default empty
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),  -- Creation timestamp
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()   -- Last update timestamp
);

-- Automatically update "updated_at" on row modification (PostgreSQL trigger example)
CREATE OR REPLACE FUNCTION update_enemies_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_update_enemies_updated_at ON enemies;

CREATE TRIGGER trg_update_enemies_updated_at
BEFORE UPDATE ON enemies
FOR EACH ROW
EXECUTE FUNCTION update_enemies_updated_at();

-- Index for faster search on level (commonly filtered)
CREATE INDEX IF NOT EXISTS idx_enemies_level ON enemies(level);

-- Index for quick lookup by name
CREATE INDEX IF NOT EXISTS idx_enemies_enemy_name ON enemies(enemy_name);

-- ===========================================
-- Sample usage: 
--   Insert a new enemy
--   INSERT INTO enemies (enemy_name, description, level, health, attack_power, defense, loot)
--   VALUES ('Goblin Raider', 'Aggressive goblin found in the wild.', 2, 120, 15, 7, '[{"item":"Pi Coin","amount":3}]');
-- ===========================================
