/**
 * Redux slice for authentication state management
 * 
 * This slice handles user authentication, login/logout,
 * and biometric authentication state.
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { User, LoginRequest, RegisterRequest, AuthState, ApiError } from '../types';
import { authAPI } from '../services/api';

// ============================================================================
// ASYNC THUNKS
// ============================================================================

export const loginUser = createAsyncThunk(
  'auth/login',
  async (credentials: LoginRequest, { rejectWithValue }) => {
    try {
      const response = await authAPI.login(credentials);
      return response;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Login failed',
        code: 500
      });
    }
  }
);

export const registerUser = createAsyncThunk(
  'auth/register',
  async (userData: RegisterRequest, { rejectWithValue }) => {
    try {
      const response = await authAPI.register(userData);
      return response.data;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Registration failed',
        code: 500
      });
    }
  }
);

export const logoutUser = createAsyncThunk(
  'auth/logout',
  async (_, { rejectWithValue }) => {
    try {
      await authAPI.logout();
      return true;
    } catch (error) {
      // Even if logout fails on server, clear local state
      console.warn('Logout error:', error);
      return true;
    }
  }
);

export const refreshToken = createAsyncThunk(
  'auth/refreshToken',
  async (_, { rejectWithValue }) => {
    try {
      const response = await authAPI.refreshToken();
      return response;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code
        });
      }
      return rejectWithValue({
        message: 'Token refresh failed',
        code: 500
      });
    }
  }
);

export const getCurrentUser = createAsyncThunk(
  'auth/getCurrentUser',
  async (_, { rejectWithValue }) => {
    try {
      const user = await authAPI.getCurrentUser();
      return user;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code
        });
      }
      return rejectWithValue({
        message: 'Failed to get user',
        code: 500
      });
    }
  }
);

export const updateProfile = createAsyncThunk(
  'auth/updateProfile',
  async (userData: Partial<User>, { rejectWithValue }) => {
    try {
      const user = await authAPI.updateProfile(userData);
      return user;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code
        });
      }
      return rejectWithValue({
        message: 'Profile update failed',
        code: 500
      });
    }
  }
);

export const enableBiometric = createAsyncThunk(
  'auth/enableBiometric',
  async (_, { rejectWithValue }) => {
    try {
      await authAPI.enableBiometric({
        platform: 'ios', // This should be determined dynamically
        version: '1.0.0',
        device_id: 'device-id',
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        language: 'en'
      });
      return true;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code
        });
      }
      return rejectWithValue({
        message: 'Biometric enable failed',
        code: 500
      });
    }
  }
);

export const disableBiometric = createAsyncThunk(
  'auth/disableBiometric',
  async (_, { rejectWithValue }) => {
    try {
      await authAPI.disableBiometric();
      return true;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code
        });
      }
      return rejectWithValue({
        message: 'Biometric disable failed',
        code: 500
      });
    }
  }
);

// ============================================================================
// INITIAL STATE
// ============================================================================

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
  biometricEnabled: false
};

// ============================================================================
// AUTH SLICE
// ============================================================================

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setBiometricEnabled: (state, action: PayloadAction<boolean>) => {
      state.biometricEnabled = action.payload;
    },
    setUser: (state, action: PayloadAction<User | null>) => {
      state.user = action.payload;
      state.isAuthenticated = !!action.payload;
    },
    logout: (state) => {
      state.user = null;
      state.isAuthenticated = false;
      state.error = null;
      state.biometricEnabled = false;
    }
  },
  extraReducers: (builder) => {
    // Login
    builder
      .addCase(loginUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload.user;
        state.isAuthenticated = true;
        state.error = null;
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Login failed';
        state.isAuthenticated = false;
        state.user = null;
      });

    // Register
    builder
      .addCase(registerUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(registerUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload;
        state.isAuthenticated = true;
        state.error = null;
      })
      .addCase(registerUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Registration failed';
        state.isAuthenticated = false;
        state.user = null;
      });

    // Logout
    builder
      .addCase(logoutUser.fulfilled, (state) => {
        state.user = null;
        state.isAuthenticated = false;
        state.error = null;
        state.biometricEnabled = false;
        state.isLoading = false;
      });

    // Refresh Token
    builder
      .addCase(refreshToken.fulfilled, (state, action) => {
        state.user = action.payload.user;
        state.isAuthenticated = true;
        state.error = null;
      })
      .addCase(refreshToken.rejected, (state, action) => {
        state.user = null;
        state.isAuthenticated = false;
        state.error = action.payload?.message || 'Token refresh failed';
      });

    // Get Current User
    builder
      .addCase(getCurrentUser.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(getCurrentUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload;
        state.isAuthenticated = true;
        state.error = null;
      })
      .addCase(getCurrentUser.rejected, (state, action) => {
        state.isLoading = false;
        state.user = null;
        state.isAuthenticated = false;
        state.error = action.payload?.message || 'Failed to get user';
      });

    // Update Profile
    builder
      .addCase(updateProfile.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateProfile.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload;
        state.error = null;
      })
      .addCase(updateProfile.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Profile update failed';
      });

    // Enable Biometric
    builder
      .addCase(enableBiometric.fulfilled, (state) => {
        state.biometricEnabled = true;
        state.error = null;
      })
      .addCase(enableBiometric.rejected, (state, action) => {
        state.error = action.payload?.message || 'Biometric enable failed';
      });

    // Disable Biometric
    builder
      .addCase(disableBiometric.fulfilled, (state) => {
        state.biometricEnabled = false;
        state.error = null;
      })
      .addCase(disableBiometric.rejected, (state, action) => {
        state.error = action.payload?.message || 'Biometric disable failed';
      });
  }
});

// ============================================================================
// SELECTORS
// ============================================================================

export const selectAuth = (state: { auth: AuthState }) => state.auth;
export const selectUser = (state: { auth: AuthState }) => state.auth.user;
export const selectIsAuthenticated = (state: { auth: AuthState }) => state.auth.isAuthenticated;
export const selectAuthLoading = (state: { auth: AuthState }) => state.auth.isLoading;
export const selectAuthError = (state: { auth: AuthState }) => state.auth.error;
export const selectBiometricEnabled = (state: { auth: AuthState }) => state.auth.biometricEnabled;

// ============================================================================
// EXPORTS
// ============================================================================

export const { clearError, setBiometricEnabled, setUser, logout } = authSlice.actions;
export default authSlice.reducer;
