/**
 * Vuex module for system management state
 * 
 * This module handles system configuration, health monitoring,
 * and system administration functionality.
 */

import { Module } from 'vuex';
import { SystemState, SystemConfig, SystemHealth } from '../../types';
import { systemAPI } from '../../services/api';

// ============================================================================
// STATE
// ============================================================================

const state: SystemState = {
  config: null,
  health: null,
  isLoading: false,
  error: null,
  isMaintenanceMode: false
};

// ============================================================================
// MUTATIONS
// ============================================================================

const mutations = {
  SET_LOADING(state: SystemState, loading: boolean) {
    state.isLoading = loading;
  },

  SET_CONFIG(state: SystemState, config: SystemConfig | null) {
    state.config = config;
  },

  SET_HEALTH(state: SystemState, health: SystemHealth | null) {
    state.health = health;
  },

  SET_MAINTENANCE_MODE(state: SystemState, enabled: boolean) {
    state.isMaintenanceMode = enabled;
  },

  SET_ERROR(state: SystemState, error: string | null) {
    state.error = error;
  },

  CLEAR_ERROR(state: SystemState) {
    state.error = null;
  }
};

// ============================================================================
// ACTIONS
// ============================================================================

const actions = {
  /**
   * Fetch system configuration
   */
  async fetchSystemConfig({ commit }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const config = await systemAPI.getSystemConfig();
      
      commit('SET_CONFIG', config);
      commit('SET_MAINTENANCE_MODE', config.general.maintenance_mode);
      
      return config;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch system config');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Update system configuration
   */
  async updateSystemConfig({ commit }, config: Partial<SystemConfig>) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const updatedConfig = await systemAPI.updateSystemConfig(config);
      
      commit('SET_CONFIG', updatedConfig);
      commit('SET_MAINTENANCE_MODE', updatedConfig.general.maintenance_mode);
      
      return updatedConfig;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to update system config');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Fetch system health
   */
  async fetchSystemHealth({ commit }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const health = await systemAPI.getSystemHealth();
      
      commit('SET_HEALTH', health);
      
      return health;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch system health');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Fetch system logs
   */
  async fetchSystemLogs({ commit }, params: any = {}) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const response = await systemAPI.getSystemLogs(params);
      
      return response;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch system logs');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Enable maintenance mode
   */
  async enableMaintenanceMode({ commit }, config: any) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      await systemAPI.enableMaintenanceMode(config);
      
      commit('SET_MAINTENANCE_MODE', true);
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to enable maintenance mode');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Disable maintenance mode
   */
  async disableMaintenanceMode({ commit }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      await systemAPI.disableMaintenanceMode();
      
      commit('SET_MAINTENANCE_MODE', false);
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to disable maintenance mode');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Fetch system metrics
   */
  async fetchSystemMetrics({ commit }, params: any = {}) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const metrics = await systemAPI.getSystemMetrics(params);
      
      return metrics;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch system metrics');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
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
   * Get system configuration
   */
  config: (state: SystemState) => state.config,

  /**
   * Get system health
   */
  health: (state: SystemState) => state.health,

  /**
   * Check if loading
   */
  isLoading: (state: SystemState) => state.isLoading,

  /**
   * Get error message
   */
  error: (state: SystemState) => state.error,

  /**
   * Check if maintenance mode is enabled
   */
  isMaintenanceMode: (state: SystemState) => state.isMaintenanceMode,

  /**
   * Check if system is healthy
   */
  isSystemHealthy: (state: SystemState) => {
    return state.health?.status === 'healthy';
  },

  /**
   * Get system status
   */
  systemStatus: (state: SystemState) => {
    return state.health?.status || 'unknown';
  },

  /**
   * Get system uptime
   */
  systemUptime: (state: SystemState) => {
    return state.health?.uptime || 0;
  },

  /**
   * Get system response time
   */
  systemResponseTime: (state: SystemState) => {
    return state.health?.response_time || 0;
  },

  /**
   * Get system error rate
   */
  systemErrorRate: (state: SystemState) => {
    return state.health?.error_rate || 0;
  },

  /**
   * Get database status
   */
  databaseStatus: (state: SystemState) => {
    return state.health?.database_status || 'unknown';
  },

  /**
   * Get Redis status
   */
  redisStatus: (state: SystemState) => {
    return state.health?.redis_status || 'unknown';
  },

  /**
   * Get API status
   */
  apiStatus: (state: SystemState) => {
    return state.health?.api_status || 'unknown';
  },

  /**
   * Get site name
   */
  siteName: (state: SystemState) => {
    return state.config?.general.site_name || 'Pocket Hedge Fund';
  },

  /**
   * Get site URL
   */
  siteUrl: (state: SystemState) => {
    return state.config?.general.site_url || '';
  },

  /**
   * Get support email
   */
  supportEmail: (state: SystemState) => {
    return state.config?.general.support_email || '';
  },

  /**
   * Get default language
   */
  defaultLanguage: (state: SystemState) => {
    return state.config?.general.default_language || 'en';
  },

  /**
   * Get default timezone
   */
  defaultTimezone: (state: SystemState) => {
    return state.config?.general.default_timezone || 'UTC';
  },

  /**
   * Check if registration is enabled
   */
  isRegistrationEnabled: (state: SystemState) => {
    return state.config?.general.registration_enabled || false;
  },

  /**
   * Check if email verification is required
   */
  isEmailVerificationRequired: (state: SystemState) => {
    return state.config?.general.email_verification_required || false;
  },

  /**
   * Get security configuration
   */
  securityConfig: (state: SystemState) => {
    return state.config?.security;
  },

  /**
   * Get feature configuration
   */
  featureConfig: (state: SystemState) => {
    return state.config?.features;
  },

  /**
   * Get integration configuration
   */
  integrationConfig: (state: SystemState) => {
    return state.config?.integrations;
  },

  /**
   * Get notification configuration
   */
  notificationConfig: (state: SystemState) => {
    return state.config?.notifications;
  }
};

// ============================================================================
// MODULE EXPORT
// ============================================================================

const systemModule: Module<SystemState, any> = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default systemModule;
