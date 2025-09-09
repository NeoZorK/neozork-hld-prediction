import axios from 'axios';
import * as SecureStore from 'expo-secure-store';
import Constants from 'expo-constants';

// Get API base URL from environment or use default
const API_BASE_URL = Constants.expoConfig?.extra?.apiUrl || 'http://localhost:8080/api/v1';

class ApiService {
  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.api.interceptors.request.use(
      async (config) => {
        const token = await SecureStore.getItemAsync('auth_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor to handle errors
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Token expired or invalid, clear auth data
          await SecureStore.deleteItemAsync('auth_token');
          await SecureStore.deleteItemAsync('user_data');
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication endpoints
  async login(email, password) {
    try {
      const response = await this.api.post('/auth/login', {
        email,
        password,
      });
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Login failed',
      };
    }
  }

  async register(userData) {
    try {
      const response = await this.api.post('/auth/register', userData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Registration failed',
      };
    }
  }

  async verifyToken(token) {
    try {
      const response = await this.api.post('/auth/verify', { token });
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Token verification failed',
      };
    }
  }

  async changePassword(oldPassword, newPassword) {
    try {
      const response = await this.api.post('/auth/change-password', {
        old_password: oldPassword,
        new_password: newPassword,
      });
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Password change failed',
      };
    }
  }

  async forgotPassword(email) {
    try {
      const response = await this.api.post('/auth/forgot-password', { email });
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Password reset failed',
      };
    }
  }

  // User profile endpoints
  async getProfile() {
    try {
      const response = await this.api.get('/users/profile');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Failed to get profile',
      };
    }
  }

  async updateProfile(userData) {
    try {
      const response = await this.api.put('/users/profile', userData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Profile update failed',
      };
    }
  }

  // Fund endpoints
  async getFunds() {
    try {
      const response = await this.api.get('/funds/');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Failed to get funds',
      };
    }
  }

  async getFund(fundId) {
    try {
      const response = await this.api.get(`/funds/${fundId}`);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Failed to get fund',
      };
    }
  }

  // Investment endpoints
  async getInvestments() {
    try {
      const response = await this.api.get('/investments/');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Failed to get investments',
      };
    }
  }

  async createInvestment(investmentData) {
    try {
      const response = await this.api.post('/investments/', investmentData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Investment creation failed',
      };
    }
  }

  async getInvestment(investmentId) {
    try {
      const response = await this.api.get(`/investments/${investmentId}`);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Failed to get investment',
      };
    }
  }

  async updateInvestment(investmentId, investmentData) {
    try {
      const response = await this.api.put(`/investments/${investmentId}`, investmentData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Investment update failed',
      };
    }
  }

  async cancelInvestment(investmentId) {
    try {
      const response = await this.api.delete(`/investments/${investmentId}`);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Investment cancellation failed',
      };
    }
  }

  // Portfolio endpoints
  async getPortfolioSummary() {
    try {
      const response = await this.api.get('/portfolio/summary');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Failed to get portfolio summary',
      };
    }
  }

  async getPortfolioAnalytics() {
    try {
      const response = await this.api.get('/portfolio/analytics');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Failed to get portfolio analytics',
      };
    }
  }

  // Returns endpoints
  async getPortfolioReturns() {
    try {
      const response = await this.api.get('/returns/portfolio');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Failed to get portfolio returns',
      };
    }
  }

  async getRiskMetrics() {
    try {
      const response = await this.api.get('/returns/risk-metrics');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Failed to get risk metrics',
      };
    }
  }

  async getReturnsSummary() {
    try {
      const response = await this.api.get('/returns/summary');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Failed to get returns summary',
      };
    }
  }

  // Biometric endpoints
  async enableBiometric() {
    try {
      const response = await this.api.post('/auth/enable-biometric');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Biometric enable failed',
      };
    }
  }

  async disableBiometric() {
    try {
      const response = await this.api.post('/auth/disable-biometric');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Biometric disable failed',
      };
    }
  }

  // Health check
  async healthCheck() {
    try {
      const response = await this.api.get('/health');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: 'Health check failed',
      };
    }
  }
}

export const apiService = new ApiService();
