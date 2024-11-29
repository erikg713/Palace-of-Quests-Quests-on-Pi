CREATE TABLE leaderboard_history (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    season_name VARCHAR(100),
    rank INT,
    xp INT,
    coins INT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
