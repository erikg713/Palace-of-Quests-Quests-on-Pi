import React, { useState, useEffect } from "react";
import axios from "axios";

const SkillUpgrade = ({ userId }) => {
  const [skills, setSkills] = useState([]);

  useEffect(() => {
    const fetchSkills = async () => {
      const { data } = await axios.get("/api/skills");
      setSkills(data);
    };
    fetchSkills();
  }, []);

  const handleUpgrade = async (skillId) => {
    try {
      const response = await axios.post(`/api/player/${userId}/skills/${skillId}/upgrade`, {
        coins_spent: 50,
        xp_used: 100,
      });
      alert(response.data.message);
    } catch (error) {
      console.error("Skill upgrade failed", error);
    }
  };

  return (
    <div>
      <h1>Upgrade Skills</h1>
      {skills.map((skill) => (
        <div key={skill.id}>
          <h3>{skill.skill_name}</h3>
          <p>{skill.description}</p>
          <button onClick={() => handleUpgrade(skill.id)}>Upgrade</button>
        </div>
      ))}
    </div>
  );
};

export default SkillUpgrade;
