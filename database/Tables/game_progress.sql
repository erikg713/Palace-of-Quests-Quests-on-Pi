-- Table to track each user's progress through game levels.
CREATE TABLE game_progress (
    progress_id SERIAL PRIMARY KEY, -- Unique row identifier
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE, -- References users table
    level_number INTEGER NOT NULL CHECK (level_number > 0), -- Only allow positive level numbers
    completed_at TIMESTAMPTZ NOT NULL DEFAULT NOW() -- Completion timestamp with timezone
);

-- Index to quickly find all progress for a user
CREATE INDEX IF NOT EXISTS idx_game_progress_user_id ON game_progress(user_id);

-- Optional: Index for level-based analytics or reporting
CREATE INDEX IF NOT EXISTS idx_game_progress_level_number ON game_progress(level_number);
