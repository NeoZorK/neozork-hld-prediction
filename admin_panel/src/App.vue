<template>
  <div id="app">
    <!-- Navigation -->
    <nav class="navbar" v-if="isAuthenticated">
      <div class="navbar-brand">
        <h1>Pocket Hedge Fund Admin</h1>
      </div>
      <div class="navbar-menu">
        <router-link to="/dashboard" class="navbar-item">
          <i class="fas fa-tachometer-alt"></i>
          Dashboard
        </router-link>
        <router-link to="/tenants" class="navbar-item">
          <i class="fas fa-building"></i>
          Tenants
        </router-link>
        <router-link to="/users" class="navbar-item">
          <i class="fas fa-users"></i>
          Users
        </router-link>
        <router-link to="/funds" class="navbar-item">
          <i class="fas fa-chart-line"></i>
          Funds
        </router-link>
        <router-link to="/billing" class="navbar-item">
          <i class="fas fa-dollar-sign"></i>
          Billing
        </router-link>
        <router-link to="/analytics" class="navbar-item">
          <i class="fas fa-chart-bar"></i>
          Analytics
        </router-link>
        <router-link to="/system" class="navbar-item">
          <i class="fas fa-cog"></i>
          System
        </router-link>
      </div>
      <div class="navbar-user">
        <div class="user-menu">
          <button class="user-button" @click="toggleUserMenu">
            <div class="user-avatar">
              {{ userInitials }}
            </div>
            <span class="user-name">{{ userFullName }}</span>
            <i class="fas fa-chevron-down"></i>
          </button>
          <div v-if="showUserMenu" class="user-dropdown">
            <a href="#" class="dropdown-item">
              <i class="fas fa-user"></i>
              Profile
            </a>
            <a href="#" class="dropdown-item">
              <i class="fas fa-cog"></i>
              Settings
            </a>
            <hr class="dropdown-divider">
            <a href="#" class="dropdown-item" @click="logout">
              <i class="fas fa-sign-out-alt"></i>
              Logout
            </a>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content" :class="{ 'with-navbar': isAuthenticated }">
      <router-view />
    </main>

    <!-- Loading Overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <i class="fas fa-spinner fa-spin"></i>
        <p>Loading...</p>
      </div>
    </div>

    <!-- Error Toast -->
    <div v-if="error" class="error-toast">
      <i class="fas fa-exclamation-triangle"></i>
      <span>{{ error }}</span>
      <button class="toast-close" @click="clearError">
        <i class="fas fa-times"></i>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted, ref } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'App',
  setup() {
    const store = useStore();
    const router = useRouter();

    // State
    const showUserMenu = ref(false);

    // Computed properties
    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated']);
    const isLoading = computed(() => store.getters['auth/isLoading']);
    const error = computed(() => store.getters['auth/error']);
    const userFullName = computed(() => store.getters['auth/userFullName']);
    const userInitials = computed(() => store.getters['auth/userInitials']);

    // Methods
    const toggleUserMenu = () => {
      showUserMenu.value = !showUserMenu.value;
    };

    const logout = async () => {
      try {
        await store.dispatch('auth/logout');
        router.push('/login');
      } catch (error) {
        console.error('Logout failed:', error);
      }
    };

    const clearError = () => {
      store.dispatch('auth/clearError');
    };

    // Close user menu when clicking outside
    const handleClickOutside = (event: Event) => {
      const target = event.target as HTMLElement;
      if (!target.closest('.user-menu')) {
        showUserMenu.value = false;
      }
    };

    // Lifecycle
    onMounted(() => {
      // Check if user is already authenticated
      if (!isAuthenticated.value) {
        store.dispatch('auth/getCurrentUser');
      }

      // Add click outside listener
      document.addEventListener('click', handleClickOutside);
    });

    return {
      isAuthenticated,
      isLoading,
      error,
      userFullName,
      userInitials,
      showUserMenu,
      toggleUserMenu,
      logout,
      clearError
    };
  }
});
</script>

<style>
/* Global Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f8fafc;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Navigation Styles */
.navbar {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.navbar-brand h1 {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1f2937;
  margin: 0;
}

.navbar-menu {
  display: flex;
  gap: 2rem;
  flex: 1;
  justify-content: center;
}

.navbar-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  color: #6b7280;
  text-decoration: none;
  border-radius: 0.375rem;
  transition: all 0.2s;
  font-weight: 500;
}

.navbar-item:hover,
.navbar-item.router-link-active {
  color: #3b82f6;
  background-color: #f3f4f6;
}

.navbar-user {
  display: flex;
  align-items: center;
}

.user-menu {
  position: relative;
}

.user-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1rem;
  background: none;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
  color: #374151;
}

.user-button:hover {
  background-color: #f3f4f6;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #3b82f6;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
}

.user-name {
  font-weight: 500;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  min-width: 200px;
  z-index: 1001;
  margin-top: 0.5rem;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: #374151;
  text-decoration: none;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: #f9fafb;
}

.dropdown-divider {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 0.5rem 0;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 2rem;
}

.main-content.with-navbar {
  padding-top: 80px; /* Account for fixed navbar */
}

/* Loading Overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.loading-spinner {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  text-align: center;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.loading-spinner i {
  font-size: 2rem;
  color: #3b82f6;
  margin-bottom: 1rem;
}

.loading-spinner p {
  color: #6b7280;
  margin: 0;
}

/* Error Toast */
.error-toast {
  position: fixed;
  top: 80px;
  right: 2rem;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  z-index: 1500;
  max-width: 400px;
}

.toast-close {
  background: none;
  border: none;
  color: #dc2626;
  cursor: pointer;
  padding: 0.25rem;
  margin-left: auto;
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar {
    padding: 0 1rem;
    flex-wrap: wrap;
    height: auto;
    min-height: 64px;
  }

  .navbar-menu {
    order: 3;
    width: 100%;
    justify-content: flex-start;
    gap: 1rem;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
  }

  .navbar-item {
    padding: 0.5rem;
    font-size: 0.875rem;
  }

  .main-content {
    padding: 1rem;
  }

  .main-content.with-navbar {
    padding-top: 120px; /* Account for taller navbar on mobile */
  }

  .error-toast {
    right: 1rem;
    left: 1rem;
    max-width: none;
  }
}

@media (max-width: 480px) {
  .navbar-brand h1 {
    font-size: 1.25rem;
  }

  .user-button {
    padding: 0.25rem 0.5rem;
  }

  .user-name {
    display: none;
  }
}

/* Utility Classes */
.text-center {
  text-align: center;
}

.text-left {
  text-align: left;
}

.text-right {
  text-align: right;
}

.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-3 { margin-bottom: 0.75rem; }
.mb-4 { margin-bottom: 1rem; }
.mb-5 { margin-bottom: 1.25rem; }
.mb-6 { margin-bottom: 1.5rem; }

.mt-1 { margin-top: 0.25rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-3 { margin-top: 0.75rem; }
.mt-4 { margin-top: 1rem; }
.mt-5 { margin-top: 1.25rem; }
.mt-6 { margin-top: 1.5rem; }

.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-3 { padding: 0.75rem; }
.p-4 { padding: 1rem; }
.p-5 { padding: 1.25rem; }
.p-6 { padding: 1.5rem; }

.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.gap-1 { gap: 0.25rem; }
.gap-2 { gap: 0.5rem; }
.gap-3 { gap: 0.75rem; }
.gap-4 { gap: 1rem; }

.w-full { width: 100%; }
.h-full { height: 100%; }

.rounded { border-radius: 0.25rem; }
.rounded-md { border-radius: 0.375rem; }
.rounded-lg { border-radius: 0.5rem; }

.shadow { box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); }
.shadow-md { box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
.shadow-lg { box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1); }

.bg-white { background-color: white; }
.bg-gray-50 { background-color: #f9fafb; }
.bg-gray-100 { background-color: #f3f4f6; }
.bg-blue-50 { background-color: #eff6ff; }
.bg-blue-500 { background-color: #3b82f6; }
.bg-green-50 { background-color: #f0fdf4; }
.bg-green-500 { background-color: #10b981; }
.bg-red-50 { background-color: #fef2f2; }
.bg-red-500 { background-color: #ef4444; }

.text-gray-500 { color: #6b7280; }
.text-gray-700 { color: #374151; }
.text-gray-900 { color: #111827; }
.text-blue-500 { color: #3b82f6; }
.text-green-500 { color: #10b981; }
.text-red-500 { color: #ef4444; }

.border { border: 1px solid #e5e7eb; }
.border-gray-200 { border-color: #e5e7eb; }
.border-gray-300 { border-color: #d1d5db; }
</style>
