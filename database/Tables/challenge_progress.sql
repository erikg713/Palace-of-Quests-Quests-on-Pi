-- Create the challenges table to store available challenges
CREATE TABLE challenges (
    challenge_id SERIAL PRIMARY KEY, -- Unique identifier for the challenge
    challenge_name VARCHAR(100) NOT NULL, -- Name of the challenge
    description TEXT, -- Detailed description of the challenge
    total_steps INT NOT NULL CHECK (total_steps > 0), -- Total steps required to complete the challenge
    reward DECIMAL(10, 2) DEFAULT 0 CHECK (reward >= 0), -- Reward for completing the challenge, must be non-negative
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp when the challenge was created
);

-- Create the challenges_progress table to track user progress
CREATE TABLE challenges_progress (
    progress_id SERIAL PRIMARY KEY, -- Unique identifier for the progress record
    user_id INT NOT NULL, -- Reference to the user (add foreign key if users table exists)
    challenge_id INT NOT NULL, -- Reference to the challenge
    current_step INT DEFAULT 0 CHECK (current_step >= 0), -- Steps completed so far, must be non-negative
    is_completed BOOLEAN DEFAULT FALSE, -- Whether the challenge is completed
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Last update timestamp
    FOREIGN KEY (challenge_id) REFERENCES challenges(challenge_id) ON DELETE CASCADE -- Delete progress if challenge is deleted
);

-- Add indexes for better query performance
CREATE INDEX idx_challenges_progress_user_id ON challenges_progress(user_id);
CREATE INDEX idx_challenges_progress_challenge_id ON challenges_progress(challenge_id);

-- Insert sample data into challenges_progress table
INSERT INTO challenges_progress (user_id, challenge_id, current_step, is_completed)
VALUES
    (1, 1, 20, FALSE), -- User 1 has completed 20 steps of the challenge
    (2, 2, 50, TRUE);  -- User 2 has completed the challenge
