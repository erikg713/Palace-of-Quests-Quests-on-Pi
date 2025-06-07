CREATE TABLE auctions (
    id SERIAL PRIMARY KEY,
    seller_id INT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    item_name VARCHAR(100) NOT NULL,
    starting_bid DECIMAL(10, 2) DEFAULT 0.00,
    current_bid DECIMAL(10, 2) DEFAULT NULL,
    bidder_id INT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    end_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP + INTERVAL '7 days',
    status VARCHAR(20) DEFAULT 'Active',
    CHECK (status IN ('Active', 'Completed', 'Canceled'))
);

CREATE INDEX idx_auctions_seller_id ON auctions(seller_id);
CREATE INDEX idx_auctions_bidder_id ON auctions(bidder_id);
CREATE INDEX idx_auctions_end_time ON auctions(end_time);
