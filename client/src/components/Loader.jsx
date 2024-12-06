import React from 'react';
import './Loader.css'; // Assuming a CSS file for styling

const Loader = ({ size = '50px', color = '#4caf50' }) => {
  return (
    <div
      className="loader"
      style={{
        width: size,
        height: size,
        borderColor: `${color} transparent ${color} transparent`,
      }}
    />
  );
};

export default Loader;
