import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  fetchUser,
  loginUser,
  logoutUser,
  updateUserProfile,
} from '../store/actions/authActions'; // Update the path as per your project structure
import { RootState } from '../store'; // Update the path as per your project structure

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
