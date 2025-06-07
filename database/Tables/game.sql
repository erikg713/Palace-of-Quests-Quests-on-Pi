-- Table: game_progress
-- Purpose: Records each user's progress per level, including completion timestamp.
-- Last updated: 2025-06-07

CREATE TABLE IF NOT EXISTS game_progress (
    progress_id SERIAL PRIMARY KEY,                              -- Unique row ID
    user_id INTEGER NOT NULL REFERENCES users(user_id) 
        ON DELETE CASCADE,                                       -- User account reference
    level_number INTEGER NOT NULL CHECK (level_number > 0),      -- Level must be positive
    completed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,   -- When the level was completed
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,     -- When record was created
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP      -- When record was last updated
);

-- Indexes for performance on common queries
CREATE INDEX IF NOT EXISTS idx_game_progress_user_id ON game_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_game_progress_level_number ON game_progress(level_number);

-- Trigger to automatically update updated_at on row changes
CREATE OR REPLACE FUNCTION update_game_progress_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_update_game_progress_updated_at ON game_progress;
CREATE TRIGGER trg_update_game_progress_updated_at
BEFORE UPDATE ON game_progress
FOR EACH ROW
EXECUTE FUNCTION update_game_progress_updated_at();

-- Optional: Comment on table and columns for database documentation
COMMENT ON TABLE game_progress IS 'Tracks each user''s progress through game levels.';
COMMENT ON COLUMN game_progress.progress_id IS 'Primary key for the progress record.';
COMMENT ON COLUMN game_progress.user_id IS 'Foreign key to users(user_id).';
COMMENT ON COLUMN game_progress.level_number IS 'Current level completed by the user.';
COMMENT ON COLUMN game_progress.completed_at IS 'Timestamp when the level was completed.';
COMMENT ON COLUMN game_progress.created_at IS 'Record creation timestamp.';
COMMENT ON COLUMN game_progress.updated_at IS 'Record last update timestamp.';
