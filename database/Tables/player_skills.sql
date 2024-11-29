CREATE TABLE player_skills (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    skill_id INT REFERENCES skills(id) ON DELETE CASCADE,
    current_level INT DEFAULT 1,
    last_upgraded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
