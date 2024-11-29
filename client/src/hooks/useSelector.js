import React from 'react';
import { useSelector } from 'react-redux';

function UserProfile() {
  const user = useSelector((state) => state.auth.user);

  if (!user) {
    return <p>Please log in.</p>;
  }

  return <p>Welcome, {user.username}!</p>;
}

export default UserProfile;
import { useSelector } from "react-redux";

function UserProfile() {
  const user = useSelector((state) => state.auth.user);

  return <div>{user ? `Hello, ${user.username}` : "Not logged in"}</div>;
}
