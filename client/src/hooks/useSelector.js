import React from 'react';
import { useSelector } from 'react-redux';

function UserProfile() {
  const user = useSelector((state) => state.auth?.user); // Safe optional chaining to avoid errors

  if (!user) {
    return <p>Please log in.</p>;
  }

  return <p>Welcome, {user.username || "Guest"}!</p>; // Fallback in case username is undefined
}

export default UserProfile;
