import { createSlice } from '@reduxjs/toolkit';

export const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: null,
    token: null,
  },
  reducers: {
    // Using regular function syntax for consistency
    login(state, action) {
      state.user = action.payload.user;
      state.token = action.payload.token;
    },
    logout(state) {
      state.user = null;
      state.token = null;
    },
  },
});

// Export actions for use in components
export const { login, logout } = authSlice.actions;

// Export the reducer to be included in the store
export default authSlice.reducer;
