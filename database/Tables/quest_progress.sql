CREATE TABLE quest_progress (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    quest_id INT REFERENCES quests(id) ON DELETE CASCADE,
    is_completed BOOLEAN DEFAULT FALSE,
    completion_date TIMESTAMP,
    attempts INT DEFAULT 0
);
