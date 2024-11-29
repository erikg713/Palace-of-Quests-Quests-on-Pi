import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  fetchUser,
  loginUser,
  logoutUser,
  updateUserProfile,
  RootState,
} from './store';

function UserProfile() {
  const dispatch = useDispatch();

  // Selectors for state
  const user = useSelector((state: RootState) => state.auth.user);
  const loading = useSelector((state: RootState) => state.auth.loading);
  const error = useSelector((state: RootState) => state.auth.error);

  // Fetch user on component mount
  useEffect(() => {
    dispatch(fetchUser());
  }, [dispatch]);

  // Handlers for user actions
  const handleLogin = () => {
    dispatch(loginUser({ username: 'testuser', password: 'password123' }));
  };

  const handleLogout = () => {
    dispatch(logoutUser());
  };

  const handleProfileUpdate = () => {
    dispatch(updateUserProfile({ username: 'newusername' }));
  };

  // Conditional rendering for state
  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
    <div>
      {user ? (
        <>
          <p>Welcome, {user.username || 'Guest'}!</p>
          <button onClick={handleLogout}>Logout</button>
          <button onClick={handleProfileUpdate}>Update Profile</button>
        </>
      ) : (
        <>
          <p>Please log in.</p>
          <button onClick={handleLogin}>Login</button>
        </>
      )}
    </div>
  );
}

export default UserProfile;
