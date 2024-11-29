CREATE TABLE battles (
    id SERIAL PRIMARY KEY,
    player_id INT REFERENCES users(id) ON DELETE CASCADE,
    enemy_id INT REFERENCES enemies(id) ON DELETE CASCADE,
    outcome VARCHAR(50), -- e.g., "Win", "Lose"
    damage_dealt INT NOT NULL,
    damage_taken INT NOT NULL,
    battle_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
