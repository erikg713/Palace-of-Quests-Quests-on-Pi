CREATE TABLE crafting_materials (
    id SERIAL PRIMARY KEY,
    material_name VARCHAR(100),
    rarity VARCHAR(20), -- e.g., "Common", "Rare", "Epic"
    base_value DECIMAL(10, 2),
    description TEXT
);
