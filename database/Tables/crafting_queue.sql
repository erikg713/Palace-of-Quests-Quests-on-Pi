-- Table: crafting_queue
-- Purpose: Tracks each user's active and completed crafting tasks

CREATE TABLE IF NOT EXISTS crafting_queue (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recipe_id INTEGER NOT NULL REFERENCES crafting_recipes(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'In Progress' CHECK (status IN ('In Progress', 'Completed')),
    started_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITHOUT TIME ZONE,
    CONSTRAINT uq_active_queue UNIQUE (user_id, recipe_id, status)
);

-- Indexes to speed up lookups by user and recipe
CREATE INDEX IF NOT EXISTS idx_crafting_queue_user_id ON crafting_queue(user_id);
CREATE INDEX IF NOT EXISTS idx_crafting_queue_recipe_id ON crafting_queue(recipe_id);

-- Optional: Add a comment for documentation purposes
COMMENT ON TABLE crafting_queue IS 'Tracks the crafting queue for users, including status and timestamps.';
COMMENT ON COLUMN crafting_queue.status IS 'Current state: In Progress or Completed.';
COMMENT ON COLUMN crafting_queue.completed_at IS 'NULL until crafting is completed.';

-- Optional: Add a trigger to automatically set completed_at when status changes to "Completed"
-- (Example provided for PostgreSQL)
-- CREATE OR REPLACE FUNCTION set_completed_at() RETURNS trigger AS $$
-- BEGIN
--     IF NEW.status = 'Completed' AND OLD.status <> 'Completed' THEN
--         NEW.completed_at := CURRENT_TIMESTAMP;
--     END IF;
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;
--
-- CREATE TRIGGER trg_set_completed_at
-- BEFORE UPDATE ON crafting_queue
-- FOR EACH ROW
-- WHEN (OLD.status IS DISTINCT FROM NEW.status)
-- EXECUTE FUNCTION set_completed_at();
