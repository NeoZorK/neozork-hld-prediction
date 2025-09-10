/**
 * Vuex Store Configuration for Pocket Hedge Fund Admin Panel
 * 
 * This file configures the Vuex store with all modules,
 * plugins, and persistence settings.
 */

import { createStore } from 'vuex';
import { createLogger } from 'vuex';
import { AdminState, TenantState, UserState, FundState, AnalyticsState, BillingState, SystemState } from '../types';

// Import modules
import auth from './modules/auth';
import tenants from './modules/tenants';
import users from './modules/users';
import funds from './modules/funds';
import analytics from './modules/analytics';
import billing from './modules/billing';
import system from './modules/system';

// ============================================================================
// ROOT STATE
// ============================================================================

export interface RootState {
  auth: AdminState;
  tenants: TenantState;
  users: UserState;
  funds: FundState;
  analytics: AnalyticsState;
  billing: BillingState;
  system: SystemState;
}

// ============================================================================
// STORE CONFIGURATION
// ============================================================================

const store = createStore<RootState>({
  modules: {
    auth,
    tenants,
    users,
    funds,
    analytics,
    billing,
    system
  },
  plugins: process.env.NODE_ENV === 'development' ? [createLogger()] : [],
  strict: process.env.NODE_ENV === 'development'
});

// ============================================================================
// EXPORTS
// ============================================================================

export default store;
