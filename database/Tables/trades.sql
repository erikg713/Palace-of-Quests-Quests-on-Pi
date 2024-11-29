CREATE TABLE trades (
    id SERIAL PRIMARY KEY,
    sender_id INT REFERENCES users(id) ON DELETE CASCADE,
    receiver_id INT REFERENCES users(id) ON DELETE CASCADE,
    item_name VARCHAR(100),
    quantity INT DEFAULT 1,
    trade_status VARCHAR(50) DEFAULT 'Pending', -- e.g., "Pending", "Accepted", "Rejected"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
