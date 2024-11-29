CREATE TABLE player_properties (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    property_id INT REFERENCES properties(id) ON DELETE CASCADE,
    customization JSONB, -- Stores customizations made by players
    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
