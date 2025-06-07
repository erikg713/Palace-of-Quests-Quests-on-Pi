CREATE TYPE battle_outcome AS ENUM ('Win', 'Lose');

CREATE TABLE battles (
    id SERIAL PRIMARY KEY,
    player_id INT REFERENCES users(id) ON DELETE CASCADE,
    enemy_id INT REFERENCES enemies(id) ON DELETE CASCADE,
    outcome battle_outcome NOT NULL, -- Outcome of the battle
    damage_dealt INT NOT NULL CHECK (damage_dealt >= 0), -- Total damage dealt by the player
    damage_taken INT NOT NULL CHECK (damage_taken >= 0), -- Total damage taken by the player
    battle_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Time of the battle
    battle_duration INT -- Duration of the battle in seconds
);

CREATE INDEX idx_player_id ON battles(player_id);
CREATE INDEX idx_enemy_id ON battles(enemy_id);
CREATE INDEX idx_battle_time ON battles(battle_time);
