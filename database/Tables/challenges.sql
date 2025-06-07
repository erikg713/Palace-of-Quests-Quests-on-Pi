-- ============================================================================
-- Table: challenges
-- Purpose: Stores quest challenges for the Palace of Quests metaverse game.
-- Author: erikg713
-- Last Updated: 2025-06-07
-- ============================================================================

CREATE TABLE IF NOT EXISTS challenges (
    id               SERIAL PRIMARY KEY,                              -- Unique challenge ID
    challenge_name   VARCHAR(100) NOT NULL UNIQUE,                    -- Unique name for the challenge
    description      TEXT NOT NULL,                                   -- Description of the challenge
    xp_reward        INTEGER NOT NULL CHECK (xp_reward >= 0),         -- Experience points awarded
    coin_reward      NUMERIC(12, 2) NOT NULL DEFAULT 0.00 CHECK (coin_reward >= 0), -- In-game currency reward
    difficulty_level SMALLINT NOT NULL CHECK (difficulty_level BETWEEN 1 AND 10),   -- 1-10 scale
    is_active        BOOLEAN NOT NULL DEFAULT TRUE,                   -- To enable/disable challenges
    created_at       TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,   -- Creation timestamp
    updated_at       TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,   -- Last update timestamp

    -- Index for faster lookups by difficulty and activity status
    INDEX idx_challenges_difficulty_active (difficulty_level, is_active)
);

-- Trigger to auto-update 'updated_at' column
CREATE OR REPLACE FUNCTION update_challenges_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_update_challenges_updated_at ON challenges;
CREATE TRIGGER trg_update_challenges_updated_at
BEFORE UPDATE ON challenges
FOR EACH ROW
EXECUTE FUNCTION update_challenges_updated_at();

-- ============================================================================
-- Seed data for development/testing
-- ============================================================================

INSERT INTO challenges (challenge_name, description, xp_reward, coin_reward, difficulty_level)
VALUES
    ('Sword Training',   'Complete 100 sword swings.',        100,  500.00, 5),
    ('Shield Mastery',   'Block 50 attacks.',                 50,   300.00, 4),
    ('Archery Practice', 'Hit 20 bullseyes.',                 200,  750.00, 6),
    ('Puzzle Solver',    'Solve 5 complex puzzles.',          150,  600.00, 7),
    ('Dungeon Explorer', 'Clear a dungeon without taking damage.', 300, 1200.00, 9)
ON CONFLICT (challenge_name) DO NOTHING;

-- ============================================================================
-- Notes:
-- - Adjust the structure as your game logic evolves.
-- - Consider moving rewards or difficulty levels to reference/lookup tables if they become more complex.
-- - Use is_active instead of deleting challenges for better auditability.
-- ============================================================================
