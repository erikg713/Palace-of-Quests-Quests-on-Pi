-- ===========================================
-- Inventory Table
-- Tracks all items owned by users
-- ===========================================

CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    item_name VARCHAR(100) NOT NULL,
    item_type VARCHAR(50) NOT NULL, -- e.g., 'Avatar Upgrade', 'Weapon'
    rarity VARCHAR(20) NOT NULL CHECK (rarity IN ('Common', 'Rare', 'Epic', 'Legendary')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT inventory_unique_user_item UNIQUE (user_id, item_name)
);

-- Index for efficient user inventory queries
CREATE INDEX IF NOT EXISTS idx_inventory_user_id ON inventory(user_id);

-- Optional: Index for querying items by rarity (uncomment if needed)
-- CREATE INDEX IF NOT EXISTS idx_inventory_rarity ON inventory(rarity);
