import React from 'react';
import { useDispatch } from 'react-redux';
import { login, logout } from './authSlice';

function AuthButtons() {
  const dispatch = useDispatch();

  const handleLogin = () => {
    // Replace with actual login logic (e.g., API call)
    const userData = { id: 1, username: 'testuser' };
    const token = 'your_jwt_token';
    dispatch(login({ user: userData, token }));
  };

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <div>
      <button onClick={handleLogin}>Login</button>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default AuthButtons;
import { useDispatch } from "react-redux";
import { login, logout } from "./authSlice";

function LoginButton() {
  const dispatch = useDispatch();

  const handleLogin = () => {
    dispatch(
      login({
        user: { id: 1, username: "testuser", email: "test@example.com" },
        token: "some.jwt.token",
      })
    );
  };

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <div>
      <button onClick={handleLogin}>Login</button>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}
