CREATE TABLE rewards (
    id SERIAL PRIMARY KEY,
    reward_name VARCHAR(100),
    reward_type VARCHAR(50), -- e.g., "XP", "Item", "Coin"
    value INT,
    level_unlock INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
