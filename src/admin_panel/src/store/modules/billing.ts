/**
 * Vuex module for billing state management
 * 
 * This module handles billing records, revenue reports,
 * and financial data management.
 */

import { Module } from 'vuex';
import { BillingState, BillingRecord, RevenueReport, PaginationInfo } from '../../types';
import { billingAPI } from '../../services/api';

// ============================================================================
// STATE
// ============================================================================

const state: BillingState = {
  records: [],
  revenueReport: null,
  isLoading: false,
  error: null,
  pagination: null,
  filters: {}
};

// ============================================================================
// MUTATIONS
// ============================================================================

const mutations = {
  SET_LOADING(state: BillingState, loading: boolean) {
    state.isLoading = loading;
  },

  SET_RECORDS(state: BillingState, records: BillingRecord[]) {
    state.records = records;
  },

  SET_REVENUE_REPORT(state: BillingState, report: RevenueReport | null) {
    state.revenueReport = report;
  },

  SET_PAGINATION(state: BillingState, pagination: PaginationInfo | null) {
    state.pagination = pagination;
  },

  SET_FILTERS(state: BillingState, filters: Record<string, any>) {
    state.filters = { ...state.filters, ...filters };
  },

  CLEAR_FILTERS(state: BillingState) {
    state.filters = {};
  },

  SET_ERROR(state: BillingState, error: string | null) {
    state.error = error;
  },

  CLEAR_ERROR(state: BillingState) {
    state.error = null;
  },

  ADD_RECORD(state: BillingState, record: BillingRecord) {
    state.records.unshift(record);
  },

  UPDATE_RECORD(state: BillingState, updatedRecord: BillingRecord) {
    const index = state.records.findIndex(record => record.id === updatedRecord.id);
    if (index !== -1) {
      state.records.splice(index, 1, updatedRecord);
    }
  }
};

// ============================================================================
// ACTIONS
// ============================================================================

const actions = {
  /**
   * Fetch billing records
   */
  async fetchBillingRecords({ commit }, params: any = {}) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const response = await billingAPI.getBillingRecords(params);
      
      commit('SET_RECORDS', response.records);
      commit('SET_PAGINATION', response.pagination);
      
      return response;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch billing records');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Fetch revenue report
   */
  async fetchRevenueReport({ commit }, params: any = {}) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const report = await billingAPI.getRevenueReport(params);
      
      commit('SET_REVENUE_REPORT', report);
      
      return report;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch revenue report');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Create billing record
   */
  async createBillingRecord({ commit }, recordData: Partial<BillingRecord>) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const record = await billingAPI.createBillingRecord(recordData);
      
      commit('ADD_RECORD', record);
      
      return record;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to create billing record');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Update billing record
   */
  async updateBillingRecord({ commit }, { recordId, recordData }: { recordId: string; recordData: Partial<BillingRecord> }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const record = await billingAPI.updateBillingRecord(recordId, recordData);
      
      commit('UPDATE_RECORD', record);
      
      return record;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to update billing record');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Mark billing record as paid
   */
  async markBillingRecordPaid({ commit }, { recordId, paymentData }: { recordId: string; paymentData: any }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      await billingAPI.markBillingRecordPaid(recordId, paymentData);
      
      // Refresh record data
      const response = await billingAPI.getBillingRecords({ id: recordId });
      if (response.records.length > 0) {
        commit('UPDATE_RECORD', response.records[0]);
      }
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to mark billing record as paid');
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
   * Get all billing records
   */
  records: (state: BillingState) => state.records,

  /**
   * Get revenue report
   */
  revenueReport: (state: BillingState) => state.revenueReport,

  /**
   * Check if loading
   */
  isLoading: (state: BillingState) => state.isLoading,

  /**
   * Get error message
   */
  error: (state: BillingState) => state.error,

  /**
   * Get pagination info
   */
  pagination: (state: BillingState) => state.pagination,

  /**
   * Get current filters
   */
  filters: (state: BillingState) => state.filters,

  /**
   * Get records by status
   */
  recordsByStatus: (state: BillingState) => (status: string) => {
    return state.records.filter(record => record.status === status);
  },

  /**
   * Get pending records count
   */
  pendingRecordsCount: (state: BillingState) => {
    return state.records.filter(record => record.status === 'pending').length;
  },

  /**
   * Get paid records count
   */
  paidRecordsCount: (state: BillingState) => {
    return state.records.filter(record => record.status === 'paid').length;
  },

  /**
   * Get overdue records count
   */
  overdueRecordsCount: (state: BillingState) => {
    return state.records.filter(record => record.status === 'overdue').length;
  },

  /**
   * Get total records count
   */
  totalRecordsCount: (state: BillingState) => state.records.length,

  /**
   * Get total revenue
   */
  totalRevenue: (state: BillingState) => {
    return state.records
      .filter(record => record.status === 'paid')
      .reduce((total, record) => total + record.amount, 0);
  },

  /**
   * Get pending revenue
   */
  pendingRevenue: (state: BillingState) => {
    return state.records
      .filter(record => record.status === 'pending')
      .reduce((total, record) => total + record.amount, 0);
  },

  /**
   * Get overdue revenue
   */
  overdueRevenue: (state: BillingState) => {
    return state.records
      .filter(record => record.status === 'overdue')
      .reduce((total, record) => total + record.amount, 0);
  },

  /**
   * Get formatted total revenue
   */
  formattedTotalRevenue: (state: BillingState) => {
    const total = state.records
      .filter(record => record.status === 'paid')
      .reduce((total, record) => total + record.amount, 0);
    
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(total);
  },

  /**
   * Get record by ID
   */
  getRecordById: (state: BillingState) => (id: string) => {
    return state.records.find(record => record.id === id);
  },

  /**
   * Search records
   */
  searchRecords: (state: BillingState) => (query: string) => {
    const lowercaseQuery = query.toLowerCase();
    return state.records.filter(record => 
      record.tenant_name.toLowerCase().includes(lowercaseQuery) ||
      record.description.toLowerCase().includes(lowercaseQuery) ||
      record.id.toLowerCase().includes(lowercaseQuery)
    );
  }
};

// ============================================================================
// MODULE EXPORT
// ============================================================================

const billingModule: Module<BillingState, any> = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default billingModule;
