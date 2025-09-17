/**
 * Dashboard Service Tests
 * 
 * Unit tests for the dashboard service.
 */

import { dashboardService } from '../services/dashboardService';
import { apiClient } from '../services/apiClient';

// Mock the API client
jest.mock('../services/apiClient');
const mockApiClient = apiClient as jest.Mocked<typeof apiClient>;

// ============================================================================
// TEST DATA
// ============================================================================

const mockDashboardStats = {
  total_tenants: 10,
  active_tenants: 8,
  total_users: 50,
  total_revenue: 10000,
  monthly_revenue: 1000,
  usage_stats: {
    total_api_calls: 5000,
    total_storage_used: 25.5,
    active_users: 15,
    peak_usage: 1000
  },
  system_health: {
    status: 'healthy',
    uptime: 86400,
    response_time: 150,
    error_rate: 0.1
  }
};

const mockUsageAnalytics = {
  total_api_calls: 5000,
  total_storage_used: 25.5,
  active_users: 15,
  peak_usage: 1000,
  trends: {
    api_calls: 10,
    storage: 5,
    users: 15
  }
};

const mockRecentActivity = [
  {
    id: '1',
    type: 'user',
    title: 'User created',
    description: 'New user was created',
    timestamp: '2023-01-01T00:00:00Z',
    user: 'admin'
  }
];

// ============================================================================
// TESTS
// ============================================================================

describe('Dashboard Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getStats', () => {
    it('returns dashboard stats successfully', async () => {
      mockApiClient.get.mockResolvedValue({
        data: {
          success: true,
          data: mockDashboardStats
        }
      });

      const result = await dashboardService.getStats('tenant-1');

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockDashboardStats);
      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/api/v1/dashboard/stats?tenant_id=tenant-1'
      );
    });

    it('returns error when API fails', async () => {
      mockApiClient.get.mockRejectedValue(new Error('API Error'));

      const result = await dashboardService.getStats('tenant-1');

      expect(result.success).toBe(false);
      expect(result.error).toBe('API Error');
    });

    it('calls API without tenant_id when not provided', async () => {
      mockApiClient.get.mockResolvedValue({
        data: {
          success: true,
          data: mockDashboardStats
        }
      });

      await dashboardService.getStats();

      expect(mockApiClient.get).toHaveBeenCalledWith('/api/v1/dashboard/stats?');
    });
  });

  describe('getUsageAnalytics', () => {
    it('returns usage analytics successfully', async () => {
      mockApiClient.get.mockResolvedValue({
        data: {
          success: true,
          data: mockUsageAnalytics
        }
      });

      const result = await dashboardService.getUsageAnalytics('tenant-1', {
        date_from: '2023-01-01',
        date_to: '2023-01-31',
        period: 'month'
      });

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockUsageAnalytics);
      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/api/v1/dashboard/usage-analytics?tenant_id=tenant-1&date_from=2023-01-01&date_to=2023-01-31&period=month'
      );
    });

    it('handles API errors', async () => {
      mockApiClient.get.mockRejectedValue(new Error('Network Error'));

      const result = await dashboardService.getUsageAnalytics('tenant-1');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Network Error');
    });
  });

  describe('getRecentActivity', () => {
    it('returns recent activity successfully', async () => {
      mockApiClient.get.mockResolvedValue({
        data: {
          success: true,
          data: mockRecentActivity
        }
      });

      const result = await dashboardService.getRecentActivity('tenant-1', 10);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockRecentActivity);
      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/api/v1/dashboard/recent-activity?tenant_id=tenant-1&limit=10'
      );
    });

    it('uses default limit when not provided', async () => {
      mockApiClient.get.mockResolvedValue({
        data: {
          success: true,
          data: mockRecentActivity
        }
      });

      await dashboardService.getRecentActivity('tenant-1');

      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/api/v1/dashboard/recent-activity?tenant_id=tenant-1&limit=10'
      );
    });
  });

  describe('getSystemHealth', () => {
    it('returns system health successfully', async () => {
      const mockHealth = {
        status: 'healthy',
        uptime: 86400,
        response_time: 150,
        error_rate: 0.1
      };

      mockApiClient.get.mockResolvedValue({
        data: {
          success: true,
          data: mockHealth
        }
      });

      const result = await dashboardService.getSystemHealth();

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockHealth);
      expect(mockApiClient.get).toHaveBeenCalledWith('/api/v1/dashboard/system-health');
    });
  });

  describe('getTenants', () => {
    it('returns tenants with pagination', async () => {
      const mockTenants = {
        data: [],
        pagination: {
          page: 1,
          per_page: 20,
          total: 0,
          total_pages: 0
        }
      };

      mockApiClient.get.mockResolvedValue({
        data: {
          success: true,
          data: mockTenants
        }
      });

      const result = await dashboardService.getTenants(1, 20, { status: 'active' });

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockTenants);
      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/api/v1/dashboard/tenants?page=1&limit=20&status=active'
      );
    });
  });

  describe('getUsers', () => {
    it('returns users with pagination', async () => {
      const mockUsers = {
        data: [],
        pagination: {
          page: 1,
          per_page: 20,
          total: 0,
          total_pages: 0
        }
      };

      mockApiClient.get.mockResolvedValue({
        data: {
          success: true,
          data: mockUsers
        }
      });

      const result = await dashboardService.getUsers(1, 20, { role: 'admin' });

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockUsers);
      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/api/v1/dashboard/users?page=1&limit=20&role=admin'
      );
    });
  });

  describe('refreshData', () => {
    it('refreshes dashboard data successfully', async () => {
      mockApiClient.post.mockResolvedValue({
        data: {
          success: true,
          data: mockDashboardStats
        }
      });

      const result = await dashboardService.refreshData('tenant-1');

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockDashboardStats);
      expect(mockApiClient.post).toHaveBeenCalledWith(
        '/api/v1/dashboard/refresh?tenant_id=tenant-1'
      );
    });
  });

  describe('exportData', () => {
    it('exports data successfully', async () => {
      const mockExport = {
        download_url: 'https://example.com/export.csv'
      };

      mockApiClient.post.mockResolvedValue({
        data: {
          success: true,
          data: mockExport
        }
      });

      const result = await dashboardService.exportData('csv', 'tenant-1', {
        date_from: '2023-01-01',
        date_to: '2023-01-31'
      });

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockExport);
      expect(mockApiClient.post).toHaveBeenCalledWith(
        '/api/v1/dashboard/export?format=csv&tenant_id=tenant-1&date_from=2023-01-01&date_to=2023-01-31'
      );
    });
  });
});
