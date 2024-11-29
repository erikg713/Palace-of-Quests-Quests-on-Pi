CREATE TABLE achievements (
    id SERIAL PRIMARY KEY,
    achievement_name VARCHAR(100),
    description TEXT,
    xp_reward INT,
    coin_reward DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
