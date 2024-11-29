import React, { useState, useEffect } from "react";
import { getQuests, completeQuest } from "../api/questAPI";

const Quest = () => {
  const [quests, setQuests] = useState([]);

  useEffect(() => {
    const fetchQuests = async () => {
      const data = await getQuests();
      setQuests(data);
    };
    fetchQuests();
  }, []);

  const handleCompleteQuest = async (questId) => {
    const updatedQuest = await completeQuest(questId);
    setQuests(quests.map(q => (q.id === questId ? updatedQuest : q)));
  };

  return (
    <div>
      <h2>Available Quests</h2>
      <ul>
        {quests.map(quest => (
          <li key={quest.id}>
            <h3>{quest.name}</h3>
            <p>Difficulty: {quest.difficulty}</p>
            <p>{quest.isCompleted ? "Completed" : "Not completed"}</p>
            {!quest.isCompleted && (
              <button onClick={() => handleCompleteQuest(quest.id)}>
                Complete Quest
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Quest;

import React, { useState, useEffect } from "react";
import { getQuests, completeQuest } from "../api/questAPI";

const Quest = () => {
  const [quests, setQuests] = useState([]);

  useEffect(() => {
    const fetchQuests = async () => {
      const data = await getQuests();
      setQuests(data);
    };
    fetchQuests();
  }, []);

  const handleCompleteQuest = async (questId) => {
    const updatedQuest = await completeQuest(questId);
    setQuests(quests.map(q => (q.id === questId ? updatedQuest : q)));
  };

  return (
    <div className="container">
      <h2>Available Quests</h2>
      <ul>
        {quests.map(quest => (
          <li key={quest.id}>
            <h3>{quest.name}</h3>
            <p>Difficulty: {quest.difficulty}</p>
            <p>{quest.isCompleted ? "Completed" : "Not completed"}</p>
            {!quest.isCompleted && (
              <button onClick={() => handleCompleteQuest(quest.id)}>
                Complete Quest
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Quest;
