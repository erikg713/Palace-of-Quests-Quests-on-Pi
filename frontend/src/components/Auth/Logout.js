// components/Auth/Logout.js
import React from 'react';

const Logout = () => {
  const handleLogout = () => {
    // Add logout logic here (e.g., clear session, JWT, etc.)
    console.log('Logging out');
  };

  return (
    <button onClick={handleLogout}>Logout</button>
  );
};

export default Logout;