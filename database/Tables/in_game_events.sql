CREATE TABLE in_game_events (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(100),
    description TEXT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    rewards JSONB -- Stores event-specific rewards as JSON
);
