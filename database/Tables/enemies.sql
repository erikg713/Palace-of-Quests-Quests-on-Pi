CREATE TABLE enemies (
    id SERIAL PRIMARY KEY,
    enemy_name VARCHAR(100),
    description TEXT,
    level INT NOT NULL,
    health INT NOT NULL,
    attack_power INT NOT NULL,
    defense INT NOT NULL,
    loot JSONB -- Rewards players can earn after defeating the enemy
);
