// src/store/selectors/uiSelectors.ts
import { RootState } from '../types';

// UI selectors
export const selectUIState = (state: RootState) => state.ui;
export const selectSidebarOpen = (state: RootState) => state.ui.sidebarOpen;
export const selectModalOpen = (state: RootState) => state.ui.modalOpen;
export const selectNotifications = (state: RootState) => state.ui.notifications;
export const selectHasNotifications = (state: RootState) => state.ui.notifications.length > 0;