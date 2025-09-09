/**
 * Redux Store Configuration for Pocket Hedge Fund Mobile App
 * 
 * This file configures the Redux store with all slices,
 * middleware, and persistence settings.
 */

import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { combineReducers } from '@reduxjs/toolkit';

// Import slices
import authReducer from './authSlice';
import fundReducer from './fundSlice';
import portfolioReducer from './portfolioSlice';
import notificationReducer from './notificationSlice';
import appReducer from './appSlice';

// ============================================================================
// PERSIST CONFIGURATION
// ============================================================================

const persistConfig = {
  key: 'root',
  storage: AsyncStorage,
  whitelist: ['auth', 'app'], // Only persist auth and app state
  blacklist: ['fund', 'portfolio', 'notification'] // Don't persist frequently changing data
};

const authPersistConfig = {
  key: 'auth',
  storage: AsyncStorage,
  whitelist: ['user', 'isAuthenticated', 'biometricEnabled']
};

const appPersistConfig = {
  key: 'app',
  storage: AsyncStorage,
  whitelist: ['theme', 'language', 'notificationsEnabled', 'biometricEnabled']
};

// ============================================================================
// ROOT REDUCER
// ============================================================================

const rootReducer = combineReducers({
  auth: persistReducer(authPersistConfig, authReducer),
  fund: fundReducer,
  portfolio: portfolioReducer,
  notification: notificationReducer,
  app: persistReducer(appPersistConfig, appReducer)
});

const persistedReducer = persistReducer(persistConfig, rootReducer);

// ============================================================================
// STORE CONFIGURATION
// ============================================================================

export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
        ignoredPaths: ['_persist']
      }
    }),
  devTools: __DEV__
});

export const persistor = persistStore(store);

// ============================================================================
// TYPES
// ============================================================================

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// ============================================================================
// EXPORTS
// ============================================================================

export default store;
