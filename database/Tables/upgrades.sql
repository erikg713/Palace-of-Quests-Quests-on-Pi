CREATE TABLE upgrades (
    upgrade_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    cost INT NOT NULL, -- Cost in experience points
    available_from_level INT NOT NULL
);