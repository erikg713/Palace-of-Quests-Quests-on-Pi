// UserProfile.tsx
import React from 'react';
import { useSelector } from 'react-redux';

// Define the shape of the user object
interface User {
  username?: string; // username is optional
}

// Define the Redux state structure
interface RootState {
  auth?: {
    user?: User;
  };
}

function UserProfile() {
  // Use Redux state with proper type
  const user = useSelector((state: RootState) => state.auth?.user);

  // Conditional rendering
  if (!user) {
    return <p>Please log in.</p>;
  }

  return <p>Welcome, {user.username || "Guest"}!</p>;
}

export default UserProfile;
