/**
 * Vuex module for user management state
 * 
 * This module handles user data, CRUD operations,
 * and user-related state management.
 */

import { Module } from 'vuex';
import { UserState, User, PaginationInfo } from '../../types';
import { userAPI } from '../../services/api';

// ============================================================================
// STATE
// ============================================================================

const state: UserState = {
  users: [],
  selectedUser: null,
  isLoading: false,
  error: null,
  pagination: null,
  filters: {}
};

// ============================================================================
// MUTATIONS
// ============================================================================

const mutations = {
  SET_LOADING(state: UserState, loading: boolean) {
    state.isLoading = loading;
  },

  SET_USERS(state: UserState, users: User[]) {
    state.users = users;
  },

  SET_SELECTED_USER(state: UserState, user: User | null) {
    state.selectedUser = user;
  },

  SET_PAGINATION(state: UserState, pagination: PaginationInfo | null) {
    state.pagination = pagination;
  },

  SET_FILTERS(state: UserState, filters: Record<string, any>) {
    state.filters = { ...state.filters, ...filters };
  },

  CLEAR_FILTERS(state: UserState) {
    state.filters = {};
  },

  SET_ERROR(state: UserState, error: string | null) {
    state.error = error;
  },

  CLEAR_ERROR(state: UserState) {
    state.error = null;
  },

  ADD_USER(state: UserState, user: User) {
    state.users.unshift(user);
  },

  UPDATE_USER(state: UserState, updatedUser: User) {
    const index = state.users.findIndex(user => user.id === updatedUser.id);
    if (index !== -1) {
      state.users.splice(index, 1, updatedUser);
    }
    if (state.selectedUser?.id === updatedUser.id) {
      state.selectedUser = updatedUser;
    }
  },

  REMOVE_USER(state: UserState, userId: string) {
    state.users = state.users.filter(user => user.id !== userId);
    if (state.selectedUser?.id === userId) {
      state.selectedUser = null;
    }
  }
};

// ============================================================================
// ACTIONS
// ============================================================================

const actions = {
  /**
   * Fetch users with pagination and filtering
   */
  async fetchUsers({ commit }, params: any = {}) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const response = await userAPI.getUsers(params);
      
      commit('SET_USERS', response.users);
      commit('SET_PAGINATION', response.pagination);
      
      return response;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch users');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Get user by ID
   */
  async fetchUser({ commit }, userId: string) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const user = await userAPI.getUser(userId);
      
      commit('SET_SELECTED_USER', user);
      
      return user;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch user');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Create new user
   */
  async createUser({ commit }, userData: Partial<User>) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const user = await userAPI.createUser(userData);
      
      commit('ADD_USER', user);
      
      return user;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to create user');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Update user
   */
  async updateUser({ commit }, { userId, userData }: { userId: string; userData: Partial<User> }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const user = await userAPI.updateUser(userId, userData);
      
      commit('UPDATE_USER', user);
      
      return user;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to update user');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Delete user
   */
  async deleteUser({ commit }, userId: string) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      await userAPI.deleteUser(userId);
      
      commit('REMOVE_USER', userId);
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to delete user');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Suspend user
   */
  async suspendUser({ commit }, { userId, reason }: { userId: string; reason: string }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      await userAPI.suspendUser(userId, reason);
      
      // Refresh user data
      const user = await userAPI.getUser(userId);
      commit('UPDATE_USER', user);
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to suspend user');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Activate user
   */
  async activateUser({ commit }, userId: string) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      await userAPI.activateUser(userId);
      
      // Refresh user data
      const user = await userAPI.getUser(userId);
      commit('UPDATE_USER', user);
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to activate user');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Reset user password
   */
  async resetUserPassword({ commit }, userId: string) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const response = await userAPI.resetUserPassword(userId);
      
      return response;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to reset user password');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Get user activity
   */
  async fetchUserActivity({ commit }, { userId, params }: { userId: string; params?: any }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const response = await userAPI.getUserActivity(userId, params);
      
      return response;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to fetch user activity');
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
   * Get all users
   */
  users: (state: UserState) => state.users,

  /**
   * Get selected user
   */
  selectedUser: (state: UserState) => state.selectedUser,

  /**
   * Check if loading
   */
  isLoading: (state: UserState) => state.isLoading,

  /**
   * Get error message
   */
  error: (state: UserState) => state.error,

  /**
   * Get pagination info
   */
  pagination: (state: UserState) => state.pagination,

  /**
   * Get current filters
   */
  filters: (state: UserState) => state.filters,

  /**
   * Get users by status
   */
  usersByStatus: (state: UserState) => (status: string) => {
    return state.users.filter(user => user.status === status);
  },

  /**
   * Get users by role
   */
  usersByRole: (state: UserState) => (role: string) => {
    return state.users.filter(user => user.role === role);
  },

  /**
   * Get users by tenant
   */
  usersByTenant: (state: UserState) => (tenantId: string) => {
    return state.users.filter(user => user.tenant_id === tenantId);
  },

  /**
   * Get active users count
   */
  activeUsersCount: (state: UserState) => {
    return state.users.filter(user => user.status === 'active').length;
  },

  /**
   * Get suspended users count
   */
  suspendedUsersCount: (state: UserState) => {
    return state.users.filter(user => user.status === 'suspended').length;
  },

  /**
   * Get total users count
   */
  totalUsersCount: (state: UserState) => state.users.length,

  /**
   * Get user by ID
   */
  getUserById: (state: UserState) => (id: string) => {
    return state.users.find(user => user.id === id);
  },

  /**
   * Search users
   */
  searchUsers: (state: UserState) => (query: string) => {
    const lowercaseQuery = query.toLowerCase();
    return state.users.filter(user => 
      user.username.toLowerCase().includes(lowercaseQuery) ||
      user.email.toLowerCase().includes(lowercaseQuery) ||
      user.first_name.toLowerCase().includes(lowercaseQuery) ||
      user.last_name.toLowerCase().includes(lowercaseQuery) ||
      user.tenant_name.toLowerCase().includes(lowercaseQuery)
    );
  }
};

// ============================================================================
// MODULE EXPORT
// ============================================================================

const usersModule: Module<UserState, any> = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default usersModule;
