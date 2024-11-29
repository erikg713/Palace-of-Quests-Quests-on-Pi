import React, { useState, useEffect } from "react";
import { getAchievements } from "../api/achievementAPI";

const Achievements = () => {
  const [achievements, setAchievements] = useState([]);

  useEffect(() => {
    const fetchAchievements = async () => {
      const data = await getAchievements();
      setAchievements(data);
    };
    fetchAchievements();
  }, []);

  return (
    <div className="container">
      <h2>Achievements</h2>
      <ul>
        {achievements.map(achievement => (
          <li key={achievement.id} className={achievement.unlocked ? "completed" : ""}>
            <h3>{achievement.name}</h3>
            <p>{achievement.description}</p>
            {achievement.unlocked && <span>&#x2713;</span>}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Achievements;
