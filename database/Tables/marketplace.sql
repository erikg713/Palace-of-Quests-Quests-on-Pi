CREATE TABLE marketplace (
    id SERIAL PRIMARY KEY,
    seller_id INT REFERENCES users(id) ON DELETE CASCADE,
    item_name VARCHAR(100),
    price DECIMAL(10, 2),
    currency VARCHAR(10) DEFAULT 'Pi',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
