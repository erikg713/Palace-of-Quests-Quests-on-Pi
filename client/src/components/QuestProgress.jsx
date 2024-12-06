import React from 'react';

const QuestProgress = ({ progress }) => {
  return (
    <div>
      <div style={{ width: '100%', backgroundColor: '#ddd', height: '20px', borderRadius: '5px' }}>
        <div
          style={{
            width: `${progress}%`,
            backgroundColor: progress === 100 ? '#4caf50' : '#2196f3',
            height: '100%',
            borderRadius: '5px',
          }}
        />
      </div>
      <p>{progress}% completed</p>
    </div>
  );
};

export default QuestProgress;
