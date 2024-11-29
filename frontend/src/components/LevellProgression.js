import React from 'react';

const LevelProgression = ({ level, experience }) => {
  const maxExperience = 100; // Placeholder for level cap
  const progress = (experience / maxExperience) * 100;

  return (
    <div>
      <h2>Level {level}</h2>
      <div style={{ border: '1px solid black', width: '100%' }}>
        <div style={{ width: `${progress}%`, backgroundColor: 'green' }}>
          {progress}%
        </div>
      </div>
    </div>
  );
};

export default LevelProgression;