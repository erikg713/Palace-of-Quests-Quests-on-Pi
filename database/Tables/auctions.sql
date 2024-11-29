CREATE TABLE auctions (
    id SERIAL PRIMARY KEY,
    seller_id INT REFERENCES users(id) ON DELETE CASCADE,
    item_name VARCHAR(100),
    starting_bid DECIMAL(10, 2),
    current_bid DECIMAL(10, 2) DEFAULT NULL,
    bidder_id INT REFERENCES users(id) ON DELETE CASCADE,
    end_time TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Active' -- e.g., "Active", "Completed", "Canceled"
);
