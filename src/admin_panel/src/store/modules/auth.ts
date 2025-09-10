/**
 * Vuex module for admin authentication state management
 * 
 * This module handles admin user authentication, login/logout,
 * and permission management.
 */

import { Module } from 'vuex';
import { AdminState, AdminUser, AdminPermission } from '../../types';
import { authAPI } from '../../services/api';

// ============================================================================
// STATE
// ============================================================================

const state: AdminState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
  permissions: []
};

// ============================================================================
// MUTATIONS
// ============================================================================

const mutations = {
  SET_LOADING(state: AdminState, loading: boolean) {
    state.isLoading = loading;
  },

  SET_USER(state: AdminState, user: AdminUser | null) {
    state.user = user;
    state.isAuthenticated = !!user;
  },

  SET_PERMISSIONS(state: AdminState, permissions: AdminPermission[]) {
    state.permissions = permissions;
  },

  SET_ERROR(state: AdminState, error: string | null) {
    state.error = error;
  },

  CLEAR_ERROR(state: AdminState) {
    state.error = null;
  },

  LOGOUT(state: AdminState) {
    state.user = null;
    state.isAuthenticated = false;
    state.permissions = [];
    state.error = null;
  }
};

// ============================================================================
// ACTIONS
// ============================================================================

const actions = {
  /**
   * Admin login
   */
  async login({ commit }, credentials: { email: string; password: string; mfa_code?: string }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const response = await authAPI.login(credentials);
      
      commit('SET_USER', response.user);
      commit('SET_PERMISSIONS', response.user.permissions);
      
      return response;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Login failed');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Admin logout
   */
  async logout({ commit }) {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      commit('LOGOUT');
    }
  },

  /**
   * Get current admin user
   */
  async getCurrentUser({ commit }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      const user = await authAPI.getCurrentUser();
      
      commit('SET_USER', user);
      commit('SET_PERMISSIONS', user.permissions);
      
      return user;
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Failed to get user');
      commit('LOGOUT');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  /**
   * Refresh token
   */
  async refreshToken({ commit }) {
    try {
      const response = await authAPI.refreshToken();
      return response;
    } catch (error: any) {
      commit('LOGOUT');
      throw error;
    }
  },

  /**
   * Change password
   */
  async changePassword({ commit }, data: { current_password: string; new_password: string }) {
    try {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');

      await authAPI.changePassword(data);
    } catch (error: any) {
      commit('SET_ERROR', error.message || 'Password change failed');
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
   * Get current user
   */
  user: (state: AdminState) => state.user,

  /**
   * Check if user is authenticated
   */
  isAuthenticated: (state: AdminState) => state.isAuthenticated,

  /**
   * Check if loading
   */
  isLoading: (state: AdminState) => state.isLoading,

  /**
   * Get error message
   */
  error: (state: AdminState) => state.error,

  /**
   * Get user permissions
   */
  permissions: (state: AdminState) => state.permissions,

  /**
   * Check if user has specific permission
   */
  hasPermission: (state: AdminState) => (permission: AdminPermission) => {
    return state.permissions.includes(permission);
  },

  /**
   * Check if user has any of the specified permissions
   */
  hasAnyPermission: (state: AdminState) => (permissions: AdminPermission[]) => {
    return permissions.some(permission => state.permissions.includes(permission));
  },

  /**
   * Check if user has all of the specified permissions
   */
  hasAllPermissions: (state: AdminState) => (permissions: AdminPermission[]) => {
    return permissions.every(permission => state.permissions.includes(permission));
  },

  /**
   * Get user role
   */
  userRole: (state: AdminState) => state.user?.role,

  /**
   * Check if user is super admin
   */
  isSuperAdmin: (state: AdminState) => state.user?.role === 'super_admin',

  /**
   * Check if user is admin
   */
  isAdmin: (state: AdminState) => ['super_admin', 'admin'].includes(state.user?.role || ''),

  /**
   * Get user full name
   */
  userFullName: (state: AdminState) => {
    if (!state.user) return '';
    return `${state.user.first_name} ${state.user.last_name}`.trim();
  },

  /**
   * Get user initials
   */
  userInitials: (state: AdminState) => {
    if (!state.user) return '';
    const first = state.user.first_name.charAt(0).toUpperCase();
    const last = state.user.last_name.charAt(0).toUpperCase();
    return `${first}${last}`;
  }
};

// ============================================================================
// MODULE EXPORT
// ============================================================================

const authModule: Module<AdminState, any> = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default authModule;
