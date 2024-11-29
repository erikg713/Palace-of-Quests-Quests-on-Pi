CREATE TABLE guilds (
    id SERIAL PRIMARY KEY,
    guild_name VARCHAR(100) UNIQUE NOT NULL,
    leader_id INT REFERENCES users(id) ON DELETE CASCADE, -- Guild leader
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
