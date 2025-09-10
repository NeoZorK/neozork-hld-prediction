/**
 * API Service for Pocket Hedge Fund Mobile App
 * 
 * This service handles all API communications with the backend,
 * including authentication, fund management, and mobile-specific features.
 */

import { 
  LoginRequest, 
  LoginResponse, 
  RegisterRequest, 
  User,
  Fund,
  FundDetails,
  FundPerformance,
  Investor,
  PortfolioPosition,
  NotificationData,
  ApiResponse,
  PaginatedResponse,
  ApiError,
  DeviceInfo
} from '../types';

// ============================================================================
// API CONFIGURATION
// ============================================================================

const API_BASE_URL = __DEV__ 
  ? 'http://localhost:8080/api/v1'
  : 'https://api.neozork.com/api/v1';

const API_TIMEOUT = 30000; // 30 seconds

// ============================================================================
// HTTP CLIENT
// ============================================================================

class MobileHttpClient {
  private baseURL: string;
  private timeout: number;
  private defaultHeaders: Record<string, string>;

  constructor(baseURL: string, timeout: number = API_TIMEOUT) {
    this.baseURL = baseURL;
    this.timeout = timeout;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const token = await this.getAuthToken();
    
    const config: RequestInit = {
      ...options,
      headers: {
        ...this.defaultHeaders,
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      signal: AbortSignal.timeout(this.timeout),
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          errorData.error || 'API Error',
          errorData.message || `HTTP ${response.status}: ${response.statusText}`,
          errorData.details,
          new Date().toISOString(),
          errorData.request_id,
          response.status
        );
      }

      const data = await response.json();
      return data;
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      
      if (error.name === 'AbortError') {
        throw new ApiError(
          'Timeout',
          'Request timed out',
          {},
          new Date().toISOString()
        );
      }
      
      throw new ApiError(
        'Network Error',
        error.message || 'Failed to fetch data',
        {},
        new Date().toISOString()
      );
    }
  }

  private async getAuthToken(): Promise<string | null> {
    // In React Native, use AsyncStorage or SecureStore
    try {
      const { getItem } = await import('@react-native-async-storage/async-storage');
      return await getItem('access_token');
    } catch (error) {
      return null;
    }
  }

  private async setAuthToken(token: string): Promise<void> {
    try {
      const { setItem } = await import('@react-native-async-storage/async-storage');
      await setItem('access_token', token);
    } catch (error) {
      console.error('Failed to save auth token:', error);
    }
  }

  private async removeAuthToken(): Promise<void> {
    try {
      const { removeItem } = await import('@react-native-async-storage/async-storage');
      await removeItem('access_token');
      await removeItem('refresh_token');
    } catch (error) {
      console.error('Failed to remove auth tokens:', error);
    }
  }

  // HTTP Methods
  async get<T>(endpoint: string, params?: Record<string, any>): Promise<T> {
    const url = params ? `${endpoint}?${new URLSearchParams(params)}` : endpoint;
    return this.request<T>(url, { method: 'GET' });
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }

  // Token management
  async setToken(token: string): Promise<void> {
    await this.setAuthToken(token);
  }

  async clearToken(): Promise<void> {
    await this.removeAuthToken();
  }
}

// ============================================================================
// API SERVICE INSTANCE
// ============================================================================

const apiClient = new MobileHttpClient(API_BASE_URL);

// ============================================================================
// AUTHENTICATION API
// ============================================================================

export const authAPI = {
  /**
   * Login user with email and password
   */
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>('/auth/login', credentials);
    await apiClient.setToken(response.access_token);
    return response;
  },

  /**
   * Register new user
   */
  async register(userData: RegisterRequest): Promise<ApiResponse<User>> {
    return apiClient.post<ApiResponse<User>>('/auth/register', userData);
  },

  /**
   * Logout current user
   */
  async logout(): Promise<void> {
    try {
      await apiClient.post('/auth/logout');
    } finally {
      await apiClient.clearToken();
    }
  },

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<LoginResponse> {
    const { getItem } = await import('@react-native-async-storage/async-storage');
    const refreshToken = await getItem('refresh_token');
    
    if (!refreshToken) {
      throw new ApiError('No Refresh Token', 'No refresh token available');
    }

    const response = await apiClient.post<LoginResponse>('/auth/refresh', {
      refresh_token: refreshToken
    });
    
    await apiClient.setToken(response.access_token);
    return response;
  },

  /**
   * Get current user profile
   */
  async getCurrentUser(): Promise<User> {
    return apiClient.get<User>('/auth/me');
  },

  /**
   * Update user profile
   */
  async updateProfile(userData: Partial<User>): Promise<User> {
    return apiClient.put<User>('/auth/profile', userData);
  },

  /**
   * Enable biometric authentication
   */
  async enableBiometric(deviceInfo: DeviceInfo): Promise<void> {
    return apiClient.post('/auth/biometric/enable', deviceInfo);
  },

  /**
   * Disable biometric authentication
   */
  async disableBiometric(): Promise<void> {
    return apiClient.post('/auth/biometric/disable');
  }
};

// ============================================================================
// FUND MANAGEMENT API
// ============================================================================

export const fundAPI = {
  /**
   * Get all funds with pagination and filtering
   */
  async getFunds(params?: {
    fund_type?: string;
    status?: string;
    page?: number;
    page_size?: number;
  }): Promise<PaginatedResponse<Fund>> {
    return apiClient.get<PaginatedResponse<Fund>>('/funds/', params);
  },

  /**
   * Get fund by ID with full details
   */
  async getFund(fundId: string): Promise<FundDetails> {
    return apiClient.get<FundDetails>(`/funds/${fundId}`);
  },

  /**
   * Get fund performance history
   */
  async getFundPerformance(fundId: string, days: number = 30): Promise<FundPerformance[]> {
    return apiClient.get<FundPerformance[]>(`/funds/${fundId}/performance`, { days });
  },

  /**
   * Search funds by name or description
   */
  async searchFunds(query: string): Promise<Fund[]> {
    return apiClient.get<Fund[]>('/funds/search', { q: query });
  },

  /**
   * Get trending funds
   */
  async getTrendingFunds(): Promise<Fund[]> {
    return apiClient.get<Fund[]>('/funds/trending');
  },

  /**
   * Get user's favorite funds
   */
  async getFavoriteFunds(): Promise<Fund[]> {
    return apiClient.get<Fund[]>('/funds/favorites');
  },

  /**
   * Add fund to favorites
   */
  async addToFavorites(fundId: string): Promise<void> {
    return apiClient.post(`/funds/${fundId}/favorite`);
  },

  /**
   * Remove fund from favorites
   */
  async removeFromFavorites(fundId: string): Promise<void> {
    return apiClient.delete(`/funds/${fundId}/favorite`);
  }
};

// ============================================================================
// PORTFOLIO API
// ============================================================================

export const portfolioAPI = {
  /**
   * Get portfolio positions for a fund
   */
  async getPositions(fundId: string): Promise<PortfolioPosition[]> {
    return apiClient.get<PortfolioPosition[]>(`/portfolio/${fundId}/positions`);
  },

  /**
   * Get user's overall portfolio
   */
  async getUserPortfolio(): Promise<{
    total_value: number;
    total_return: number;
    total_return_percentage: number;
    positions: PortfolioPosition[];
  }> {
    return apiClient.get('/portfolio/user');
  },

  /**
   * Get portfolio performance history
   */
  async getPortfolioPerformance(days: number = 30): Promise<{
    date: string;
    value: number;
    return: number;
    return_percentage: number;
  }[]> {
    return apiClient.get('/portfolio/performance', { days });
  }
};

// ============================================================================
// INVESTOR API
// ============================================================================

export const investorAPI = {
  /**
   * Get investor's investments
   */
  async getInvestments(): Promise<Investor[]> {
    return apiClient.get<Investor[]>('/investors/investments');
  },

  /**
   * Make new investment
   */
  async makeInvestment(fundId: string, amount: number): Promise<Investor> {
    return apiClient.post<Investor>('/investors/invest', {
      fund_id: fundId,
      amount: amount
    });
  },

  /**
   * Withdraw investment
   */
  async withdrawInvestment(investmentId: string, amount: number): Promise<void> {
    return apiClient.post(`/investors/withdraw`, {
      investment_id: investmentId,
      amount: amount
    });
  },

  /**
   * Get investment history
   */
  async getInvestmentHistory(): Promise<{
    investments: Investor[];
    total_invested: number;
    total_return: number;
    total_return_percentage: number;
  }> {
    return apiClient.get('/investors/history');
  }
};

// ============================================================================
// NOTIFICATIONS API
// ============================================================================

export const notificationAPI = {
  /**
   * Get user notifications
   */
  async getNotifications(params?: {
    page?: number;
    page_size?: number;
    unread_only?: boolean;
  }): Promise<PaginatedResponse<NotificationData>> {
    return apiClient.get<PaginatedResponse<NotificationData>>('/notifications/', params);
  },

  /**
   * Mark notification as read
   */
  async markAsRead(notificationId: string): Promise<void> {
    return apiClient.put(`/notifications/${notificationId}/read`);
  },

  /**
   * Mark all notifications as read
   */
  async markAllAsRead(): Promise<void> {
    return apiClient.put('/notifications/read-all');
  },

  /**
   * Delete notification
   */
  async deleteNotification(notificationId: string): Promise<void> {
    return apiClient.delete(`/notifications/${notificationId}`);
  },

  /**
   * Update push notification settings
   */
  async updatePushSettings(settings: {
    enabled: boolean;
    fund_updates: boolean;
    investment_alerts: boolean;
    performance_notifications: boolean;
    system_announcements: boolean;
  }): Promise<void> {
    return apiClient.put('/notifications/push-settings', settings);
  }
};

// ============================================================================
// SYSTEM API
// ============================================================================

export const systemAPI = {
  /**
   * Get system health status
   */
  async getHealth(): Promise<{
    status: string;
    timestamp: string;
    version: string;
    database: string;
    authentication: string;
  }> {
    return apiClient.get('/health');
  },

  /**
   * Get API status
   */
  async getStatus(): Promise<{
    api_version: string;
    status: string;
    uptime: number;
    database_status: string;
    redis_status: string;
    active_connections: number;
    total_requests: number;
    error_rate: number;
  }> {
    return apiClient.get('/status');
  },

  /**
   * Get app configuration
   */
  async getAppConfig(): Promise<{
    min_app_version: string;
    maintenance_mode: boolean;
    features: Record<string, boolean>;
    limits: Record<string, number>;
  }> {
    return apiClient.get('/config/app');
  }
};

// ============================================================================
// ERROR HANDLING
// ============================================================================

export class ApiError extends Error {
  public readonly error: string;
  public readonly details?: Record<string, any>;
  public readonly timestamp: string;
  public readonly requestId?: string;
  public readonly code?: number;

  constructor(
    error: string,
    message: string,
    details?: Record<string, any>,
    timestamp?: string,
    requestId?: string,
    code?: number
  ) {
    super(message);
    this.name = 'ApiError';
    this.error = error;
    this.details = details;
    this.timestamp = timestamp || new Date().toISOString();
    this.requestId = requestId;
    this.code = code;
  }
}

// ============================================================================
// EXPORT API CLIENT
// ============================================================================

export { apiClient };
export default {
  auth: authAPI,
  fund: fundAPI,
  portfolio: portfolioAPI,
  investor: investorAPI,
  notification: notificationAPI,
  system: systemAPI
};
