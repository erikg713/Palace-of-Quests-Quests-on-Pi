CREATE TABLE game_progress (
    progress_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    level_number INT NOT NULL,
    completed_at TIMESTAMP DEFAULT NOW()
);