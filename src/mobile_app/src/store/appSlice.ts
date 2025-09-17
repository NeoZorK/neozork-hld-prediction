/**
 * Redux slice for app-wide state management
 * 
 * This slice handles theme, language, settings,
 * and other app-wide configurations.
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AppState } from '../types';

// ============================================================================
// INITIAL STATE
// ============================================================================

const initialState: AppState = {
  theme: 'light',
  language: 'en',
  notificationsEnabled: true,
  biometricEnabled: false,
  offlineMode: false
};

// ============================================================================
// APP SLICE
// ============================================================================

const appSlice = createSlice({
  name: 'app',
  initialState,
  reducers: {
    setTheme: (state, action: PayloadAction<'light' | 'dark' | 'auto'>) => {
      state.theme = action.payload;
    },
    setLanguage: (state, action: PayloadAction<string>) => {
      state.language = action.payload;
    },
    setNotificationsEnabled: (state, action: PayloadAction<boolean>) => {
      state.notificationsEnabled = action.payload;
    },
    setBiometricEnabled: (state, action: PayloadAction<boolean>) => {
      state.biometricEnabled = action.payload;
    },
    setOfflineMode: (state, action: PayloadAction<boolean>) => {
      state.offlineMode = action.payload;
    },
    resetAppSettings: (state) => {
      state.theme = 'light';
      state.language = 'en';
      state.notificationsEnabled = true;
      state.biometricEnabled = false;
      state.offlineMode = false;
    }
  }
});

// ============================================================================
// SELECTORS
// ============================================================================

export const selectApp = (state: { app: AppState }) => state.app;
export const selectTheme = (state: { app: AppState }) => state.app.theme;
export const selectLanguage = (state: { app: AppState }) => state.app.language;
export const selectNotificationsEnabled = (state: { app: AppState }) => state.app.notificationsEnabled;
export const selectBiometricEnabled = (state: { app: AppState }) => state.app.biometricEnabled;
export const selectOfflineMode = (state: { app: AppState }) => state.app.offlineMode;

// ============================================================================
// EXPORTS
// ============================================================================

export const { 
  setTheme, 
  setLanguage, 
  setNotificationsEnabled, 
  setBiometricEnabled, 
  setOfflineMode, 
  resetAppSettings 
} = appSlice.actions;

export default appSlice.reducer;
