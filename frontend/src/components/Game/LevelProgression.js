// components/Game/LevelProgression.js
import React from 'react';

const LevelProgression = () => {
  return (
    <div>
      <h3>Level Progression</h3>
      <p>Next level in 100 XP</p>
      <div className="progress-bar">
        <div className="progress" style={{ width: '30%' }}></div>
      </div>
    </div>
  );
};

export default LevelProgression;
import React from 'react';

const LevelProgression = ({ currentXP, requiredXP }) => {
  const progress = (currentXP / requiredXP) * 100;

  return (
    <div className="progress-container">
      <h3>Level Progress</h3>
      <div className="progress-bar" style={{ width: `${progress}%` }} />
      <span>{currentXP} / {requiredXP} XP</span>
    </div>
  );
};

export default LevelProgression;