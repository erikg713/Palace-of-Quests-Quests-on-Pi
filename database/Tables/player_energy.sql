CREATE TABLE player_energy (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    energy_level INT DEFAULT 100, -- Max energy level
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
