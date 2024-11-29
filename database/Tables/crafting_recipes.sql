CREATE TABLE crafting_recipes (
    id SERIAL PRIMARY KEY,
    recipe_name VARCHAR(100),
    item_result VARCHAR(100), -- Item crafted
    materials_required JSONB, -- JSON object with material details
    crafting_time INT DEFAULT 0 -- Time required in seconds
);
