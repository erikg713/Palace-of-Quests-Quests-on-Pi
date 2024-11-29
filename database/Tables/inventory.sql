CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    item_name VARCHAR(100),
    item_type VARCHAR(50), -- e.g., "Avatar Upgrade", "Weapon"
    rarity VARCHAR(20), -- e.g., "Common", "Rare", "Legendary"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
