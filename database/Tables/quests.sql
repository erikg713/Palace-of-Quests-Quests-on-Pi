CREATE TABLE quests (
    id SERIAL PRIMARY KEY,
    quest_name VARCHAR(100),
    description TEXT,
    quest_type VARCHAR(50), -- e.g., "Main", "Side"
    xp_reward INT,
    coin_reward DECIMAL(10, 2),
    is_recurring BOOLEAN DEFAULT FALSE, -- True for repeatable quests
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
