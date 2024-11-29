CREATE TABLE challenges (
    id SERIAL PRIMARY KEY,
    challenge_name VARCHAR(100),
    description TEXT,
    xp_reward INT,
    coin_reward DECIMAL(10, 2),
    difficulty_level INT, -- 1-10 scale
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO challenges (challenge_name, description, total_steps, reward)
VALUES
    ('Sword Training', 'Complete 100 sword swings.', 100, 500.0),
    ('Shield Mastery', 'Block 50 attacks.', 50, 300.0);
