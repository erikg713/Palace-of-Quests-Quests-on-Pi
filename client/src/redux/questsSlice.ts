import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from '../services/api';

export const fetchQuests = createAsyncThunk('quests/fetchQuests', async () => {
  const response = await axios.get('/quests');
  return response.data;
});

const questsSlice = createSlice({
  name: 'quests',
  initialState: { quests: [], loading: false, error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchQuests.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchQuests.fulfilled, (state, action) => {
        state.loading = false;
        state.quests = action.payload;
      })
      .addCase(fetchQuests.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default questsSlice.reducer;
