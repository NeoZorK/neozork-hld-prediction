/**
 * Vuex module for analytics state management
 * 
 * This module handles dashboard statistics, analytics data,
 * and reporting functionality.
 */

import { Module } from 'vuex';
import { AnalyticsState, DashboardStats, AnalyticsData } from '../../types';
import { analyticsAPI } from '../../services/api';

// ============================================================================
// STATE
// ============================================================================

const state: AnalyticsState = {
  stats: null,
  analyticsData: null,
  isLoading: false,
  error: null,
  period: '30d',
  filters: {}
};

// ============================================================================
// MUTATIONS
// ============================================================================

const mutations = {
  SET_LOADING(state: AnalyticsState, loading: boolean) {
    state.isLoading = loading;
  },

  SET_STATS(state: AnalyticsState, stats: DashboardStats | null) {
    state.stats = stats;
  },

  SET_ANALYTICS_DATA(state: AnalyticsState, data: AnalyticsData | null) {
    state.analyticsData = data;
  },

  SET_PERIOD(state: AnalyticsState, period: string) {
    state.period = period;
  },

  SET_FILTERS(state: AnalyticsState, filters: Record<string, any>) {
    state.filters = { ...state.filters, ...filters };
  },

  CLEAR_FILTERS(state: AnalyticsState) {
    state.filters = {};
  },

  SET_ERROR(state: AnalyticsState, error: string | null) {
    state.error = error;
  },

  CLEAR_ERROR(state: AnalyticsState) {
    state.error = null;
  }
};

// ============================================================================
// ACTIONS
// ============================================================================

const actions = {
  /**
   * Fetch dashboard statistics
   */
  async fetchDashboardStats({ commit }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const stats = await analyticsAPI.getDashboardStats();
      
      commit('SET_STATS', stats);
      
      return stats;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch dashboard stats');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Fetch analytics data
   */
  async fetchAnalyticsData({ commit, state }, params: any = {}) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const data = await analyticsAPI.getAnalyticsData({
        period: state.period,
        ...state.filters,
        ...params
      });
      
      commit('SET_ANALYTICS_DATA', data);
      
      return data;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch analytics data');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Fetch revenue analytics
   */
  async fetchRevenueAnalytics({ commit, state }, params: any = {}) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const data = await analyticsAPI.getRevenueAnalytics({
        period: state.period,
        ...state.filters,
        ...params
      });
      
      return data;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch revenue analytics');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Fetch user analytics
   */
  async fetchUserAnalytics({ commit, state }, params: any = {}) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const data = await analyticsAPI.getUserAnalytics({
        period: state.period,
        ...state.filters,
        ...params
      });
      
      return data;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch user analytics');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Fetch fund performance analytics
   */
  async fetchFundPerformanceAnalytics({ commit, state }, params: any = {}) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const data = await analyticsAPI.getFundPerformanceAnalytics({
        period: state.period,
        ...state.filters,
        ...params
      });
      
      return data;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch fund performance analytics');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Set period
   */
  setPeriod({ commit }, period: string) {
    commit('SET_PERIOD', period);
  },

  /**
   * Set filters
   */
  setFilters({ commit }, filters: Record<string, any>) {
    commit('SET_FILTERS', filters);
  },

  /**
   * Clear filters
   */
  clearFilters({ commit }) {
    commit('CLEAR_FILTERS');
  },

  /**
   * Clear error
   */
  clearError({ commit }) {
    commit('CLEAR_ERROR');
  }
};

// ============================================================================
// GETTERS
// ============================================================================

const getters = {
  /**
   * Get dashboard stats
   */
  stats: (state: AnalyticsState) => state.stats,

  /**
   * Get analytics data
   */
  analyticsData: (state: AnalyticsState) => state.analyticsData,

  /**
   * Check if loading
   */
  isLoading: (state: AnalyticsState) => state.isLoading,

  /**
   * Get error message
   */
  error: (state: AnalyticsState) => state.error,

  /**
   * Get current period
   */
  period: (state: AnalyticsState) => state.period,

  /**
   * Get current filters
   */
  filters: (state: AnalyticsState) => state.filters,

  /**
   * Get total tenants count
   */
  totalTenants: (state: AnalyticsState) => state.stats?.total_tenants || 0,

  /**
   * Get total users count
   */
  totalUsers: (state: AnalyticsState) => state.stats?.total_users || 0,

  /**
   * Get total funds count
   */
  totalFunds: (state: AnalyticsState) => state.stats?.total_funds || 0,

  /**
   * Get total AUM
   */
  totalAUM: (state: AnalyticsState) => state.stats?.total_assets_under_management || 0,

  /**
   * Get total revenue
   */
  totalRevenue: (state: AnalyticsState) => state.stats?.total_revenue || 0,

  /**
   * Get monthly revenue
   */
  monthlyRevenue: (state: AnalyticsState) => state.stats?.monthly_revenue || 0,

  /**
   * Get revenue growth
   */
  revenueGrowth: (state: AnalyticsState) => state.stats?.revenue_growth || 0,

  /**
   * Get active subscriptions count
   */
  activeSubscriptions: (state: AnalyticsState) => state.stats?.active_subscriptions || 0,

  /**
   * Get churn rate
   */
  churnRate: (state: AnalyticsState) => state.stats?.churn_rate || 0,

  /**
   * Get user growth
   */
  userGrowth: (state: AnalyticsState) => state.stats?.user_growth || 0,

  /**
   * Get average fund performance
   */
  averageFundPerformance: (state: AnalyticsState) => state.stats?.fund_performance_avg || 0,

  /**
   * Get system health
   */
  systemHealth: (state: AnalyticsState) => state.stats?.system_health,

  /**
   * Check if system is healthy
   */
  isSystemHealthy: (state: AnalyticsState) => {
    const health = state.stats?.system_health;
    return health?.status === 'healthy';
  },

  /**
   * Get system uptime
   */
  systemUptime: (state: AnalyticsState) => {
    const health = state.stats?.system_health;
    return health?.uptime || 0;
  },

  /**
   * Get system response time
   */
  systemResponseTime: (state: AnalyticsState) => {
    const health = state.stats?.system_health;
    return health?.response_time || 0;
  },

  /**
   * Get system error rate
   */
  systemErrorRate: (state: AnalyticsState) => {
    const health = state.stats?.system_health;
    return health?.error_rate || 0;
  },

  /**
   * Get formatted revenue
   */
  formattedRevenue: (state: AnalyticsState) => {
    const revenue = state.stats?.total_revenue || 0;
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(revenue);
  },

  /**
   * Get formatted AUM
   */
  formattedAUM: (state: AnalyticsState) => {
    const aum = state.stats?.total_assets_under_management || 0;
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(aum);
  },

  /**
   * Get formatted growth percentage
   */
  formattedGrowth: (state: AnalyticsState) => {
    const growth = state.stats?.revenue_growth || 0;
    const sign = growth >= 0 ? '+' : '';
    return `${sign}${growth.toFixed(1)}%`;
  },

  /**
   * Get formatted churn rate
   */
  formattedChurnRate: (state: AnalyticsState) => {
    const churn = state.stats?.churn_rate || 0;
    return `${churn.toFixed(1)}%`;
  }
};

// ============================================================================
// MODULE EXPORT
// ============================================================================

const analyticsModule: Module<AnalyticsState, any> = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default analyticsModule;
