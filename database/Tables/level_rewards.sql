-- Drop the table if it already exists
DROP TABLE IF EXISTS level_rewards;

-- Create the table for level rewards
CREATE TABLE level_rewards (
    level_id INT PRIMARY KEY AUTO_INCREMENT,         -- Unique level identifier
    level_name VARCHAR(100) NOT NULL,                -- Name of the level
    reward_type VARCHAR(50) NOT NULL,                -- Type of reward (e.g., "Coins", "Item")
    reward_amount INT NOT NULL CHECK (reward_amount > 0),  -- Quantity must be greater than zero
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp of record creation
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Timestamp of last update
    CONSTRAINT reward_type_check CHECK (reward_type IN ('Coins', 'Item', 'Bonus', 'Gems')) -- Valid reward types
);

-- Insert initial data into level_rewards
INSERT INTO level_rewards (level_name, reward_type, reward_amount)
VALUES
    ('Level 1', 'Coins', 100),
    ('Level 2', 'Coins', 200),
    ('Level 3', 'Item', 1),
    ('Level 4', 'Gems', 50),
    ('Level 5', 'Bonus', 1);
DELIMITER $$

-- Stored Procedure to update reward details dynamically
CREATE PROCEDURE UpdateReward(
    IN level_id_input INT,             -- Input: Level ID to update
    IN new_reward_type VARCHAR(50),    -- Input: New reward type
    IN new_reward_amount INT           -- Input: New reward amount
)
BEGIN
    -- Check if the level exists
    IF NOT EXISTS (SELECT 1 FROM level_rewards WHERE level_id = level_id_input) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Level not found';
    END IF;

    -- Update the reward details
    UPDATE level_rewards
    SET reward_type = new_reward_type,
        reward_amount = new_reward_amount,
        updated_at = CURRENT_TIMESTAMP
    WHERE level_id = level_id_input;
END$$

DELIMITER ;
-- Drop the table if it exists
DROP TABLE IF EXISTS level_rewards_log;

-- Create a log table to track updates
CREATE TABLE level_rewards_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique log identifier
    level_id INT NOT NULL,                 -- Level that was updated
    old_reward_type VARCHAR(50),           -- Old reward type
    old_reward_amount INT,                 -- Old reward amount
    new_reward_type VARCHAR(50),           -- New reward type
    new_reward_amount INT,                 -- New reward amount
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of the update
);

-- Trigger to log updates on level_rewards
DELIMITER $$

CREATE TRIGGER LogLevelRewardUpdate
AFTER UPDATE ON level_rewards
FOR EACH ROW
BEGIN
    INSERT INTO level_rewards_log (level_id, old_reward_type, old_reward_amount, new_reward_type, new_reward_amount, updated_at)
    VALUES (OLD.level_id, OLD.reward_type, OLD.reward_amount, NEW.reward_type, NEW.reward_amount, NEW.updated_at);
END$$

DELIMITER ;
DELIMITER $$

CREATE PROCEDURE IncrementRewardsByType(
    IN reward_type_input VARCHAR(50),  -- Reward type to update
    IN increment_amount INT            -- Increment value
)
BEGIN
    -- Validate reward type
    IF NOT EXISTS (SELECT 1 FROM level_rewards WHERE reward_type = reward_type_input) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid reward type';
    END IF;

    -- Update rewards of the specified type
    UPDATE level_rewards
    SET reward_amount = reward_amount + increment_amount,
        updated_at = CURRENT_TIMESTAMP
    WHERE reward_type = reward_type_input;
SELECT * FROM reward_summary;
END$$

DELIMITER ;
CALL IncrementRewardsByType('Coins', 50);
SELECT * FROM level_rewards WHERE reward_type = 'Coins';
DELIMITER $$

CREATE PROCEDURE IncrementRewardsByPercentage(
    IN reward_type_input VARCHAR(50),  -- Reward type to update
    IN percentage FLOAT                -- Increment percentage
)
BEGIN
    -- Validate reward type
    IF NOT EXISTS (SELECT 1 FROM level_rewards WHERE reward_type = reward_type_input) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid reward type';
    END IF;

    -- Update rewards of the specified type
    UPDATE level_rewards
    SET reward_amount = reward_amount + (reward_amount * (percentage / 100)),
        updated_at = CURRENT_TIMESTAMP
    WHERE reward_type = reward_type_input;
END$$

DELIMITER ;
CALL IncrementRewardsByPercentage('Coins', 10); -- 10% increment
SELECT * FROM level_rewards WHERE reward_type = 'Coins';
-- Drop the view if it exists
DROP VIEW IF EXISTS reward_summary;

-- Create a view to aggregate rewards by type
CREATE VIEW reward_summary AS
SELECT
    reward_type,
    COUNT(level_id) AS number_of_levels,
    SUM(reward_amount) AS total_rewards,
    AVG(reward_amount) AS average_reward
FROM level_rewards
GROUP BY reward_type;
