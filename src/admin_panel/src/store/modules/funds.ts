/**
 * Vuex module for fund management state
 * 
 * This module handles fund data, CRUD operations,
 * and fund-related state management.
 */

import { Module } from 'vuex';
import { FundState, Fund, PaginationInfo } from '../../types';
import { fundAPI } from '../../services/api';

// ============================================================================
// STATE
// ============================================================================

const state: FundState = {
  funds: [],
  selectedFund: null,
  isLoading: false,
  error: null,
  pagination: null,
  filters: {}
};

// ============================================================================
// MUTATIONS
// ============================================================================

const mutations = {
  SET_LOADING(state: FundState, loading: boolean) {
    state.isLoading = loading;
  },

  SET_FUNDS(state: FundState, funds: Fund[]) {
    state.funds = funds;
  },

  SET_SELECTED_FUND(state: FundState, fund: Fund | null) {
    state.selectedFund = fund;
  },

  SET_PAGINATION(state: FundState, pagination: PaginationInfo | null) {
    state.pagination = pagination;
  },

  SET_FILTERS(state: FundState, filters: Record<string, any>) {
    state.filters = { ...state.filters, ...filters };
  },

  CLEAR_FILTERS(state: FundState) {
    state.filters = {};
  },

  SET_ERROR(state: FundState, error: string | null) {
    state.error = error;
  },

  CLEAR_ERROR(state: FundState) {
    state.error = null;
  },

  UPDATE_FUND(state: FundState, updatedFund: Fund) {
    const index = state.funds.findIndex(fund => fund.id === updatedFund.id);
    if (index !== -1) {
      state.funds.splice(index, 1, updatedFund);
    }
    if (state.selectedFund?.id === updatedFund.id) {
      state.selectedFund = updatedFund;
    }
  }
};

// ============================================================================
// ACTIONS
// ============================================================================

const actions = {
  /**
   * Fetch funds with pagination and filtering
   */
  async fetchFunds({ commit }, params: any = {}) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const response = await fundAPI.getFunds(params);
      
      commit('SET_FUNDS', response.funds);
      commit('SET_PAGINATION', response.pagination);
      
      return response;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch funds');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Get fund by ID
   */
  async fetchFund({ commit }, fundId: string) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const fund = await fundAPI.getFund(fundId);
      
      commit('SET_SELECTED_FUND', fund);
      
      return fund;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch fund');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Update fund
   */
  async updateFund({ commit }, { fundId, fundData }: { fundId: string; fundData: Partial<Fund> }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const fund = await fundAPI.updateFund(fundId, fundData);
      
      commit('UPDATE_FUND', fund);
      
      return fund;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to update fund');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Suspend fund
   */
  async suspendFund({ commit }, { fundId, reason }: { fundId: string; reason: string }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      await fundAPI.suspendFund(fundId, reason);
      
      // Refresh fund data
      const fund = await fundAPI.getFund(fundId);
      commit('UPDATE_FUND', fund);
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to suspend fund');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Activate fund
   */
  async activateFund({ commit }, fundId: string) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      await fundAPI.activateFund(fundId);
      
      // Refresh fund data
      const fund = await fundAPI.getFund(fundId);
      commit('UPDATE_FUND', fund);
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to activate fund');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Get fund compliance
   */
  async fetchFundCompliance({ commit }, fundId: string) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const compliance = await fundAPI.getFundCompliance(fundId);
      
      return compliance;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch fund compliance');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Update fund compliance
   */
  async updateFundCompliance({ commit }, { fundId, complianceData }: { fundId: string; complianceData: any }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      await fundAPI.updateFundCompliance(fundId, complianceData);
      
      // Refresh fund data
      const fund = await fundAPI.getFund(fundId);
      commit('UPDATE_FUND', fund);
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to update fund compliance');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
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
   * Get all funds
   */
  funds: (state: FundState) => state.funds,

  /**
   * Get selected fund
   */
  selectedFund: (state: FundState) => state.selectedFund,

  /**
   * Check if loading
   */
  isLoading: (state: FundState) => state.isLoading,

  /**
   * Get error message
   */
  error: (state: FundState) => state.error,

  /**
   * Get pagination info
   */
  pagination: (state: FundState) => state.pagination,

  /**
   * Get current filters
   */
  filters: (state: FundState) => state.filters,

  /**
   * Get funds by status
   */
  fundsByStatus: (state: FundState) => (status: string) => {
    return state.funds.filter(fund => fund.status === status);
  },

  /**
   * Get funds by type
   */
  fundsByType: (state: FundState) => (type: string) => {
    return state.funds.filter(fund => fund.fund_type === type);
  },

  /**
   * Get funds by risk level
   */
  fundsByRiskLevel: (state: FundState) => (riskLevel: string) => {
    return state.funds.filter(fund => fund.risk_level === riskLevel);
  },

  /**
   * Get funds by tenant
   */
  fundsByTenant: (state: FundState) => (tenantId: string) => {
    return state.funds.filter(fund => fund.tenant_id === tenantId);
  },

  /**
   * Get active funds count
   */
  activeFundsCount: (state: FundState) => {
    return state.funds.filter(fund => fund.status === 'active').length;
  },

  /**
   * Get suspended funds count
   */
  suspendedFundsCount: (state: FundState) => {
    return state.funds.filter(fund => fund.status === 'suspended').length;
  },

  /**
   * Get total funds count
   */
  totalFundsCount: (state: FundState) => state.funds.length,

  /**
   * Get fund by ID
   */
  getFundById: (state: FundState) => (id: string) => {
    return state.funds.find(fund => fund.id === id);
  },

  /**
   * Search funds
   */
  searchFunds: (state: FundState) => (query: string) => {
    const lowercaseQuery = query.toLowerCase();
    return state.funds.filter(fund => 
      fund.name.toLowerCase().includes(lowercaseQuery) ||
      fund.description.toLowerCase().includes(lowercaseQuery) ||
      fund.tenant_name.toLowerCase().includes(lowercaseQuery)
    );
  }
};

// ============================================================================
// MODULE EXPORT
// ============================================================================

const fundsModule: Module<FundState, any> = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default fundsModule;
