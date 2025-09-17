/**
 * API Service for Pocket Hedge Fund React Dashboard
 * 
 * This service handles all API communications with the backend,
 * including authentication, fund management, and data fetching.
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
  ApiResponse,
  PaginatedResponse,
  ApiError
} from '../types';

// ============================================================================
// API CONFIGURATION
// ============================================================================

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080/api/v1';
const API_TIMEOUT = 30000; // 30 seconds

// ============================================================================
// HTTP CLIENT
// ============================================================================

class HttpClient {
  private baseURL: string;
  private timeout: number;
  private defaultHeaders: Record<string, string>;

  constructor(baseURL: string, timeout: number = API_TIMEOUT) {
    this.baseURL = baseURL;
    this.timeout = timeout;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const token = this.getAuthToken();
    
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
          errorData.request_id
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

  private getAuthToken(): string | null {
    return localStorage.getItem('access_token');
  }

  private setAuthToken(token: string): void {
    localStorage.setItem('access_token', token);
  }

  private removeAuthToken(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
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
  setToken(token: string): void {
    this.setAuthToken(token);
  }

  clearToken(): void {
    this.removeAuthToken();
  }
}

// ============================================================================
// API SERVICE INSTANCE
// ============================================================================

const apiClient = new HttpClient(API_BASE_URL);

// ============================================================================
// AUTHENTICATION API
// ============================================================================

export const authAPI = {
  /**
   * Login user with email and password
   */
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>('/auth/login', credentials);
    apiClient.setToken(response.access_token);
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
      apiClient.clearToken();
    }
  },

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<LoginResponse> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new ApiError('No Refresh Token', 'No refresh token available');
    }

    const response = await apiClient.post<LoginResponse>('/auth/refresh', {
      refresh_token: refreshToken
    });
    
    apiClient.setToken(response.access_token);
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
   * Change password
   */
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    return apiClient.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword
    });
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
   * Create new fund
   */
  async createFund(fundData: Omit<Fund, 'fund_id' | 'created_at' | 'updated_at'>): Promise<Fund> {
    return apiClient.post<Fund>('/funds/', fundData);
  },

  /**
   * Update fund
   */
  async updateFund(fundId: string, fundData: Partial<Fund>): Promise<Fund> {
    return apiClient.put<Fund>(`/funds/${fundId}`, fundData);
  },

  /**
   * Delete fund (soft delete)
   */
  async deleteFund(fundId: string): Promise<void> {
    return apiClient.delete(`/funds/${fundId}`);
  },

  /**
   * Get fund performance history
   */
  async getFundPerformance(fundId: string, days: number = 30): Promise<FundPerformance[]> {
    return apiClient.get<FundPerformance[]>(`/funds/${fundId}/performance`, { days });
  },

  /**
   * Get fund investors
   */
  async getFundInvestors(fundId: string, params?: {
    page?: number;
    page_size?: number;
  }): Promise<PaginatedResponse<Investor>> {
    return apiClient.get<PaginatedResponse<Investor>>(`/funds/${fundId}/investors`, params);
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
   * Add new position to portfolio
   */
  async addPosition(fundId: string, position: Omit<PortfolioPosition, 'current_value' | 'unrealized_pnl' | 'unrealized_pnl_percentage' | 'weight_percentage'>): Promise<PortfolioPosition> {
    return apiClient.post<PortfolioPosition>(`/portfolio/${fundId}/positions`, position);
  },

  /**
   * Update position in portfolio
   */
  async updatePosition(fundId: string, symbol: string, position: Partial<PortfolioPosition>): Promise<PortfolioPosition> {
    return apiClient.put<PortfolioPosition>(`/portfolio/${fundId}/positions/${symbol}`, position);
  },

  /**
   * Remove position from portfolio
   */
  async removePosition(fundId: string, symbol: string): Promise<void> {
    return apiClient.delete(`/portfolio/${fundId}/positions/${symbol}`);
  },

  /**
   * Update portfolio prices
   */
  async updatePrices(fundId: string, prices: Record<string, number>): Promise<void> {
    return apiClient.put(`/portfolio/${fundId}/prices`, { prices });
  }
};

// ============================================================================
// INVESTOR API
// ============================================================================

export const investorAPI = {
  /**
   * Get investor's investments
   */
  async getInvestments(userId?: string): Promise<Investor[]> {
    const params = userId ? { user_id: userId } : undefined;
    return apiClient.get<Investor[]>('/investors/investments', params);
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

  constructor(
    error: string,
    message: string,
    details?: Record<string, any>,
    timestamp?: string,
    requestId?: string
  ) {
    super(message);
    this.name = 'ApiError';
    this.error = error;
    this.details = details;
    this.timestamp = timestamp || new Date().toISOString();
    this.requestId = requestId;
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
  system: systemAPI
};
