-- ENUM for rarity
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'rarity_enum') THEN
        CREATE TYPE rarity_enum AS ENUM ('Common', 'Uncommon', 'Rare', 'Epic', 'Legendary');
    END IF;
END$$;

-- Table definition
CREATE TABLE IF NOT EXISTS crafting_materials (
    id SERIAL PRIMARY KEY,
    material_name VARCHAR(100) NOT NULL UNIQUE,
    rarity rarity_enum NOT NULL DEFAULT 'Common',
    base_value NUMERIC(12, 2) NOT NULL CHECK (base_value >= 0),
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Trigger for automatic updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_updated_at ON crafting_materials;
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON crafting_materials
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

-- Indexes
CREATE INDEX IF NOT EXISTS idx_crafting_materials_rarity ON crafting_materials(rarity);
CREATE INDEX IF NOT EXISTS idx_crafting_materials_base_value ON crafting_materials(base_value);
