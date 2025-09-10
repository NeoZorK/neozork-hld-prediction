/**
 * Vuex module for tenant management state
 * 
 * This module handles tenant data, CRUD operations,
 * and tenant-related state management.
 */

import { Module } from 'vuex';
import { TenantState, Tenant, PaginationInfo } from '../../types';
import { tenantAPI } from '../../services/api';

// ============================================================================
// STATE
// ============================================================================

const state: TenantState = {
  tenants: [],
  selectedTenant: null,
  isLoading: false,
  error: null,
  pagination: null,
  filters: {}
};

// ============================================================================
// MUTATIONS
// ============================================================================

const mutations = {
  SET_LOADING(state: TenantState, loading: boolean) {
    state.isLoading = loading;
  },

  SET_TENANTS(state: TenantState, tenants: Tenant[]) {
    state.tenants = tenants;
  },

  SET_SELECTED_TENANT(state: TenantState, tenant: Tenant | null) {
    state.selectedTenant = tenant;
  },

  SET_PAGINATION(state: TenantState, pagination: PaginationInfo | null) {
    state.pagination = pagination;
  },

  SET_FILTERS(state: TenantState, filters: Record<string, any>) {
    state.filters = { ...state.filters, ...filters };
  },

  CLEAR_FILTERS(state: TenantState) {
    state.filters = {};
  },

  SET_ERROR(state: TenantState, error: string | null) {
    state.error = error;
  },

  CLEAR_ERROR(state: TenantState) {
    state.error = null;
  },

  ADD_TENANT(state: TenantState, tenant: Tenant) {
    state.tenants.unshift(tenant);
  },

  UPDATE_TENANT(state: TenantState, updatedTenant: Tenant) {
    const index = state.tenants.findIndex(tenant => tenant.id === updatedTenant.id);
    if (index !== -1) {
      state.tenants.splice(index, 1, updatedTenant);
    }
    if (state.selectedTenant?.id === updatedTenant.id) {
      state.selectedTenant = updatedTenant;
    }
  },

  REMOVE_TENANT(state: TenantState, tenantId: string) {
    state.tenants = state.tenants.filter(tenant => tenant.id !== tenantId);
    if (state.selectedTenant?.id === tenantId) {
      state.selectedTenant = null;
    }
  }
};

// ============================================================================
// ACTIONS
// ============================================================================

const actions = {
  /**
   * Fetch tenants with pagination and filtering
   */
  async fetchTenants({ commit }, params: any = {}) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const response = await tenantAPI.getTenants(params);
      
      commit('SET_TENANTS', response.tenants);
      commit('SET_PAGINATION', response.pagination);
      
      return response;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch tenants');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Get tenant by ID
   */
  async fetchTenant({ commit }, tenantId: string) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const tenant = await tenantAPI.getTenant(tenantId);
      
      commit('SET_SELECTED_TENANT', tenant);
      
      return tenant;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch tenant');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Create new tenant
   */
  async createTenant({ commit }, tenantData: Partial<Tenant>) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const tenant = await tenantAPI.createTenant(tenantData);
      
      commit('ADD_TENANT', tenant);
      
      return tenant;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to create tenant');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Update tenant
   */
  async updateTenant({ commit }, { tenantId, tenantData }: { tenantId: string; tenantData: Partial<Tenant> }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const tenant = await tenantAPI.updateTenant(tenantId, tenantData);
      
      commit('UPDATE_TENANT', tenant);
      
      return tenant;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to update tenant');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Delete tenant
   */
  async deleteTenant({ commit }, tenantId: string) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      await tenantAPI.deleteTenant(tenantId);
      
      commit('REMOVE_TENANT', tenantId);
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to delete tenant');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Suspend tenant
   */
  async suspendTenant({ commit }, { tenantId, reason }: { tenantId: string; reason: string }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      await tenantAPI.suspendTenant(tenantId, reason);
      
      // Refresh tenant data
      const tenant = await tenantAPI.getTenant(tenantId);
      commit('UPDATE_TENANT', tenant);
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to suspend tenant');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Activate tenant
   */
  async activateTenant({ commit }, tenantId: string) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      await tenantAPI.activateTenant(tenantId);
      
      // Refresh tenant data
      const tenant = await tenantAPI.getTenant(tenantId);
      commit('UPDATE_TENANT', tenant);
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to activate tenant');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Get tenant usage
   */
  async fetchTenantUsage({ commit }, tenantId: string) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const usage = await tenantAPI.getTenantUsage(tenantId);
      
      return usage;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch tenant usage');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Update tenant settings
   */
  async updateTenantSettings({ commit }, { tenantId, settings }: { tenantId: string; settings: any }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      await tenantAPI.updateTenantSettings(tenantId, settings);
      
      // Refresh tenant data
      const tenant = await tenantAPI.getTenant(tenantId);
      commit('UPDATE_TENANT', tenant);
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to update tenant settings');
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
   * Get all tenants
   */
  tenants: (state: TenantState) => state.tenants,

  /**
   * Get selected tenant
   */
  selectedTenant: (state: TenantState) => state.selectedTenant,

  /**
   * Check if loading
   */
  isLoading: (state: TenantState) => state.isLoading,

  /**
   * Get error message
   */
  error: (state: TenantState) => state.error,

  /**
   * Get pagination info
   */
  pagination: (state: TenantState) => state.pagination,

  /**
   * Get current filters
   */
  filters: (state: TenantState) => state.filters,

  /**
   * Get tenants by status
   */
  tenantsByStatus: (state: TenantState) => (status: string) => {
    return state.tenants.filter(tenant => tenant.status === status);
  },

  /**
   * Get tenants by plan
   */
  tenantsByPlan: (state: TenantState) => (plan: string) => {
    return state.tenants.filter(tenant => tenant.plan === plan);
  },

  /**
   * Get active tenants count
   */
  activeTenantsCount: (state: TenantState) => {
    return state.tenants.filter(tenant => tenant.status === 'active').length;
  },

  /**
   * Get suspended tenants count
   */
  suspendedTenantsCount: (state: TenantState) => {
    return state.tenants.filter(tenant => tenant.status === 'suspended').length;
  },

  /**
   * Get total tenants count
   */
  totalTenantsCount: (state: TenantState) => state.tenants.length,

  /**
   * Get tenant by ID
   */
  getTenantById: (state: TenantState) => (id: string) => {
    return state.tenants.find(tenant => tenant.id === id);
  },

  /**
   * Search tenants
   */
  searchTenants: (state: TenantState) => (query: string) => {
    const lowercaseQuery = query.toLowerCase();
    return state.tenants.filter(tenant => 
      tenant.name.toLowerCase().includes(lowercaseQuery) ||
      tenant.domain.toLowerCase().includes(lowercaseQuery) ||
      tenant.owner_email.toLowerCase().includes(lowercaseQuery)
    );
  }
};

// ============================================================================
// MODULE EXPORT
// ============================================================================

const tenantsModule: Module<TenantState, any> = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default tenantsModule;
