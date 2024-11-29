import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  fetchUser,
  loginUser,
  logoutUser,
  updateUserProfile,
  RootState,
} from '../store';

export const useAuth = () => {
  const dispatch = useDispatch();

  // State selectors
  const user = useSelector((state: RootState) => state.auth.user);
  const loading = useSelector((state: RootState) => state.auth.loading);
  const error = useSelector((state: RootState) => state.auth.error);

  // Fetch user on mount
  useEffect(() => {
    dispatch(fetchUser());
  }, [dispatch]);

  // Action dispatchers
  const login = (username: string, password: string) => {
    dispatch(loginUser({ username, password }));
  };

  const logout = () => {
    dispatch(logoutUser());
  };

  const updateProfile = (updatedData: { username?: string }) => {
    dispatch(updateUserProfile(updatedData));
  };

  return {
    user,
    loading,
    error,
    login,
    logout,
    updateProfile,
  };
};
import { useState, useEffect } from "react";

const useAuth = () => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const fetchUser = async () => {
            const token = localStorage.getItem("authToken");
            if (token) {
                // Simulate API call to fetch user details
                const userDetails = await fetch("/api/user", {
                    headers: { Authorization: `Bearer ${token}` },
                }).then((res) => res.json());
                setUser(userDetails);
            }
        };
        fetchUser();
    }, []);

    return user;
};

export default useAuth;
