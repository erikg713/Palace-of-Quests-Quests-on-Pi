import React, { useState, useEffect } from "react";
import { getLevelRewards, upgradeLevel } from "../api/levelAPI";

const LevelUp = ({ currentLevel }) => {
  const [levelRewards, setLevelRewards] = useState(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchRewards = async () => {
      const rewards = await getLevelRewards(currentLevel);
      setLevelRewards(rewards);
    };
    fetchRewards();
  }, [currentLevel]);

  const handleUpgrade = async () => {
    const result = await upgradeLevel();
    if (result.error) {
      setMessage(result.error);
    } else {
      setMessage(`Level Up! You are now level ${result.reward.level}.`);
      setLevelRewards(result.reward);
    }
  };

  return (
    <div>
      <h2>Level: {currentLevel}</h2>
      {levelRewards ? (
        <div>
          <h3>Rewards for Level {currentLevel}</h3>
          <p>{levelRewards.reward_name}: {levelRewards.reward_description}</p>
          <p>Stat Boost: +{levelRewards.stat_boost}</p>
          <button onClick={handleUpgrade}>Upgrade to Level {currentLevel + 1}</button>
        </div>
      ) : (
        <p>No rewards available for this level.</p>
      )}
      {message && <p>{message}</p>}
    </div>
  );
};

export default LevelUp;
