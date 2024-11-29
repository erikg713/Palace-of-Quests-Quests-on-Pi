CREATE TABLE user_inventory (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    upgrade_id INT REFERENCES avatar_upgrades(id),
    quantity INT DEFAULT 1,
    acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);