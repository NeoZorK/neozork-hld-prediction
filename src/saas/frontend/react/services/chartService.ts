/**
 * Chart Service
 * 
 * This service handles chart data generation and API calls for analytics.
 */

import { ApiResponse, ChartData, ChartDataPoint } from '../types';
import { apiClient } from './apiClient';

// ============================================================================
// INTERFACES
// ============================================================================

interface ChartRequest {
  type: 'line' | 'bar' | 'pie';
  period: string;
  dataKey: string;
  tenant_id?: string;
  date_from?: string;
  date_to?: string;
}

interface UsageData {
  api_calls: ChartDataPoint[];
  storage: ChartDataPoint[];
  users: ChartDataPoint[];
  revenue: ChartDataPoint[];
}

// ============================================================================
// CHART SERVICE
// ============================================================================

export class ChartService {
  private baseUrl = '/api/v1/charts';

  /**
   * Get usage data for charts
   */
  async getUsageData(request: ChartRequest): Promise<ApiResponse<ChartData>> {
    try {
      const response = await apiClient.get(`${this.baseUrl}/usage`, request);
      return response.data;
    } catch (error) {
      return {
        success: false,
        data: this.generateMockData(request),
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Get revenue data
   */
  async getRevenueData(period: string, tenantId?: string): Promise<ApiResponse<ChartData>> {
    try {
      const params = { period, tenant_id: tenantId };
      const response = await apiClient.get(`${this.baseUrl}/revenue`, params);
      return response.data;
    } catch (error) {
      return {
        success: false,
        data: this.generateMockRevenueData(period),
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Get user activity data
   */
  async getUserActivityData(period: string, tenantId?: string): Promise<ApiResponse<ChartData>> {
    try {
      const params = { period, tenant_id: tenantId };
      const response = await apiClient.get(`${this.baseUrl}/user-activity`, params);
      return response.data;
    } catch (error) {
      return {
        success: false,
        data: this.generateMockUserActivityData(period),
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Get system performance data
   */
  async getSystemPerformanceData(period: string): Promise<ApiResponse<ChartData>> {
    try {
      const params = { period };
      const response = await apiClient.get(`${this.baseUrl}/system-performance`, params);
      return response.data;
    } catch (error) {
      return {
        success: false,
        data: this.generateMockSystemPerformanceData(period),
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Generate mock data for development
   */
  private generateMockData(request: ChartRequest): ChartData {
    const { type, period, dataKey } = request;
    const dataPoints = this.getDataPointsForPeriod(period);
    
    const labels = dataPoints.map(point => point.date);
    const data = dataPoints.map(point => point.value);
    
    return {
      labels,
      datasets: [{
        label: this.getDataKeyLabel(dataKey),
        data,
        backgroundColor: this.getBackgroundColor(type, dataKey),
        borderColor: this.getBorderColor(dataKey),
        borderWidth: 2
      }]
    };
  }

  /**
   * Generate mock revenue data
   */
  private generateMockRevenueData(period: string): ChartData {
    const dataPoints = this.getDataPointsForPeriod(period);
    const labels = dataPoints.map(point => point.date);
    const data = dataPoints.map(point => point.value * 1000); // Convert to revenue
    
    return {
      labels,
      datasets: [{
        label: 'Revenue ($)',
        data,
        backgroundColor: 'rgba(16, 185, 129, 0.2)',
        borderColor: 'rgba(16, 185, 129, 1)',
        borderWidth: 2
      }]
    };
  }

  /**
   * Generate mock user activity data
   */
  private generateMockUserActivityData(period: string): ChartData {
    const dataPoints = this.getDataPointsForPeriod(period);
    const labels = dataPoints.map(point => point.date);
    const data = dataPoints.map(point => Math.floor(point.value / 10)); // Convert to user count
    
    return {
      labels,
      datasets: [{
        label: 'Active Users',
        data,
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 2
      }]
    };
  }

  /**
   * Generate mock system performance data
   */
  private generateMockSystemPerformanceData(period: string): ChartData {
    const dataPoints = this.getDataPointsForPeriod(period);
    const labels = dataPoints.map(point => point.date);
    const data = dataPoints.map(point => Math.random() * 100); // Random performance percentage
    
    return {
      labels,
      datasets: [{
        label: 'System Performance (%)',
        data,
        backgroundColor: 'rgba(245, 158, 11, 0.2)',
        borderColor: 'rgba(245, 158, 11, 1)',
        borderWidth: 2
      }]
    };
  }

  /**
   * Get data points for a specific period
   */
  private getDataPointsForPeriod(period: string): ChartDataPoint[] {
    const now = new Date();
    const points: ChartDataPoint[] = [];
    
    let days: number;
    switch (period) {
      case '7d': days = 7; break;
      case '30d': days = 30; break;
      case '90d': days = 90; break;
      case '1y': days = 365; break;
      default: days = 30;
    }
    
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date(now);
      date.setDate(date.getDate() - i);
      
      points.push({
        date: date.toISOString().split('T')[0],
        value: Math.floor(Math.random() * 1000) + 100
      });
    }
    
    return points;
  }

  /**
   * Get label for data key
   */
  private getDataKeyLabel(dataKey: string): string {
    const labels: Record<string, string> = {
      'api_calls': 'API Calls',
      'storage': 'Storage (GB)',
      'users': 'Active Users',
      'revenue': 'Revenue ($)'
    };
    return labels[dataKey] || dataKey;
  }

  /**
   * Get background color for chart type and data key
   */
  private getBackgroundColor(type: string, dataKey: string): string | string[] {
    const colors: Record<string, string> = {
      'api_calls': 'rgba(59, 130, 246, 0.2)',
      'storage': 'rgba(245, 158, 11, 0.2)',
      'users': 'rgba(16, 185, 129, 0.2)',
      'revenue': 'rgba(139, 92, 246, 0.2)'
    };
    
    if (type === 'pie') {
      return [
        'rgba(59, 130, 246, 0.8)',
        'rgba(16, 185, 129, 0.8)',
        'rgba(245, 158, 11, 0.8)',
        'rgba(239, 68, 68, 0.8)',
        'rgba(139, 92, 246, 0.8)'
      ];
    }
    
    return colors[dataKey] || 'rgba(59, 130, 246, 0.2)';
  }

  /**
   * Get border color for data key
   */
  private getBorderColor(dataKey: string): string {
    const colors: Record<string, string> = {
      'api_calls': 'rgba(59, 130, 246, 1)',
      'storage': 'rgba(245, 158, 11, 1)',
      'users': 'rgba(16, 185, 129, 1)',
      'revenue': 'rgba(139, 92, 246, 1)'
    };
    return colors[dataKey] || 'rgba(59, 130, 246, 1)';
  }
}

// ============================================================================
// EXPORT INSTANCE
// ============================================================================

export const chartService = new ChartService();
