CREATE TABLE friends (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    friend_id INT REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'Pending', -- e.g., "Pending", "Accepted", "Blocked"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
