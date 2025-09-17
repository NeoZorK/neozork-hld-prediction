/**
 * Vue Router configuration for Pocket Hedge Fund Admin Panel
 * 
 * This file configures the routing for the admin panel,
 * including authentication guards and route definitions.
 */

import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import { useStore } from 'vuex';

// Import views
import Dashboard from '../views/Dashboard.vue';
import Tenants from '../views/Tenants.vue';
import Users from '../views/Users.vue';
import Funds from '../views/Funds.vue';
import Billing from '../views/Billing.vue';
import Analytics from '../views/Analytics.vue';
import System from '../views/System.vue';
import Login from '../views/Login.vue';
import NotFound from '../views/NotFound.vue';

// ============================================================================
// ROUTE DEFINITIONS
// ============================================================================

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      requiresAuth: false,
      title: 'Login - Admin Panel'
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      requiresAuth: true,
      title: 'Dashboard - Admin Panel',
      permissions: ['analytics:read']
    }
  },
  {
    path: '/tenants',
    name: 'Tenants',
    component: Tenants,
    meta: {
      requiresAuth: true,
      title: 'Tenant Management - Admin Panel',
      permissions: ['tenants:read']
    }
  },
  {
    path: '/tenants/:id',
    name: 'TenantDetails',
    component: () => import('../views/TenantDetails.vue'),
    meta: {
      requiresAuth: true,
      title: 'Tenant Details - Admin Panel',
      permissions: ['tenants:read']
    }
  },
  {
    path: '/users',
    name: 'Users',
    component: Users,
    meta: {
      requiresAuth: true,
      title: 'User Management - Admin Panel',
      permissions: ['users:read']
    }
  },
  {
    path: '/users/:id',
    name: 'UserDetails',
    component: () => import('../views/UserDetails.vue'),
    meta: {
      requiresAuth: true,
      title: 'User Details - Admin Panel',
      permissions: ['users:read']
    }
  },
  {
    path: '/funds',
    name: 'Funds',
    component: Funds,
    meta: {
      requiresAuth: true,
      title: 'Fund Management - Admin Panel',
      permissions: ['funds:read']
    }
  },
  {
    path: '/funds/:id',
    name: 'FundDetails',
    component: () => import('../views/FundDetails.vue'),
    meta: {
      requiresAuth: true,
      title: 'Fund Details - Admin Panel',
      permissions: ['funds:read']
    }
  },
  {
    path: '/billing',
    name: 'Billing',
    component: Billing,
    meta: {
      requiresAuth: true,
      title: 'Billing Management - Admin Panel',
      permissions: ['billing:read']
    }
  },
  {
    path: '/analytics',
    name: 'Analytics',
    component: Analytics,
    meta: {
      requiresAuth: true,
      title: 'Analytics - Admin Panel',
      permissions: ['analytics:read']
    }
  },
  {
    path: '/system',
    name: 'System',
    component: System,
    meta: {
      requiresAuth: true,
      title: 'System Management - Admin Panel',
      permissions: ['settings:read']
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: {
      requiresAuth: true,
      title: 'Profile - Admin Panel'
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings.vue'),
    meta: {
      requiresAuth: true,
      title: 'Settings - Admin Panel'
    }
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('../views/Reports.vue'),
    meta: {
      requiresAuth: true,
      title: 'Reports - Admin Panel',
      permissions: ['reports:read']
    }
  },
  {
    path: '/logs',
    name: 'Logs',
    component: () => import('../views/Logs.vue'),
    meta: {
      requiresAuth: true,
      title: 'System Logs - Admin Panel',
      permissions: ['settings:read']
    }
  },
  {
    path: '/maintenance',
    name: 'Maintenance',
    component: () => import('../views/Maintenance.vue'),
    meta: {
      requiresAuth: true,
      title: 'Maintenance Mode - Admin Panel',
      permissions: ['settings:write']
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: {
      requiresAuth: false,
      title: 'Page Not Found - Admin Panel'
    }
  }
];

// ============================================================================
// ROUTER INSTANCE
// ============================================================================

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  }
});

// ============================================================================
// NAVIGATION GUARDS
// ============================================================================

/**
 * Global before guard to check authentication and permissions
 */
router.beforeEach(async (to, from, next) => {
  const store = useStore();
  
  // Set page title
  if (to.meta.title) {
    document.title = to.meta.title as string;
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    // Check if user is authenticated
    if (!store.getters['auth/isAuthenticated']) {
      // Try to get current user from stored token
      try {
        await store.dispatch('auth/getCurrentUser');
      } catch (error) {
        // If getting user fails, redirect to login
        next({
          path: '/login',
          query: { redirect: to.fullPath }
        });
        return;
      }
    }

    // Check permissions if required
    if (to.meta.permissions) {
      const permissions = to.meta.permissions as string[];
      const hasPermission = store.getters['auth/hasAnyPermission'](permissions);
      
      if (!hasPermission) {
        // Redirect to dashboard if no permission
        next('/dashboard');
        return;
      }
    }
  } else if (to.path === '/login' && store.getters['auth/isAuthenticated']) {
    // If user is already authenticated and trying to access login, redirect to dashboard
    next('/dashboard');
    return;
  }

  next();
});

/**
 * Global after guard for analytics and cleanup
 */
router.afterEach((to, from) => {
  // Track page view for analytics
  if (process.env.NODE_ENV === 'production') {
    // Add analytics tracking here
    console.log(`Page view: ${to.path}`);
  }

  // Clear any global errors
  const store = useStore();
  store.dispatch('auth/clearError');
});

// ============================================================================
// ROUTE UTILITIES
// ============================================================================

/**
 * Check if user has permission to access a route
 */
export const hasRoutePermission = (routeName: string): boolean => {
  const store = useStore();
  const route = router.getRoutes().find(r => r.name === routeName);
  
  if (!route || !route.meta.permissions) {
    return true;
  }

  const permissions = route.meta.permissions as string[];
  return store.getters['auth/hasAnyPermission'](permissions);
};

/**
 * Get all accessible routes for the current user
 */
export const getAccessibleRoutes = () => {
  const store = useStore();
  return router.getRoutes().filter(route => {
    if (!route.meta.requiresAuth) {
      return true;
    }

    if (!store.getters['auth/isAuthenticated']) {
      return false;
    }

    if (!route.meta.permissions) {
      return true;
    }

    const permissions = route.meta.permissions as string[];
    return store.getters['auth/hasAnyPermission'](permissions);
  });
};

/**
 * Navigate to a route with permission check
 */
export const navigateToRoute = (routeName: string) => {
  if (hasRoutePermission(routeName)) {
    router.push({ name: routeName });
  } else {
    console.warn(`Access denied to route: ${routeName}`);
  }
};

// ============================================================================
// EXPORTS
// ============================================================================

export default router;
export { routes };
