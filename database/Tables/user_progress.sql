CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    current_level INT NOT NULL DEFAULT 1,
    xp INT NOT NULL DEFAULT 0,
    last_level_up TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
