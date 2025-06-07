-- Table to store achievements for users in the Pi Quest game.
CREATE TABLE achievements (
    id SERIAL PRIMARY KEY, -- Unique identifier for each achievement
    achievement_name VARCHAR(100) NOT NULL UNIQUE, -- Name of the achievement
    description TEXT NOT NULL, -- Description of the achievement
    xp_reward INT NOT NULL DEFAULT 0, -- XP points rewarded for the achievement
    coin_reward DECIMAL(10, 2) NOT NULL DEFAULT 0.00, -- Coin reward for the achievement
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp when the achievement was created
);

-- Add an index for quick lookup of achievements by name
CREATE INDEX idx_achievement_name ON achievements (achievement_name);
