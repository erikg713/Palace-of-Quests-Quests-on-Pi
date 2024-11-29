CREATE TABLE player_materials (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    material_id INT REFERENCES crafting_materials(id) ON DELETE CASCADE,
    quantity INT DEFAULT 0
);
