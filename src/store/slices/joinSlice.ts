// src/store/slices/joinSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { JoinState, JoinFormData } from '../types';
import { submitJoinForm } from '../thunks/joinThunks';

const initialState: JoinState = {
  isLoading: false,
  error: null,
  lastFetch: null,
  formData: {
    name: '',
    email: '',
    phone: '',
    motivation: ''
  },
  submitted: false
};

const joinSlice = createSlice({
  name: 'join',
  initialState,
  reducers: {
    updateFormData: (state, action: PayloadAction<Partial<JoinFormData>>) => {
      state.formData = { ...state.formData, ...action.payload };
    },
    resetForm: (state) => {
      state.formData = initialState.formData;
      state.submitted = false;
      state.error = null;
    },
    clearError: (state) => {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(submitJoinForm.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(submitJoinForm.fulfilled, (state) => {
        state.isLoading = false;
        state.submitted = true;
        state.lastFetch = Date.now();
        // Reset form data after successful submission
        state.formData = initialState.formData;
      })
      .addCase(submitJoinForm.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Une erreur est survenue';
      });
  }
});

export const {
  updateFormData,
  resetForm,
  clearError
} = joinSlice.actions;

export default joinSlice.reducer;