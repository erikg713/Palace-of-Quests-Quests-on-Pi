CREATE TABLE avatar_upgrades (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    level_required INT NOT NULL, -- Minimum level to unlock
    price DECIMAL(10, 2) NOT NULL, -- Price in Pi coins
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
