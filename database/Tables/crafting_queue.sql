CREATE TABLE crafting_queue (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    recipe_id INT REFERENCES crafting_recipes(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'In Progress', -- e.g., "In Progress", "Completed"
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);
