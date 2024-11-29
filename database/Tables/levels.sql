CREATE TABLE levels (
    id SERIAL PRIMARY KEY,
    level_number INT NOT NULL UNIQUE,
    xp_required INT NOT NULL, -- XP needed to unlock this level
    reward_description TEXT, -- Details of the reward
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE levels (
    level_id SERIAL PRIMARY KEY,
    level_number INT NOT NULL UNIQUE,
    experience_required INT NOT NULL,
    reward JSONB DEFAULT '{}'
);