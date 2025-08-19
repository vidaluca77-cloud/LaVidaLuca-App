// src/store/selectors/joinSelectors.ts
import { RootState } from '../types';

// Join selectors
export const selectJoinState = (state: RootState) => state.join;
export const selectJoinFormData = (state: RootState) => state.join.formData;
export const selectJoinIsLoading = (state: RootState) => state.join.isLoading;
export const selectJoinError = (state: RootState) => state.join.error;
export const selectJoinSubmitted = (state: RootState) => state.join.submitted;
export const selectJoinLastFetch = (state: RootState) => state.join.lastFetch;