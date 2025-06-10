CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    transaction_type VARCHAR(50), -- e.g., "Marketplace Purchase", "Subscription"
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'Pi',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50),
    pi_amount DECIMAL,
    payment_id VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
