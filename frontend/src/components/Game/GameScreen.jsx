import React, { useEffect, useState } from 'react';
import { getPlayerStats } from '../../api/api';

const GameScreen = () => {
  const [stats, setStats] = useState({});

  useEffect(() => {
    const fetchStats = async () => {
      const userId = 1; // Example: Replace with actual logged-in user ID
      const { data } = await getPlayerStats(userId);
      setStats(data);
    };
    fetchStats();
  }, []);

  return (
    <div>
      <h1>Welcome to Palace of Quests</h1>
      <h2>Level: {stats.level}</h2>
      <h2>XP: {stats.xp}</h2>
    </div>
  );
};

export default GameScreen;
