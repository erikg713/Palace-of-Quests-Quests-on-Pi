-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    wallet_address VARCHAR(100) NOT NULL
);

-- Inventory table
CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    item_type VARCHAR(50) NOT NULL,
    price NUMERIC(10, 2),
    rarity VARCHAR(20) DEFAULT 'common',
    upgrade_level INTEGER DEFAULT 1,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

-- Quests table
CREATE TABLE IF NOT EXISTS quests (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type VARCHAR(50) DEFAULT 'standard',
    is_completed BOOLEAN DEFAULT FALSE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    payment_id VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    txid VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

-- Achievements table
CREATE TABLE IF NOT EXISTS achievements (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    points INTEGER DEFAULT 10
);

-- User achievements table
CREATE TABLE IF NOT EXISTS user_achievements (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    achievement_id INTEGER REFERENCES achievements(id) ON DELETE CASCADE,
    date_earned TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, achievement_id)
);

-- Level rewards table
CREATE TABLE IF NOT EXISTS level_rewards (
    level INTEGER PRIMARY KEY,
    reward_name VARCHAR(100),
    reward_description TEXT,
    stat_boost INTEGER DEFAULT 0,
    item_unlock VARCHAR(100),
    quest_difficulty INTEGER NOT NULL
);

-- Premium benefits table
CREATE TABLE IF NOT EXISTS premium_benefits (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    price_pi DECIMAL(10, 2) NOT NULL,
    benefit_type VARCHAR(50) CHECK (benefit_type IN ('xp_boost', 'item', 'guild_access')),
    duration_days INTEGER DEFAULT 0 CHECK (duration_days >= 0)
);

-- Insert premium benefits
INSERT INTO premium_benefits (name, description, price_pi, benefit_type, duration_days)
VALUES 
    ('XP Boost', 'Double experience points for 7 days', 5.00, 'xp_boost', 7),
    ('Exclusive Sword', 'A powerful sword only available to premium members', 3.00, 'item', 0),
    ('Premium Guild Pass', 'Access to elite guilds with exclusive quests', 10.00, 'guild_access', 30)
ON CONFLICT (name) DO NOTHING;

-- Indexing for performance
CREATE INDEX IF NOT EXISTS idx_user_id ON users (id);
CREATE INDEX IF NOT EXISTS idx_payment_id ON payments (payment_id);
CREATE INDEX IF NOT EXISTS idx_quest_user_id ON quests (user_id);
CREATE INDEX IF NOT EXISTS idx_inventory_user_id ON inventory (user_id);
