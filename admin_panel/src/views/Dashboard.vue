<template>
  <div class="dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <h1 class="dashboard-title">Admin Dashboard</h1>
      <div class="dashboard-actions">
        <button 
          class="btn btn-primary"
          @click="refreshData"
          :disabled="isLoading"
        >
          <i class="fas fa-sync-alt" :class="{ 'fa-spin': isLoading }"></i>
          Refresh
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid" v-if="stats">
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-building"></i>
        </div>
        <div class="stat-content">
          <h3 class="stat-value">{{ stats.total_tenants }}</h3>
          <p class="stat-label">Total Tenants</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-users"></i>
        </div>
        <div class="stat-content">
          <h3 class="stat-value">{{ stats.total_users }}</h3>
          <p class="stat-label">Total Users</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-chart-line"></i>
        </div>
        <div class="stat-content">
          <h3 class="stat-value">{{ stats.total_funds }}</h3>
          <p class="stat-label">Total Funds</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-dollar-sign"></i>
        </div>
        <div class="stat-content">
          <h3 class="stat-value">{{ formattedAUM }}</h3>
          <p class="stat-label">Assets Under Management</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-money-bill-wave"></i>
        </div>
        <div class="stat-content">
          <h3 class="stat-value">{{ formattedRevenue }}</h3>
          <p class="stat-label">Total Revenue</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-percentage"></i>
        </div>
        <div class="stat-content">
          <h3 class="stat-value">{{ formattedGrowth }}</h3>
          <p class="stat-label">Revenue Growth</p>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="charts-row">
      <div class="chart-container">
        <h3 class="chart-title">Revenue Trend</h3>
        <div class="chart-placeholder">
          <i class="fas fa-chart-area"></i>
          <p>Revenue chart will be displayed here</p>
        </div>
      </div>

      <div class="chart-container">
        <h3 class="chart-title">User Growth</h3>
        <div class="chart-placeholder">
          <i class="fas fa-chart-line"></i>
          <p>User growth chart will be displayed here</p>
        </div>
      </div>
    </div>

    <!-- System Health -->
    <div class="system-health" v-if="systemHealth">
      <h3 class="section-title">System Health</h3>
      <div class="health-grid">
        <div class="health-item">
          <div class="health-label">Status</div>
          <div class="health-value" :class="systemHealth.status">
            <i class="fas fa-circle"></i>
            {{ systemHealth.status.toUpperCase() }}
          </div>
        </div>
        <div class="health-item">
          <div class="health-label">Uptime</div>
          <div class="health-value">{{ formatUptime(systemHealth.uptime) }}</div>
        </div>
        <div class="health-item">
          <div class="health-label">Response Time</div>
          <div class="health-value">{{ systemHealth.response_time }}ms</div>
        </div>
        <div class="health-item">
          <div class="health-label">Error Rate</div>
          <div class="health-value">{{ systemHealth.error_rate }}%</div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="recent-activity">
      <h3 class="section-title">Recent Activity</h3>
      <div class="activity-list">
        <div class="activity-item" v-for="activity in recentActivities" :key="activity.id">
          <div class="activity-icon">
            <i :class="getActivityIcon(activity.type)"></i>
          </div>
          <div class="activity-content">
            <p class="activity-description">{{ activity.description }}</p>
            <span class="activity-time">{{ formatTime(activity.timestamp) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="error-message">
      <i class="fas fa-exclamation-triangle"></i>
      {{ error }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted } from 'vue';
import { useStore } from 'vuex';

export default defineComponent({
  name: 'Dashboard',
  setup() {
    const store = useStore();

    // Computed properties
    const stats = computed(() => store.getters['analytics/stats']);
    const isLoading = computed(() => store.getters['analytics/isLoading']);
    const error = computed(() => store.getters['analytics/error']);
    const systemHealth = computed(() => store.getters['analytics/systemHealth']);

    const formattedAUM = computed(() => {
      const aum = stats.value?.total_assets_under_management || 0;
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(aum);
    });

    const formattedRevenue = computed(() => {
      const revenue = stats.value?.total_revenue || 0;
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(revenue);
    });

    const formattedGrowth = computed(() => {
      const growth = stats.value?.revenue_growth || 0;
      const sign = growth >= 0 ? '+' : '';
      return `${sign}${growth.toFixed(1)}%`;
    });

    // Mock recent activities
    const recentActivities = computed(() => [
      {
        id: '1',
        type: 'tenant',
        description: 'New tenant "Acme Corp" registered',
        timestamp: new Date(Date.now() - 1000 * 60 * 30) // 30 minutes ago
      },
      {
        id: '2',
        type: 'user',
        description: 'User "john.doe" logged in',
        timestamp: new Date(Date.now() - 1000 * 60 * 45) // 45 minutes ago
      },
      {
        id: '3',
        type: 'fund',
        description: 'Fund "Growth Fund Alpha" created',
        timestamp: new Date(Date.now() - 1000 * 60 * 60) // 1 hour ago
      },
      {
        id: '4',
        type: 'billing',
        description: 'Payment received from "Tech Startup Inc"',
        timestamp: new Date(Date.now() - 1000 * 60 * 90) // 1.5 hours ago
      }
    ]);

    // Methods
    const refreshData = async () => {
      try {
        await Promise.all([
          store.dispatch('analytics/fetchDashboardStats'),
          store.dispatch('analytics/fetchSystemHealth')
        ]);
      } catch (error) {
        console.error('Failed to refresh data:', error);
      }
    };

    const formatUptime = (uptime: number) => {
      const days = Math.floor(uptime / (24 * 60 * 60));
      const hours = Math.floor((uptime % (24 * 60 * 60)) / (60 * 60));
      const minutes = Math.floor((uptime % (60 * 60)) / 60);
      
      if (days > 0) {
        return `${days}d ${hours}h ${minutes}m`;
      } else if (hours > 0) {
        return `${hours}h ${minutes}m`;
      } else {
        return `${minutes}m`;
      }
    };

    const formatTime = (timestamp: Date) => {
      const now = new Date();
      const diff = now.getTime() - timestamp.getTime();
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
    };

    const getActivityIcon = (type: string) => {
      const icons: Record<string, string> = {
        tenant: 'fas fa-building',
        user: 'fas fa-user',
        fund: 'fas fa-chart-line',
        billing: 'fas fa-dollar-sign',
        system: 'fas fa-cog'
      };
      return icons[type] || 'fas fa-info-circle';
    };

    // Lifecycle
    onMounted(() => {
      refreshData();
    });

    return {
      stats,
      isLoading,
      error,
      systemHealth,
      formattedAUM,
      formattedRevenue,
      formattedGrowth,
      recentActivities,
      refreshData,
      formatUptime,
      formatTime,
      getActivityIcon
    };
  }
});
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.dashboard-title {
  font-size: 2rem;
  font-weight: bold;
  color: #1f2937;
  margin: 0;
}

.dashboard-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2563eb;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 0.5rem;
  background-color: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  color: #6b7280;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: bold;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
}

.stat-label {
  color: #6b7280;
  margin: 0;
  font-size: 0.875rem;
}

.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.chart-container {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 1rem 0;
}

.chart-placeholder {
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  background-color: #f9fafb;
  border-radius: 0.375rem;
  border: 2px dashed #d1d5db;
}

.chart-placeholder i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.system-health {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 1rem 0;
}

.health-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.health-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.health-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.health-value {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.health-value.healthy {
  color: #10b981;
}

.health-value.warning {
  color: #f59e0b;
}

.health-value.critical {
  color: #ef4444;
}

.recent-activity {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: 0.375rem;
  background-color: #f9fafb;
}

.activity-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background-color: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
}

.activity-content {
  flex: 1;
}

.activity-description {
  margin: 0 0 0.25rem 0;
  color: #1f2937;
  font-weight: 500;
}

.activity-time {
  font-size: 0.875rem;
  color: #6b7280;
}

.error-message {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 1rem;
  border-radius: 0.375rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }

  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .charts-row {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
