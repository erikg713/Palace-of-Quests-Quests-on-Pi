-- Create the challenges table to store available challenges
CREATE TABLE challenges (
    challenge_id SERIAL PRIMARY KEY,
    challenge_name VARCHAR(100) NOT NULL,
    description TEXT,
    total_steps INT NOT NULL, -- Total steps required to complete the challenge
    reward DECIMAL(10, 2), -- Reward for completing the challenge
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the challenges_progress table to track user progress
CREATE TABLE challenges_progress (
    progress_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL, -- Reference to the user
    challenge_id INT NOT NULL, -- Reference to the challenge
    current_step INT DEFAULT 0, -- Steps completed so far
    is_completed BOOLEAN DEFAULT FALSE, -- Whether the challenge is completed
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (challenge_id) REFERENCES challenges(challenge_id)
);
INSERT INTO challenges_progress (user_id, challenge_id, current_step, is_completed)
VALUES
    (1, 1, 20, FALSE), -- User 1 has completed 20 sword swings out of 100
    (2, 2, 50, TRUE);  -- User 2 has completed the shield mastery challenge
