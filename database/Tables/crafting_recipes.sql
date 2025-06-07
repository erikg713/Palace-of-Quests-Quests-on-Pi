-- Enhanced Table: crafting_recipes
CREATE TABLE IF NOT EXISTS crafting_recipes (
    id SERIAL PRIMARY KEY,
    recipe_name VARCHAR(100) NOT NULL UNIQUE,
    item_result VARCHAR(100) NOT NULL,
    materials_required JSONB NOT NULL CHECK (jsonb_typeof(materials_required) = 'object'),
    crafting_time INT DEFAULT 0 CHECK (crafting_time >= 0),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Automatically update updated_at on row modification
CREATE OR REPLACE FUNCTION update_crafting_recipes_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_crafting_recipes_updated_at ON crafting_recipes;
CREATE TRIGGER set_crafting_recipes_updated_at
BEFORE UPDATE ON crafting_recipes
FOR EACH ROW
EXECUTE FUNCTION update_crafting_recipes_updated_at();
