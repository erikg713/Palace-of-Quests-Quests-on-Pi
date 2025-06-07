import { configureStore } from "@reduxjs/toolkit";
import { createLogger } from 'redux-logger';
import authReducer from "./slices/authSlice";
import questsReducer from "./slices/questsSlice";
import uiReducer from "./slices/uiSlice";

// Configure middleware based on environment
const middleware = [];

// Only add logger in development
if (process.env.NODE_ENV === 'development') {
  const logger = createLogger({
    collapsed: true,
    duration: true,
  });
  middleware.push(logger);
}

/**
 * Redux store configuration for Palace of Quests application.
 * Combines multiple reducers and configures middleware.
 */
const store = configureStore({
  reducer: {
    auth: authReducer,
    quests: questsReducer,
    ui: uiReducer,
  },
  middleware: (getDefaultMiddleware) => 
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore specific paths for non-serializable values if needed
        ignoredActions: ['auth/loginSuccess'],
        ignoredPaths: ['auth.userData.createdAt'],
      },
    }).concat(middleware),
  devTools: process.env.NODE_ENV !== 'production',
});

export default store;

// Useful types for components and hooks
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
