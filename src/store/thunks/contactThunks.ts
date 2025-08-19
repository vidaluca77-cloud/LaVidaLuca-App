// src/store/thunks/contactThunks.ts
import { createAsyncThunk } from '@reduxjs/toolkit';
import { ContactFormData, AsyncThunkConfig } from '../types';

export const submitContactForm = createAsyncThunk<
  void,
  ContactFormData,
  AsyncThunkConfig
>(
  'contact/submitForm',
  async (formData, { rejectWithValue }) => {
    try {
      // Get API URL from environment or use default
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      
      const response = await fetch(`${apiUrl}/api/contact`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `Erreur ${response.status}: ${response.statusText}`);
      }

      // Return void since we don't need the response data
      return;
    } catch (error) {
      if (error instanceof Error) {
        return rejectWithValue(error.message);
      }
      return rejectWithValue('Une erreur inattendue est survenue');
    }
  }
);