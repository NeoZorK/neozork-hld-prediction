/**
 * Chart Service Tests
 * 
 * Unit tests for the chart service.
 */

import { chartService } from '../services/chartService';
import { apiClient } from '../services/apiClient';

// Mock the API client
jest.mock('../services/apiClient');
const mockApiClient = apiClient as jest.Mocked<typeof apiClient>;

// ============================================================================
// TEST DATA
// ============================================================================

const mockChartData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
  datasets: [{
    label: 'API Calls',
    data: [100, 200, 150, 300, 250],
    backgroundColor: 'rgba(59, 130, 246, 0.2)',
    borderColor: 'rgba(59, 130, 246, 1)',
    borderWidth: 2
  }]
};

// ============================================================================
// TESTS
// ============================================================================

describe('Chart Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getUsageData', () => {
    it('returns chart data successfully', async () => {
      mockApiClient.get.mockResolvedValue({
        data: {
          success: true,
          data: mockChartData
        }
      });

      const result = await chartService.getUsageData({
        type: 'line',
        period: '30d',
        dataKey: 'api_calls',
        tenant_id: 'tenant-1'
      });

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockChartData);
      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/api/v1/charts/usage',
        {
          type: 'line',
          period: '30d',
          dataKey: 'api_calls',
          tenant_id: 'tenant-1'
        }
      );
    });

    it('returns mock data when API fails', async () => {
      mockApiClient.get.mockRejectedValue(new Error('API Error'));

      const result = await chartService.getUsageData({
        type: 'line',
        period: '30d',
        dataKey: 'api_calls'
      });

      expect(result.success).toBe(false);
      expect(result.data).toBeDefined();
      expect(result.data.labels).toBeDefined();
      expect(result.data.datasets).toBeDefined();
    });
  });

  describe('getRevenueData', () => {
    it('returns revenue chart data successfully', async () => {
      mockApiClient.get.mockResolvedValue({
        data: {
          success: true,
          data: mockChartData
        }
      });

      const result = await chartService.getRevenueData('30d', 'tenant-1');

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockChartData);
      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/api/v1/charts/revenue',
        { period: '30d', tenant_id: 'tenant-1' }
      );
    });

    it('returns mock data when API fails', async () => {
      mockApiClient.get.mockRejectedValue(new Error('API Error'));

      const result = await chartService.getRevenueData('30d');

      expect(result.success).toBe(false);
      expect(result.data).toBeDefined();
    });
  });

  describe('getUserActivityData', () => {
    it('returns user activity chart data successfully', async () => {
      mockApiClient.get.mockResolvedValue({
        data: {
          success: true,
          data: mockChartData
        }
      });

      const result = await chartService.getUserActivityData('30d', 'tenant-1');

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockChartData);
      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/api/v1/charts/user-activity',
        { period: '30d', tenant_id: 'tenant-1' }
      );
    });

    it('returns mock data when API fails', async () => {
      mockApiClient.get.mockRejectedValue(new Error('API Error'));

      const result = await chartService.getUserActivityData('30d');

      expect(result.success).toBe(false);
      expect(result.data).toBeDefined();
    });
  });

  describe('getSystemPerformanceData', () => {
    it('returns system performance chart data successfully', async () => {
      mockApiClient.get.mockResolvedValue({
        data: {
          success: true,
          data: mockChartData
        }
      });

      const result = await chartService.getSystemPerformanceData('30d');

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockChartData);
      expect(mockApiClient.get).toHaveBeenCalledWith(
        '/api/v1/charts/system-performance',
        { period: '30d' }
      );
    });

    it('returns mock data when API fails', async () => {
      mockApiClient.get.mockRejectedValue(new Error('API Error'));

      const result = await chartService.getSystemPerformanceData('30d');

      expect(result.success).toBe(false);
      expect(result.data).toBeDefined();
    });
  });

  describe('Mock Data Generation', () => {
    it('generates correct mock data for different periods', async () => {
      mockApiClient.get.mockRejectedValue(new Error('API Error'));

      const result7d = await chartService.getUsageData({
        type: 'line',
        period: '7d',
        dataKey: 'api_calls'
      });

      const result30d = await chartService.getUsageData({
        type: 'line',
        period: '30d',
        dataKey: 'api_calls'
      });

      const result90d = await chartService.getUsageData({
        type: 'line',
        period: '90d',
        dataKey: 'api_calls'
      });

      expect(result7d.data.labels).toHaveLength(7);
      expect(result30d.data.labels).toHaveLength(30);
      expect(result90d.data.labels).toHaveLength(90);
    });

    it('generates correct mock data for different chart types', async () => {
      mockApiClient.get.mockRejectedValue(new Error('API Error'));

      const lineResult = await chartService.getUsageData({
        type: 'line',
        period: '30d',
        dataKey: 'api_calls'
      });

      const barResult = await chartService.getUsageData({
        type: 'bar',
        period: '30d',
        dataKey: 'api_calls'
      });

      const pieResult = await chartService.getUsageData({
        type: 'pie',
        period: '30d',
        dataKey: 'api_calls'
      });

      expect(lineResult.data.datasets[0].backgroundColor).toBe('rgba(59, 130, 246, 0.2)');
      expect(barResult.data.datasets[0].backgroundColor).toBe('rgba(59, 130, 246, 0.2)');
      expect(Array.isArray(pieResult.data.datasets[0].backgroundColor)).toBe(true);
    });

    it('generates correct mock data for different data keys', async () => {
      mockApiClient.get.mockRejectedValue(new Error('API Error'));

      const apiCallsResult = await chartService.getUsageData({
        type: 'line',
        period: '30d',
        dataKey: 'api_calls'
      });

      const storageResult = await chartService.getUsageData({
        type: 'line',
        period: '30d',
        dataKey: 'storage'
      });

      const usersResult = await chartService.getUsageData({
        type: 'line',
        period: '30d',
        dataKey: 'users'
      });

      expect(apiCallsResult.data.datasets[0].label).toBe('API Calls');
      expect(storageResult.data.datasets[0].label).toBe('Storage (GB)');
      expect(usersResult.data.datasets[0].label).toBe('Active Users');
    });
  });
});
