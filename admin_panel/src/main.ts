/**
 * Main entry point for Pocket Hedge Fund Admin Panel
 * 
 * This file initializes the Vue application with all necessary
 * plugins, stores, and global configurations.
 */

import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

// Import global styles
import './assets/styles/main.css';

// Import FontAwesome
import '@fortawesome/fontawesome-free/css/all.min.css';

// Import Vue Toastification
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';

// ============================================================================
// VUE APP CREATION
// ============================================================================

const app = createApp(App);

// ============================================================================
// PLUGIN REGISTRATION
// ============================================================================

// Router
app.use(router);

// Vuex Store
app.use(store);

// Toast Notifications
app.use(Toast, {
  position: 'top-right',
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false
});

// ============================================================================
// GLOBAL PROPERTIES
// ============================================================================

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error:', err);
  console.error('Component instance:', instance);
  console.error('Error info:', info);
  
  // Show error toast
  if (app.config.globalProperties.$toast) {
    app.config.globalProperties.$toast.error('An unexpected error occurred');
  }
};

// Global warning handler
app.config.warnHandler = (msg, instance, trace) => {
  console.warn('Vue warning:', msg);
  console.warn('Component instance:', instance);
  console.warn('Trace:', trace);
};

// ============================================================================
// GLOBAL DIRECTIVES
// ============================================================================

// Permission directive
app.directive('permission', {
  mounted(el, binding) {
    const { value } = binding;
    const store = app.config.globalProperties.$store;
    
    if (value && !store.getters['auth/hasAnyPermission'](value)) {
      el.style.display = 'none';
    }
  },
  updated(el, binding) {
    const { value } = binding;
    const store = app.config.globalProperties.$store;
    
    if (value && !store.getters['auth/hasAnyPermission'](value)) {
      el.style.display = 'none';
    } else {
      el.style.display = '';
    }
  }
});

// Loading directive
app.directive('loading', {
  mounted(el, binding) {
    const { value } = binding;
    if (value) {
      el.classList.add('loading');
    }
  },
  updated(el, binding) {
    const { value } = binding;
    if (value) {
      el.classList.add('loading');
    } else {
      el.classList.remove('loading');
    }
  }
});

// ============================================================================
// GLOBAL MIXINS
// ============================================================================

// Format currency mixin
app.mixin({
  methods: {
    formatCurrency(value: number, currency = 'USD') {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(value);
    },
    
    formatNumber(value: number, decimals = 0) {
      return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
      }).format(value);
    },
    
    formatPercentage(value: number, decimals = 1) {
      return `${value.toFixed(decimals)}%`;
    },
    
    formatDate(date: string | Date, format = 'short') {
      const dateObj = typeof date === 'string' ? new Date(date) : date;
      
      if (format === 'short') {
        return dateObj.toLocaleDateString();
      } else if (format === 'long') {
        return dateObj.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        });
      } else if (format === 'datetime') {
        return dateObj.toLocaleString();
      }
      
      return dateObj.toLocaleDateString();
    },
    
    formatRelativeTime(date: string | Date) {
      const dateObj = typeof date === 'string' ? new Date(date) : date;
      const now = new Date();
      const diff = now.getTime() - dateObj.getTime();
      
      const minutes = Math.floor(diff / (1000 * 60));
      const hours = Math.floor(diff / (1000 * 60 * 60));
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      
      if (days > 0) {
        return `${days} day${days > 1 ? 's' : ''} ago`;
      } else if (hours > 0) {
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
      } else if (minutes > 0) {
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
      } else {
        return 'Just now';
      }
    },
    
    truncateText(text: string, length = 100) {
      if (text.length <= length) {
        return text;
      }
      return text.substring(0, length) + '...';
    },
    
    capitalizeFirst(str: string) {
      return str.charAt(0).toUpperCase() + str.slice(1);
    },
    
    debounce(func: Function, wait: number) {
      let timeout: NodeJS.Timeout;
      return function executedFunction(...args: any[]) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    },
    
    throttle(func: Function, limit: number) {
      let inThrottle: boolean;
      return function executedFunction(...args: any[]) {
        if (!inThrottle) {
          func.apply(this, args);
          inThrottle = true;
          setTimeout(() => inThrottle = false, limit);
        }
      };
    }
  }
});

// ============================================================================
// GLOBAL COMPONENTS
// ============================================================================

// Register global components
import LoadingSpinner from './components/LoadingSpinner.vue';
import ErrorMessage from './components/ErrorMessage.vue';
import ConfirmDialog from './components/ConfirmDialog.vue';
import DataTable from './components/DataTable.vue';
import Pagination from './components/Pagination.vue';
import SearchInput from './components/SearchInput.vue';
import DatePicker from './components/DatePicker.vue';
import SelectInput from './components/SelectInput.vue';
import Modal from './components/Modal.vue';
import Toast from './components/Toast.vue';

app.component('LoadingSpinner', LoadingSpinner);
app.component('ErrorMessage', ErrorMessage);
app.component('ConfirmDialog', ConfirmDialog);
app.component('DataTable', DataTable);
app.component('Pagination', Pagination);
app.component('SearchInput', SearchInput);
app.component('DatePicker', DatePicker);
app.component('SelectInput', SelectInput);
app.component('Modal', Modal);
app.component('Toast', Toast);

// ============================================================================
// DEVELOPMENT TOOLS
// ============================================================================

if (process.env.NODE_ENV === 'development') {
  // Add Vue DevTools
  app.config.performance = true;
  
  // Add global properties for debugging
  app.config.globalProperties.$log = console.log;
  app.config.globalProperties.$warn = console.warn;
  app.config.globalProperties.$error = console.error;
}

// ============================================================================
// APP MOUNTING
// ============================================================================

app.mount('#app');

// ============================================================================
// EXPORTS
// ============================================================================

export default app;
