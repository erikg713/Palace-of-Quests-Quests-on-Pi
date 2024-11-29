import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice'; // Adjust the path as necessary

const store = configureStore({
  reducer: {
    auth: authReducer,
    // Include other reducers if you have them
  },
});

export default store;
