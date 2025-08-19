// src/store/selectors/contactSelectors.ts
import { RootState } from '../types';

// Contact selectors
export const selectContactState = (state: RootState) => state.contact;
export const selectContactFormData = (state: RootState) => state.contact.formData;
export const selectContactIsLoading = (state: RootState) => state.contact.isLoading;
export const selectContactError = (state: RootState) => state.contact.error;
export const selectContactSubmitted = (state: RootState) => state.contact.submitted;
export const selectContactLastFetch = (state: RootState) => state.contact.lastFetch;