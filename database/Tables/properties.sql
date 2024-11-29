CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    property_name VARCHAR(100),
    description TEXT,
    base_price DECIMAL(10, 2),
    max_capacity INT DEFAULT 10, -- Max items/guests allowed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
