CREATE TABLE user_upgrades (
    user_upgrade_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    upgrade_id INT REFERENCES upgrades(upgrade_id) ON DELETE CASCADE,
    purchased_at TIMESTAMP DEFAULT NOW()
);