import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import axios from '../services/api';

// --- Types ---
interface Quest {
  id: number;
  name: string;
  description: string;
  // Add other quest properties as needed
}

interface QuestsState {
  quests: Quest[];
  loading: boolean;
  error: string | null;
}

// --- Initial State ---
const initialState: QuestsState = {
  quests: [],
  loading: false,
  error: null,
};

// --- Async Thunks ---
export const fetchQuests = createAsyncThunk<Quest[], void, { rejectValue: string }>(
  'quests/fetchQuests',
  async (_, { rejectWithValue }) => {
    try {
      const { data } = await axios.get<Quest[]>('/quests');
      return data;
    } catch (err: any) {
      // You may want to log the error here for debugging
      return rejectWithValue(
        err?.response?.data?.message || 'Failed to fetch quests. Please try again.'
      );
    }
  }
);

// --- Slice ---
const questsSlice = createSlice({
  name: 'quests',
  initialState,
  reducers: {
    resetQuestsState: () => initialState,
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchQuests.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchQuests.fulfilled, (state, action: PayloadAction<Quest[]>) => {
        state.loading = false;
        state.quests = action.payload;
      })
      .addCase(fetchQuests.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || 'Unknown error';
      });
  },
});

// --- Exports ---
export const { resetQuestsState } = questsSlice.actions;
export default questsSlice.reducer;
