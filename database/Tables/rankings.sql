CREATE TABLE rankings (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    mode VARCHAR(50), -- e.g., "Battle Mode", "Challenge Mode"
    rank INT,
    points INT,
    season_name VARCHAR(100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
