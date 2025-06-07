CREATE TABLE avatar_upgrades (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    level_required INT NOT NULL CHECK (level_required >= 0), -- Minimum level to unlock
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0), -- Price in Pi coins
    image_url VARCHAR(255) CHECK (image_url ~ '^(https?:\/\/).+'), -- Validate URL format
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Indexes for efficiency
CREATE INDEX idx_level_required ON avatar_upgrades(level_required);
CREATE INDEX idx_price ON avatar_upgrades(price);
