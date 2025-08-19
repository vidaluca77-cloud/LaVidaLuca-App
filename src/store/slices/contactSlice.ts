// src/store/slices/contactSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { ContactState, ContactFormData } from '../types';
import { submitContactForm } from '../thunks/contactThunks';

const initialState: ContactState = {
  isLoading: false,
  error: null,
  lastFetch: null,
  formData: {
    name: '',
    email: '',
    message: ''
  },
  submitted: false
};

const contactSlice = createSlice({
  name: 'contact',
  initialState,
  reducers: {
    updateFormData: (state, action: PayloadAction<Partial<ContactFormData>>) => {
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
      .addCase(submitContactForm.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(submitContactForm.fulfilled, (state) => {
        state.isLoading = false;
        state.submitted = true;
        state.lastFetch = Date.now();
        // Reset form data after successful submission
        state.formData = initialState.formData;
      })
      .addCase(submitContactForm.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Une erreur est survenue';
      });
  }
});

export const {
  updateFormData,
  resetForm,
  clearError
} = contactSlice.actions;

export default contactSlice.reducer;