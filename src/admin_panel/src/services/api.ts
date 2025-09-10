/**
 * API Service for Pocket Hedge Fund Admin Panel
 * 
 * This service handles all API communications with the backend,
 * including tenant management, user management, analytics, and system administration.
 */

import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios';
import { 
  AdminUser,
  Tenant,
  User,
  Fund,
  DashboardStats,
  AnalyticsData,
  BillingRecord,
  RevenueReport,
  SystemConfig,
  SystemHealth,
  ApiResponse,
  PaginationInfo,
  ApiError
} from '../types';

// ============================================================================
// API CONFIGURATION
// ============================================================================

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8080/api/v1/admin';

// ============================================================================
// HTTP CLIENT
// ============================================================================

class AdminHttpClient {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor(baseURL: string) {
    this.client = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Handle unauthorized access
          this.clearToken();
          window.location.href = '/login';
        }
        return Promise.reject(this.handleError(error));
      }
    );
  }

  private handleError(error: AxiosError): ApiError {
    const response = error.response?.data as any;
    return {
      error: response?.error || 'API Error',
      message: response?.message || error.message || 'An error occurred',
      details: response?.details,
      timestamp: new Date().toISOString(),
      request_id: response?.request_id,
      code: error.response?.status
    };
  }

  public setToken(token: string): void {
    this.token = token;
    localStorage.setItem('admin_token', token);
  }

  public clearToken(): void {
    this.token = null;
    localStorage.removeItem('admin_token');
  }

  public getToken(): string | null {
    return this.token || localStorage.getItem('admin_token');
  }

  // HTTP Methods
  async get<T>(url: string, params?: any): Promise<T> {
    const response = await this.client.get(url, { params });
    return response.data;
  }

  async post<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.post(url, data);
    return response.data;
  }

  async put<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.put(url, data);
    return response.data;
  }

  async delete<T>(url: string): Promise<T> {
    const response = await this.client.delete(url);
    return response.data;
  }

  async patch<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.patch(url, data);
    return response.data;
  }
}

// ============================================================================
// API SERVICE INSTANCE
// ============================================================================

const apiClient = new AdminHttpClient(API_BASE_URL);

// ============================================================================
// AUTHENTICATION API
// ============================================================================

export const authAPI = {
  /**
   * Admin login
   */
  async login(credentials: { email: string; password: string; mfa_code?: string }): Promise<{ user: AdminUser; token: string }> {
    const response = await apiClient.post<{ user: AdminUser; token: string }>('/auth/login', credentials);
    apiClient.setToken(response.token);
    return response;
  },

  /**
   * Admin logout
   */
  async logout(): Promise<void> {
    try {
      await apiClient.post('/auth/logout');
    } finally {
      apiClient.clearToken();
    }
  },

  /**
   * Get current admin user
   */
  async getCurrentUser(): Promise<AdminUser> {
    return apiClient.get<AdminUser>('/auth/me');
  },

  /**
   * Refresh token
   */
  async refreshToken(): Promise<{ token: string }> {
    const response = await apiClient.post<{ token: string }>('/auth/refresh');
    apiClient.setToken(response.token);
    return response;
  },

  /**
   * Change password
   */
  async changePassword(data: { current_password: string; new_password: string }): Promise<void> {
    return apiClient.post('/auth/change-password', data);
  }
};

// ============================================================================
// TENANT MANAGEMENT API
// ============================================================================

export const tenantAPI = {
  /**
   * Get all tenants with pagination and filtering
   */
  async getTenants(params?: {
    page?: number;
    page_size?: number;
    status?: string;
    plan?: string;
    search?: string;
    sort_by?: string;
    sort_order?: 'asc' | 'desc';
  }): Promise<{ tenants: Tenant[]; pagination: PaginationInfo }> {
    return apiClient.get('/tenants', params);
  },

  /**
   * Get tenant by ID
   */
  async getTenant(tenantId: string): Promise<Tenant> {
    return apiClient.get<Tenant>(`/tenants/${tenantId}`);
  },

  /**
   * Create new tenant
   */
  async createTenant(tenantData: Partial<Tenant>): Promise<Tenant> {
    return apiClient.post<Tenant>('/tenants', tenantData);
  },

  /**
   * Update tenant
   */
  async updateTenant(tenantId: string, tenantData: Partial<Tenant>): Promise<Tenant> {
    return apiClient.put<Tenant>(`/tenants/${tenantId}`, tenantData);
  },

  /**
   * Delete tenant
   */
  async deleteTenant(tenantId: string): Promise<void> {
    return apiClient.delete(`/tenants/${tenantId}`);
  },

  /**
   * Suspend tenant
   */
  async suspendTenant(tenantId: string, reason: string): Promise<void> {
    return apiClient.post(`/tenants/${tenantId}/suspend`, { reason });
  },

  /**
   * Activate tenant
   */
  async activateTenant(tenantId: string): Promise<void> {
    return apiClient.post(`/tenants/${tenantId}/activate`);
  },

  /**
   * Get tenant usage statistics
   */
  async getTenantUsage(tenantId: string): Promise<any> {
    return apiClient.get(`/tenants/${tenantId}/usage`);
  },

  /**
   * Update tenant settings
   */
  async updateTenantSettings(tenantId: string, settings: any): Promise<void> {
    return apiClient.put(`/tenants/${tenantId}/settings`, settings);
  }
};

// ============================================================================
// USER MANAGEMENT API
// ============================================================================

export const userAPI = {
  /**
   * Get all users with pagination and filtering
   */
  async getUsers(params?: {
    page?: number;
    page_size?: number;
    tenant_id?: string;
    role?: string;
    status?: string;
    search?: string;
    sort_by?: string;
    sort_order?: 'asc' | 'desc';
  }): Promise<{ users: User[]; pagination: PaginationInfo }> {
    return apiClient.get('/users', params);
  },

  /**
   * Get user by ID
   */
  async getUser(userId: string): Promise<User> {
    return apiClient.get<User>(`/users/${userId}`);
  },

  /**
   * Create new user
   */
  async createUser(userData: Partial<User>): Promise<User> {
    return apiClient.post<User>('/users', userData);
  },

  /**
   * Update user
   */
  async updateUser(userId: string, userData: Partial<User>): Promise<User> {
    return apiClient.put<User>(`/users/${userId}`, userData);
  },

  /**
   * Delete user
   */
  async deleteUser(userId: string): Promise<void> {
    return apiClient.delete(`/users/${userId}`);
  },

  /**
   * Suspend user
   */
  async suspendUser(userId: string, reason: string): Promise<void> {
    return apiClient.post(`/users/${userId}/suspend`, { reason });
  },

  /**
   * Activate user
   */
  async activateUser(userId: string): Promise<void> {
    return apiClient.post(`/users/${userId}/activate`);
  },

  /**
   * Reset user password
   */
  async resetUserPassword(userId: string): Promise<{ temporary_password: string }> {
    return apiClient.post(`/users/${userId}/reset-password`);
  },

  /**
   * Get user activity
   */
  async getUserActivity(userId: string, params?: {
    page?: number;
    page_size?: number;
    action?: string;
    date_from?: string;
    date_to?: string;
  }): Promise<{ activities: any[]; pagination: PaginationInfo }> {
    return apiClient.get(`/users/${userId}/activity`, params);
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
    page?: number;
    page_size?: number;
    tenant_id?: string;
    status?: string;
    fund_type?: string;
    risk_level?: string;
    search?: string;
    sort_by?: string;
    sort_order?: 'asc' | 'desc';
  }): Promise<{ funds: Fund[]; pagination: PaginationInfo }> {
    return apiClient.get('/funds', params);
  },

  /**
   * Get fund by ID
   */
  async getFund(fundId: string): Promise<Fund> {
    return apiClient.get<Fund>(`/funds/${fundId}`);
  },

  /**
   * Update fund
   */
  async updateFund(fundId: string, fundData: Partial<Fund>): Promise<Fund> {
    return apiClient.put<Fund>(`/funds/${fundId}`, fundData);
  },

  /**
   * Suspend fund
   */
  async suspendFund(fundId: string, reason: string): Promise<void> {
    return apiClient.post(`/funds/${fundId}/suspend`, { reason });
  },

  /**
   * Activate fund
   */
  async activateFund(fundId: string): Promise<void> {
    return apiClient.post(`/funds/${fundId}/activate`);
  },

  /**
   * Get fund compliance status
   */
  async getFundCompliance(fundId: string): Promise<any> {
    return apiClient.get(`/funds/${fundId}/compliance`);
  },

  /**
   * Update fund compliance
   */
  async updateFundCompliance(fundId: string, complianceData: any): Promise<void> {
    return apiClient.put(`/funds/${fundId}/compliance`, complianceData);
  }
};

// ============================================================================
// ANALYTICS API
// ============================================================================

export const analyticsAPI = {
  /**
   * Get dashboard statistics
   */
  async getDashboardStats(): Promise<DashboardStats> {
    return apiClient.get<DashboardStats>('/analytics/dashboard');
  },

  /**
   * Get analytics data
   */
  async getAnalyticsData(params?: {
    period?: string;
    metric?: string;
    tenant_id?: string;
    date_from?: string;
    date_to?: string;
  }): Promise<AnalyticsData> {
    return apiClient.get<AnalyticsData>('/analytics/data', params);
  },

  /**
   * Get revenue analytics
   */
  async getRevenueAnalytics(params?: {
    period?: string;
    tenant_id?: string;
    date_from?: string;
    date_to?: string;
  }): Promise<any> {
    return apiClient.get('/analytics/revenue', params);
  },

  /**
   * Get user analytics
   */
  async getUserAnalytics(params?: {
    period?: string;
    tenant_id?: string;
    date_from?: string;
    date_to?: string;
  }): Promise<any> {
    return apiClient.get('/analytics/users', params);
  },

  /**
   * Get fund performance analytics
   */
  async getFundPerformanceAnalytics(params?: {
    period?: string;
    tenant_id?: string;
    fund_id?: string;
    date_from?: string;
    date_to?: string;
  }): Promise<any> {
    return apiClient.get('/analytics/funds', params);
  }
};

// ============================================================================
// BILLING API
// ============================================================================

export const billingAPI = {
  /**
   * Get billing records
   */
  async getBillingRecords(params?: {
    page?: number;
    page_size?: number;
    tenant_id?: string;
    status?: string;
    date_from?: string;
    date_to?: string;
    sort_by?: string;
    sort_order?: 'asc' | 'desc';
  }): Promise<{ records: BillingRecord[]; pagination: PaginationInfo }> {
    return apiClient.get('/billing/records', params);
  },

  /**
   * Get revenue report
   */
  async getRevenueReport(params?: {
    period?: string;
    tenant_id?: string;
    date_from?: string;
    date_to?: string;
  }): Promise<RevenueReport> {
    return apiClient.get<RevenueReport>('/billing/revenue-report', params);
  },

  /**
   * Create billing record
   */
  async createBillingRecord(recordData: Partial<BillingRecord>): Promise<BillingRecord> {
    return apiClient.post<BillingRecord>('/billing/records', recordData);
  },

  /**
   * Update billing record
   */
  async updateBillingRecord(recordId: string, recordData: Partial<BillingRecord>): Promise<BillingRecord> {
    return apiClient.put<BillingRecord>(`/billing/records/${recordId}`, recordData);
  },

  /**
   * Mark billing record as paid
   */
  async markBillingRecordPaid(recordId: string, paymentData: any): Promise<void> {
    return apiClient.post(`/billing/records/${recordId}/mark-paid`, paymentData);
  }
};

// ============================================================================
// SYSTEM MANAGEMENT API
// ============================================================================

export const systemAPI = {
  /**
   * Get system configuration
   */
  async getSystemConfig(): Promise<SystemConfig> {
    return apiClient.get<SystemConfig>('/system/config');
  },

  /**
   * Update system configuration
   */
  async updateSystemConfig(config: Partial<SystemConfig>): Promise<SystemConfig> {
    return apiClient.put<SystemConfig>('/system/config', config);
  },

  /**
   * Get system health
   */
  async getSystemHealth(): Promise<SystemHealth> {
    return apiClient.get<SystemHealth>('/system/health');
  },

  /**
   * Get system logs
   */
  async getSystemLogs(params?: {
    page?: number;
    page_size?: number;
    level?: string;
    service?: string;
    date_from?: string;
    date_to?: string;
  }): Promise<{ logs: any[]; pagination: PaginationInfo }> {
    return apiClient.get('/system/logs', params);
  },

  /**
   * Enable maintenance mode
   */
  async enableMaintenanceMode(config: any): Promise<void> {
    return apiClient.post('/system/maintenance/enable', config);
  },

  /**
   * Disable maintenance mode
   */
  async disableMaintenanceMode(): Promise<void> {
    return apiClient.post('/system/maintenance/disable');
  },

  /**
   * Get system metrics
   */
  async getSystemMetrics(params?: {
    period?: string;
    metric?: string;
    date_from?: string;
    date_to?: string;
  }): Promise<any> {
    return apiClient.get('/system/metrics', params);
  }
};

// ============================================================================
// EXPORT API CLIENT
// ============================================================================

export { apiClient };
export default {
  auth: authAPI,
  tenant: tenantAPI,
  user: userAPI,
  fund: fundAPI,
  analytics: analyticsAPI,
  billing: billingAPI,
  system: systemAPI
};
