import { createSlice } from '@reduxjs/toolkit';

// Exporting authSlice for potential use elsewhere
export const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: null,
    token: null,
  },
  reducers: {
    // Using function declarations
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

// Exporting actions
export const { login, logout } = authSlice.actions;

// Exporting reducer as default export
export default authSlice.reducer;
