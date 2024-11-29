CREATE TABLE guild_members (
    id SERIAL PRIMARY KEY,
    guild_id INT REFERENCES guilds(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'Member', -- e.g., "Leader", "Co-Leader", "Member"
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
