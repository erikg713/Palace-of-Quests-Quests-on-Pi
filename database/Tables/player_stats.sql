CREATE TABLE player_stats (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    level INT DEFAULT 1,
    xp INT DEFAULT 0,
    total_xp INT DEFAULT 0,
    coins DECIMAL(10, 2) DEFAULT 0.00,
    last_login TIMESTAMP
);
