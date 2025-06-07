-- Table: friends
-- Purpose: Represents user friendship relationships and statuses.

CREATE TABLE friends (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    friend_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(16) NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Accepted', 'Blocked')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_friend_pair UNIQUE (user_id, friend_id),
    CONSTRAINT chk_no_self_friend CHECK (user_id <> friend_id)
);

CREATE INDEX idx_friends_user_id ON friends(user_id);
CREATE INDEX idx_friends_friend_id ON friends(friend_id);

-- Keeps updated_at current on any row update (PostgreSQL)
CREATE OR REPLACE FUNCTION set_friends_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_friends_updated_at ON friends;

CREATE TRIGGER trg_friends_updated_at
BEFORE UPDATE ON friends
FOR EACH ROW
EXECUTE FUNCTION set_friends_updated_at();
