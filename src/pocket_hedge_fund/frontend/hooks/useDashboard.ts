/**
 * Dashboard Hook for Pocket Hedge Fund React Dashboard
 * 
 * This hook provides dashboard data management, statistics fetching,
 * and real-time updates for the main dashboard view.
 */

import { useState, useEffect, useCallback } from 'react';
import { 
  DashboardStats, 
  DashboardChart, 
  Fund, 
  FundPerformance, 
  ChartDataPoint,
  ApiError 
} from '../types';
import { fundAPI, systemAPI } from '../services/api';

// ============================================================================
// DASHBOARD DATA INTERFACE
// ============================================================================

interface DashboardData {
  stats: DashboardStats | null;
  charts: DashboardChart[];
  recentFunds: Fund[];
  topPerformers: Fund[];
  isLoading: boolean;
  error: string | null;
  lastUpdated: string | null;
}

// ============================================================================
// USE DASHBOARD HOOK
// ============================================================================

export const useDashboard = () => {
  const [data, setData] = useState<DashboardData>({
    stats: null,
    charts: [],
    recentFunds: [],
    topPerformers: [],
    isLoading: true,
    error: null,
    lastUpdated: null
  });

  // ============================================================================
  // ERROR HANDLING
  // ============================================================================

  const handleError = useCallback((error: any) => {
    console.error('Dashboard Error:', error);
    
    if (error instanceof ApiError) {
      setData(prev => ({ ...prev, error: error.message }));
    } else if (error.message) {
      setData(prev => ({ ...prev, error: error.message }));
    } else {
      setData(prev => ({ ...prev, error: 'Failed to load dashboard data' }));
    }
  }, []);

  // ============================================================================
  // DATA FETCHING
  // ============================================================================

  const fetchDashboardStats = useCallback(async (): Promise<DashboardStats> => {
    try {
      // Fetch funds data
      const fundsResponse = await fundAPI.getFunds({ page_size: 100 });
      const funds = fundsResponse.items;

      // Calculate statistics
      const totalFunds = funds.length;
      const totalInvestors = funds.reduce((sum, fund) => sum + fund.current_investors, 0);
      const totalAUM = funds.reduce((sum, fund) => sum + fund.current_value, 0);
      
      // Calculate average return
      const totalReturn = funds.reduce((sum, fund) => {
        const returnPercent = ((fund.current_value - fund.initial_capital) / fund.initial_capital) * 100;
        return sum + returnPercent;
      }, 0);
      const avgReturn = funds.length > 0 ? totalReturn / funds.length : 0;

      // Count active strategies (simplified - would need actual strategy data)
      const activeStrategies = funds.filter(fund => fund.status === 'active').length;

      // Calculate risk score (simplified)
      const riskScore = funds.reduce((sum, fund) => {
        const riskValue = fund.risk_level === 'low' ? 1 : fund.risk_level === 'medium' ? 2 : 3;
        return sum + riskValue;
      }, 0) / funds.length;

      return {
        total_funds: totalFunds,
        total_investors: totalInvestors,
        total_assets_under_management: totalAUM,
        total_return_percentage: avgReturn,
        active_strategies: activeStrategies,
        risk_score: riskScore
      };
    } catch (error) {
      handleError(error);
      throw error;
    }
  }, [handleError]);

  const fetchDashboardCharts = useCallback(async (): Promise<DashboardChart[]> => {
    try {
      const charts: DashboardChart[] = [];

      // Performance over time chart
      const performanceData: ChartDataPoint[] = [];
      const fundsResponse = await fundAPI.getFunds({ page_size: 10 });
      
      for (const fund of fundsResponse.items) {
        try {
          const performance = await fundAPI.getFundPerformance(fund.fund_id, 30);
          if (performance.length > 0) {
            const latest = performance[performance.length - 1];
            performanceData.push({
              date: latest.snapshot_date,
              value: latest.total_return_percentage,
              label: fund.name
            });
          }
        } catch (error) {
          console.warn(`Failed to fetch performance for fund ${fund.fund_id}:`, error);
        }
      }

      if (performanceData.length > 0) {
        charts.push({
          title: 'Fund Performance (30 Days)',
          type: 'line',
          data: performanceData,
          color: '#3B82F6',
          height: 300
        });
      }

      // Asset allocation pie chart
      const allocationData: ChartDataPoint[] = [];
      for (const fund of fundsResponse.items) {
        allocationData.push({
          date: fund.fund_type,
          value: fund.current_value,
          label: fund.name
        });
      }

      if (allocationData.length > 0) {
        charts.push({
          title: 'Assets Under Management by Fund Type',
          type: 'pie',
          data: allocationData,
          color: '#10B981',
          height: 300
        });
      }

      return charts;
    } catch (error) {
      handleError(error);
      return [];
    }
  }, [handleError]);

  const fetchRecentFunds = useCallback(async (): Promise<Fund[]> => {
    try {
      const response = await fundAPI.getFunds({ 
        page_size: 5,
        status: 'active'
      });
      return response.items;
    } catch (error) {
      handleError(error);
      return [];
    }
  }, [handleError]);

  const fetchTopPerformers = useCallback(async (): Promise<Fund[]> => {
    try {
      const response = await fundAPI.getFunds({ page_size: 100 });
      const funds = response.items;
      
      // Sort by performance and take top 5
      const topPerformers = funds
        .map(fund => ({
          ...fund,
          performance: ((fund.current_value - fund.initial_capital) / fund.initial_capital) * 100
        }))
        .sort((a, b) => b.performance - a.performance)
        .slice(0, 5);
      
      return topPerformers;
    } catch (error) {
      handleError(error);
      return [];
    }
  }, [handleError]);

  // ============================================================================
  // MAIN DATA LOADING
  // ============================================================================

  const loadDashboardData = useCallback(async () => {
    try {
      setData(prev => ({ ...prev, isLoading: true, error: null }));

      const [stats, charts, recentFunds, topPerformers] = await Promise.all([
        fetchDashboardStats(),
        fetchDashboardCharts(),
        fetchRecentFunds(),
        fetchTopPerformers()
      ]);

      setData({
        stats,
        charts,
        recentFunds,
        topPerformers,
        isLoading: false,
        error: null,
        lastUpdated: new Date().toISOString()
      });
    } catch (error) {
      setData(prev => ({ 
        ...prev, 
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to load dashboard data'
      }));
    }
  }, [fetchDashboardStats, fetchDashboardCharts, fetchRecentFunds, fetchTopPerformers]);

  // ============================================================================
  // REFRESH FUNCTIONALITY
  // ============================================================================

  const refresh = useCallback(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  // ============================================================================
  // AUTO-REFRESH
  // ============================================================================

  useEffect(() => {
    // Initial load
    loadDashboardData();

    // Auto-refresh every 5 minutes
    const interval = setInterval(() => {
      loadDashboardData();
    }, 5 * 60 * 1000);

    return () => clearInterval(interval);
  }, [loadDashboardData]);

  // ============================================================================
  // RETURN HOOK INTERFACE
  // ============================================================================

  return {
    // Data
    stats: data.stats,
    charts: data.charts,
    recentFunds: data.recentFunds,
    topPerformers: data.topPerformers,
    
    // State
    isLoading: data.isLoading,
    error: data.error,
    lastUpdated: data.lastUpdated,
    
    // Actions
    refresh,
    clearError: () => setData(prev => ({ ...prev, error: null }))
  };
};

// ============================================================================
// FUND PERFORMANCE HOOK
// ============================================================================

export const useFundPerformance = (fundId: string, days: number = 30) => {
  const [performance, setPerformance] = useState<FundPerformance[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPerformance = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const data = await fundAPI.getFundPerformance(fundId, days);
      setPerformance(data);
    } catch (error) {
      console.error('Fund Performance Error:', error);
      setError(error instanceof Error ? error.message : 'Failed to load performance data');
    } finally {
      setIsLoading(false);
    }
  }, [fundId, days]);

  useEffect(() => {
    if (fundId) {
      fetchPerformance();
    }
  }, [fundId, days, fetchPerformance]);

  return {
    performance,
    isLoading,
    error,
    refresh: fetchPerformance
  };
};

// ============================================================================
// SYSTEM STATUS HOOK
// ============================================================================

export const useSystemStatus = () => {
  const [status, setStatus] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const data = await systemAPI.getStatus();
      setStatus(data);
    } catch (error) {
      console.error('System Status Error:', error);
      setError(error instanceof Error ? error.message : 'Failed to load system status');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStatus();
    
    // Refresh every 30 seconds
    const interval = setInterval(fetchStatus, 30000);
    return () => clearInterval(interval);
  }, [fetchStatus]);

  return {
    status,
    isLoading,
    error,
    refresh: fetchStatus
  };
};

// ============================================================================
// EXPORT
// ============================================================================

export default useDashboard;
