CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    wallet_address VARCHAR(100) NOT NULL
);

CREATE TABLE quests (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    payment_id VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    txid VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    wallet_address VARCHAR(100)
);

CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    item_type VARCHAR(50),
    price NUMERIC(10, 2),
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE quests (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    user_id INTEGER REFERENCES users(id)
);

CREATE INDEX idx_user_id ON users (id);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    payment_id VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(50) NOT NULL,
    txid VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

from app import db
from datetime import datetime

def update_payment_status(payment_id, status, txid=None):
    payment = Payment.query.filter_by(payment_id=payment_id).first()
    if payment:
        payment.status = status
        payment.txid = txid
        payment.updated_at = datetime.utcnow()
        db.session.commit()

ALTER TABLE payments
ADD COLUMN status VARCHAR(50) DEFAULT 'pending';

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    wallet_address VARCHAR(100) NOT NULL
);

CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    item_type VARCHAR(50),
    price NUMERIC(10, 2),
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE quests (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    payment_id VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    txid VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE INDEX idx_user_id ON users (id);
CREATE INDEX idx_payment_id ON payments (payment_id);

ALTER TABLE quests 
    ADD COLUMN type VARCHAR(50) DEFAULT 'standard';

ALTER TABLE items 
    ADD COLUMN rarity VARCHAR(20) DEFAULT 'common',
    ADD COLUMN upgrade_level INTEGER DEFAULT 1;

CREATE TABLE achievements (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    points INTEGER DEFAULT 10
);

CREATE TABLE user_achievements (
    user_id INTEGER REFERENCES users(id),
    achievement_id INTEGER REFERENCES achievements(id),
    date_earned TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, achievement_id)
);

ALTER TABLE avatars 
    ADD COLUMN hairstyle VARCHAR(50) DEFAULT 'default',
    ADD COLUMN weapon_skin VARCHAR(50) DEFAULT 'standard',
    ADD COLUMN background_theme VARCHAR(50) DEFAULT 'plain';

CREATE TABLE level_rewards (
    level INTEGER PRIMARY KEY,
    reward_name VARCHAR(100),
    reward_description TEXT,
    stat_boost INTEGER DEFAULT 0,
    item_unlock VARCHAR(100),
    quest_difficulty INTEGER
);

CREATE TABLE premium_benefits (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    price_pi DECIMAL(10, 2) NOT NULL,
    benefit_type VARCHAR(50),
    duration_days INTEGER DEFAULT 0  -- Duration for time-limited benefits
);

INSERT INTO premium_benefits (name, description, price_pi, benefit_type, duration_days)
VALUES 
('XP Boost', 'Double experience points for 7 days', 5.00, 'xp_boost', 7),
('Exclusive Sword', 'A powerful sword only available to premium members', 3.00, 'item', 0),
('Premium Guild Pass', 'Access to elite guilds with exclusive quests', 10.00, 'guild_access', 30);

CREATE TABLE IF NOT EXISTS premium_benefits (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    price_pi DECIMAL(10, 2) NOT NULL,
    benefit_type VARCHAR(50) CHECK (benefit_type IN ('xp_boost', 'item', 'guild_access')),
    duration_days INTEGER DEFAULT 0 CHECK (duration_days >= 0)
);

INSERT INTO premium_benefits (name, description, price_pi, benefit_type, duration_days)
VALUES 
('XP Boost', 'Double experience points for 7 days', 5.00, 'xp_boost', 7),
('Exclusive Sword', 'A powerful sword only available to premium members', 3.00, 'item', 0),
('Premium Guild Pass', 'Access to elite guilds with exclusive quests', 10.00, 'guild_access', 30);
