import React, { useEffect, useState } from 'react';
import './Dashboard.css';

const Dashboard = () => {
  const [userStats, setUserStats] = useState({});
  const [quests, setQuests] = useState([]);

  useEffect(() => {
    // Fetch user stats and quests from the backend
    fetch('/api/user-stats')
      .then((res) => res.json())
      .then((data) => setUserStats(data));

    fetch('/api/quests')
      .then((res) => res.json())
      .then((data) => setQuests(data));
  }, []);

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Welcome to the Palace of Quests</h1>
        <p>Level: {userStats.level || 'Loading...'}</p>
        <p>Experience Points: {userStats.xp || 'Loading...'}</p>
      </header>

      <main className="dashboard-main">
        <section className="quests-section">
          <h2>Your Active Quests</h2>
          <ul className="quests-list">
            {quests.length > 0 ? (
              quests.map((quest, index) => (
                <li key={index} className="quest-item">
                  <h3>{quest.title}</h3>
                  <p>{quest.description}</p>
                  <p>Status: {quest.status}</p>
                </li>
              ))
            ) : (
              <p>Loading quests...</p>
            )}
          </ul>
        </section>

        <section className="actions-section">
          <h2>Actions</h2>
          <button className="action-btn">Start New Quest</button>
          <button className="action-btn">Upgrade Avatar</button>
        </section>
      </main>
    </div>
  );
};

export default Dashboard;

import React, { useEffect, useState } from 'react';
import QuestProgress from '../components/QuestProgress';
import axios from '../services/api';

const Dashboard = () => {
  const [quests, setQuests] = useState([]);

  useEffect(() => {
    axios.get('/quests').then((res) => setQuests(res.data));
  }, []);

  return (
    <div>
      <h1>Your Quests</h1>
      {quests.map((quest) => (
        <div key={quest.id}>
          <h2>{quest.title}</h2>
          <QuestProgress progress={quest.progress} />
        </div>
      ))}
    </div>
  );
};

export default Dashboard;
