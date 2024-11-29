CREATE TABLE seasons (
    id SERIAL PRIMARY KEY,
    season_name VARCHAR(100) UNIQUE NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    description TEXT
);
