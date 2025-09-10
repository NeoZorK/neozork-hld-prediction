import React, { createContext, useContext, useState, useEffect } from 'react';
import * as SecureStore from 'expo-secure-store';
import { Alert } from 'react-native';
import { apiService } from './ApiService';

const AuthContext = createContext({});

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    loadStoredAuth();
  }, []);

  const loadStoredAuth = async () => {
    try {
      const storedToken = await SecureStore.getItemAsync('auth_token');
      const storedUser = await SecureStore.getItemAsync('user_data');
      
      if (storedToken && storedUser) {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
        setIsAuthenticated(true);
        
        // Verify token is still valid
        const isValid = await verifyToken(storedToken);
        if (!isValid) {
          await logout();
        }
      }
    } catch (error) {
      console.error('Error loading stored auth:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const verifyToken = async (tokenToVerify) => {
    try {
      const response = await apiService.verifyToken(tokenToVerify);
      return response.success;
    } catch (error) {
      console.error('Token verification failed:', error);
      return false;
    }
  };

  const login = async (email, password) => {
    try {
      setIsLoading(true);
      const response = await apiService.login(email, password);
      
      if (response.success) {
        const { access_token, user: userData } = response.data;
        
        // Store auth data securely
        await SecureStore.setItemAsync('auth_token', access_token);
        await SecureStore.setItemAsync('user_data', JSON.stringify(userData));
        
        setToken(access_token);
        setUser(userData);
        setIsAuthenticated(true);
        
        return { success: true, user: userData };
      } else {
        return { success: false, error: response.message };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: 'Login failed. Please try again.' };
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (userData) => {
    try {
      setIsLoading(true);
      const response = await apiService.register(userData);
      
      if (response.success) {
        return { success: true, message: 'Registration successful. Please login.' };
      } else {
        return { success: false, error: response.message };
      }
    } catch (error) {
      console.error('Registration error:', error);
      return { success: false, error: 'Registration failed. Please try again.' };
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      // Clear stored auth data
      await SecureStore.deleteItemAsync('auth_token');
      await SecureStore.deleteItemAsync('user_data');
      
      setToken(null);
      setUser(null);
      setIsAuthenticated(false);
      
      return { success: true };
    } catch (error) {
      console.error('Logout error:', error);
      return { success: false, error: 'Logout failed' };
    }
  };

  const updateUser = async (updatedUserData) => {
    try {
      const response = await apiService.updateProfile(updatedUserData);
      
      if (response.success) {
        const updatedUser = { ...user, ...response.data };
        setUser(updatedUser);
        await SecureStore.setItemAsync('user_data', JSON.stringify(updatedUser));
        return { success: true, user: updatedUser };
      } else {
        return { success: false, error: response.message };
      }
    } catch (error) {
      console.error('Update user error:', error);
      return { success: false, error: 'Update failed. Please try again.' };
    }
  };

  const changePassword = async (oldPassword, newPassword) => {
    try {
      const response = await apiService.changePassword(oldPassword, newPassword);
      return response;
    } catch (error) {
      console.error('Change password error:', error);
      return { success: false, error: 'Password change failed. Please try again.' };
    }
  };

  const forgotPassword = async (email) => {
    try {
      const response = await apiService.forgotPassword(email);
      return response;
    } catch (error) {
      console.error('Forgot password error:', error);
      return { success: false, error: 'Password reset failed. Please try again.' };
    }
  };

  const enableBiometric = async () => {
    try {
      // Implementation for biometric authentication
      const response = await apiService.enableBiometric();
      return response;
    } catch (error) {
      console.error('Enable biometric error:', error);
      return { success: false, error: 'Biometric setup failed. Please try again.' };
    }
  };

  const disableBiometric = async () => {
    try {
      const response = await apiService.disableBiometric();
      return response;
    } catch (error) {
      console.error('Disable biometric error:', error);
      return { success: false, error: 'Biometric disable failed. Please try again.' };
    }
  };

  const value = {
    user,
    token,
    isLoading,
    isAuthenticated,
    login,
    register,
    logout,
    updateUser,
    changePassword,
    forgotPassword,
    enableBiometric,
    disableBiometric,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
