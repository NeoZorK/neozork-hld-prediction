/**
 * Dashboard Service
 * 
 * This service handles all dashboard-related API calls and data management.
 */

import { ApiResponse, DashboardStats, PaginatedResponse, Tenant, User } from '../types';
import { apiClient } from './apiClient';

// ============================================================================
// INTERFACES
// ============================================================================

interface DashboardFilters {
  tenant_id?: string;
  date_from?: string;
  date_to?: string;
  period?: 'day' | 'week' | 'month' | 'year';
}

interface UsageAnalytics {
  total_api_calls: number;
  total_storage_used: number;
  active_users: number;
  peak_usage: number;
  trends: {
    api_calls: number;
    storage: number;
    users: number;
  };
}

// ============================================================================
// DASHBOARD SERVICE
// ============================================================================

export class DashboardService {
  private baseUrl = '/api/v1/dashboard';

  /**
   * Get dashboard statistics
   */
  async getStats(tenantId?: string): Promise<ApiResponse<DashboardStats>> {
    try {
      const params = new URLSearchParams();
      if (tenantId) params.append('tenant_id', tenantId);
      
      const response = await apiClient.get(`${this.baseUrl}/stats?${params}`);
      return response.data;
    } catch (error) {
      return {
        success: false,
        data: {} as DashboardStats,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Get usage analytics
   */
  async getUsageAnalytics(
    tenantId?: string,
    filters?: DashboardFilters
  ): Promise<ApiResponse<UsageAnalytics>> {
    try {
      const params = new URLSearchParams();
      if (tenantId) params.append('tenant_id', tenantId);
      if (filters?.date_from) params.append('date_from', filters.date_from);
      if (filters?.date_to) params.append('date_to', filters.date_to);
      if (filters?.period) params.append('period', filters.period);
      
      const response = await apiClient.get(`${this.baseUrl}/usage-analytics?${params}`);
      return response.data;
    } catch (error) {
      return {
        success: false,
        data: {} as UsageAnalytics,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Get recent activity
   */
  async getRecentActivity(
    tenantId?: string,
    limit: number = 10
  ): Promise<ApiResponse<any[]>> {
    try {
      const params = new URLSearchParams();
      if (tenantId) params.append('tenant_id', tenantId);
      params.append('limit', limit.toString());
      
      const response = await apiClient.get(`${this.baseUrl}/recent-activity?${params}`);
      return response.data;
    } catch (error) {
      return {
        success: false,
        data: [],
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Get system health status
   */
  async getSystemHealth(): Promise<ApiResponse<any>> {
    try {
      const response = await apiClient.get(`${this.baseUrl}/system-health`);
      return response.data;
    } catch (error) {
      return {
        success: false,
        data: null,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Get tenant list for admin
   */
  async getTenants(
    page: number = 1,
    limit: number = 20,
    filters?: any
  ): Promise<ApiResponse<PaginatedResponse<Tenant>>> {
    try {
      const params = new URLSearchParams();
      params.append('page', page.toString());
      params.append('limit', limit.toString());
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            params.append(key, value.toString());
          }
        });
      }
      
      const response = await apiClient.get(`${this.baseUrl}/tenants?${params}`);
      return response.data;
    } catch (error) {
      return {
        success: false,
        data: { data: [], pagination: { page: 1, per_page: 20, total: 0, total_pages: 0 } },
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Get user list for admin
   */
  async getUsers(
    page: number = 1,
    limit: number = 20,
    filters?: any
  ): Promise<ApiResponse<PaginatedResponse<User>>> {
    try {
      const params = new URLSearchParams();
      params.append('page', page.toString());
      params.append('limit', limit.toString());
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            params.append(key, value.toString());
          }
        });
      }
      
      const response = await apiClient.get(`${this.baseUrl}/users?${params}`);
      return response.data;
    } catch (error) {
      return {
        success: false,
        data: { data: [], pagination: { page: 1, per_page: 20, total: 0, total_pages: 0 } },
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Refresh dashboard data
   */
  async refreshData(tenantId?: string): Promise<ApiResponse<DashboardStats>> {
    try {
      const params = new URLSearchParams();
      if (tenantId) params.append('tenant_id', tenantId);
      
      const response = await apiClient.post(`${this.baseUrl}/refresh?${params}`);
      return response.data;
    } catch (error) {
      return {
        success: false,
        data: {} as DashboardStats,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Export dashboard data
   */
  async exportData(
    format: 'csv' | 'json' | 'pdf',
    tenantId?: string,
    filters?: DashboardFilters
  ): Promise<ApiResponse<{ download_url: string }>> {
    try {
      const params = new URLSearchParams();
      params.append('format', format);
      if (tenantId) params.append('tenant_id', tenantId);
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            params.append(key, value.toString());
          }
        });
      }
      
      const response = await apiClient.post(`${this.baseUrl}/export?${params}`);
      return response.data;
    } catch (error) {
      return {
        success: false,
        data: { download_url: '' },
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }
}

// ============================================================================
// EXPORT INSTANCE
// ============================================================================

export const dashboardService = new DashboardService();
