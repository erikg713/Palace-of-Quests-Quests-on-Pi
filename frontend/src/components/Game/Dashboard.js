// components/Game/Dashboard.js
import React from 'react';

const Dashboard = () => {
  return (
    <div>
      <h2>Player Dashboard</h2>
      <p>Level: 1</p>
      <p>Experience: 0 XP</p>
      <p>Pi Wallet Balance: 100 Pi</p>
      <p>Avatar: (Placeholder Image)</p>
    </div>
  );
};

export default Dashboard;
import React, { useEffect, useState } from 'react';
import { getPlayerData } from '../../services/api';

const Dashboard = () => {
  const [playerData, setPlayerData] = useState(null);

  useEffect(() => {
    const fetchPlayerData = async () => {
      const data = await getPlayerData();
      setPlayerData(data);
    };

    fetchPlayerData();
  }, []);

  if (!playerData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="dashboard">
      <h2>Welcome, {playerData.username}!</h2>
      <p>Level: {playerData.level}</p>
      <p>XP: {playerData.xp}</p>
      <p>Pi Wallet: {playerData.piBalance} Pi</p>
    </div>
  );
};

export default Dashboard;