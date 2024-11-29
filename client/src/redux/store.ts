import { configureStore, createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { createLogger } from 'redux-logger';

// Define the shape of the user data
interface User {
  username?: string;
}

// Define the shape of the state
interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
}

// Initial state
const initialState: AuthState = {
  user: null,
  loading: false,
  error: null,
};

// Thunk for fetching user data from an API
export const fetchUser = createAsyncThunk('auth/fetchUser', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('https://api.example.com/user');
    if (!response.ok) throw new Error('Failed to fetch user data');
    return await response.json(); // Assumes the API returns a user object
  } catch (error: any) {
    return rejectWithValue(error.message);
  }
});

// Auth slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout(state) {
      state.user = null;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload;
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

// Export actions
export const { logout } = authSlice.actions;

// Configure the store
const logger = createLogger();

const store = configureStore({
  reducer: {
    auth: authSlice.reducer,
  },
  middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(logger),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;
