CREATE TABLE taxes (
    id SERIAL PRIMARY KEY,
    transaction_type VARCHAR(50), -- e.g., "Marketplace Sale", "Auction"
    tax_rate DECIMAL(5, 2), -- Percentage
    collected_amount DECIMAL(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
