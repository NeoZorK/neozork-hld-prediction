<template>
  <div class="tenants">
    <!-- Header -->
    <div class="tenants-header">
      <h1 class="tenants-title">Tenant Management</h1>
      <div class="tenants-actions">
        <button 
          class="btn btn-primary"
          @click="showCreateModal = true"
        >
          <i class="fas fa-plus"></i>
          Add Tenant
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters">
      <div class="filter-group">
        <label for="status-filter">Status:</label>
        <select 
          id="status-filter" 
          v-model="filters.status"
          @change="applyFilters"
        >
          <option value="">All</option>
          <option value="active">Active</option>
          <option value="suspended">Suspended</option>
          <option value="cancelled">Cancelled</option>
          <option value="trial">Trial</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="plan-filter">Plan:</label>
        <select 
          id="plan-filter" 
          v-model="filters.plan"
          @change="applyFilters"
        >
          <option value="">All</option>
          <option value="free">Free</option>
          <option value="starter">Starter</option>
          <option value="professional">Professional</option>
          <option value="enterprise">Enterprise</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="search">Search:</label>
        <input 
          id="search"
          type="text" 
          v-model="filters.search"
          @input="applyFilters"
          placeholder="Search tenants..."
        />
      </div>

      <button 
        class="btn btn-secondary"
        @click="clearFilters"
      >
        Clear Filters
      </button>
    </div>

    <!-- Tenants Table -->
    <div class="tenants-table">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Domain</th>
            <th>Plan</th>
            <th>Status</th>
            <th>Users</th>
            <th>Created</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tenant in tenants" :key="tenant.id">
            <td>
              <div class="tenant-info">
                <div class="tenant-name">{{ tenant.name }}</div>
                <div class="tenant-email">{{ tenant.owner_email }}</div>
              </div>
            </td>
            <td>
              <a :href="`https://${tenant.domain}`" target="_blank" class="tenant-domain">
                {{ tenant.domain }}
              </a>
            </td>
            <td>
              <span class="plan-badge" :class="tenant.plan">
                {{ tenant.plan.toUpperCase() }}
              </span>
            </td>
            <td>
              <span class="status-badge" :class="tenant.status">
                {{ tenant.status.toUpperCase() }}
              </span>
            </td>
            <td>{{ tenant.usage.current_users }} / {{ tenant.limits.max_users }}</td>
            <td>{{ formatDate(tenant.created_at) }}</td>
            <td>
              <div class="action-buttons">
                <button 
                  class="btn btn-sm btn-primary"
                  @click="viewTenant(tenant)"
                >
                  <i class="fas fa-eye"></i>
                </button>
                <button 
                  class="btn btn-sm btn-secondary"
                  @click="editTenant(tenant)"
                >
                  <i class="fas fa-edit"></i>
                </button>
                <button 
                  v-if="tenant.status === 'active'"
                  class="btn btn-sm btn-warning"
                  @click="suspendTenant(tenant)"
                >
                  <i class="fas fa-pause"></i>
                </button>
                <button 
                  v-else-if="tenant.status === 'suspended'"
                  class="btn btn-sm btn-success"
                  @click="activateTenant(tenant)"
                >
                  <i class="fas fa-play"></i>
                </button>
                <button 
                  class="btn btn-sm btn-danger"
                  @click="deleteTenant(tenant)"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="pagination" v-if="pagination">
      <button 
        class="btn btn-secondary"
        :disabled="!pagination.has_previous"
        @click="goToPage(pagination.page - 1)"
      >
        Previous
      </button>
      
      <span class="pagination-info">
        Page {{ pagination.page }} of {{ pagination.total_pages }}
        ({{ pagination.total_count }} total)
      </span>
      
      <button 
        class="btn btn-secondary"
        :disabled="!pagination.has_next"
        @click="goToPage(pagination.page + 1)"
      >
        Next
      </button>
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="loading">
      <i class="fas fa-spinner fa-spin"></i>
      Loading tenants...
    </div>

    <!-- Error -->
    <div v-if="error" class="error-message">
      <i class="fas fa-exclamation-triangle"></i>
      {{ error }}
    </div>

    <!-- Create Tenant Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click="closeCreateModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>Create New Tenant</h3>
          <button class="modal-close" @click="closeCreateModal">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="createTenant">
            <div class="form-group">
              <label for="tenant-name">Tenant Name:</label>
              <input 
                id="tenant-name"
                type="text" 
                v-model="newTenant.name"
                required
              />
            </div>
            <div class="form-group">
              <label for="tenant-domain">Domain:</label>
              <input 
                id="tenant-domain"
                type="text" 
                v-model="newTenant.domain"
                required
              />
            </div>
            <div class="form-group">
              <label for="tenant-plan">Plan:</label>
              <select id="tenant-plan" v-model="newTenant.plan" required>
                <option value="free">Free</option>
                <option value="starter">Starter</option>
                <option value="professional">Professional</option>
                <option value="enterprise">Enterprise</option>
              </select>
            </div>
            <div class="form-group">
              <label for="owner-email">Owner Email:</label>
              <input 
                id="owner-email"
                type="email" 
                v-model="newTenant.owner_email"
                required
              />
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeCreateModal">
            Cancel
          </button>
          <button 
            class="btn btn-primary" 
            @click="createTenant"
            :disabled="isLoading"
          >
            Create Tenant
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted, ref } from 'vue';
import { useStore } from 'vuex';

export default defineComponent({
  name: 'Tenants',
  setup() {
    const store = useStore();

    // State
    const showCreateModal = ref(false);
    const newTenant = ref({
      name: '',
      domain: '',
      plan: 'free',
      owner_email: ''
    });

    // Computed properties
    const tenants = computed(() => store.getters['tenants/tenants']);
    const isLoading = computed(() => store.getters['tenants/isLoading']);
    const error = computed(() => store.getters['tenants/error']);
    const pagination = computed(() => store.getters['tenants/pagination']);
    const filters = computed(() => store.getters['tenants/filters']);

    // Methods
    const fetchTenants = async (params: any = {}) => {
      try {
        await store.dispatch('tenants/fetchTenants', {
          ...filters.value,
          ...params
        });
      } catch (error) {
        console.error('Failed to fetch tenants:', error);
      }
    };

    const applyFilters = () => {
      fetchTenants();
    };

    const clearFilters = () => {
      store.dispatch('tenants/clearFilters');
      fetchTenants();
    };

    const goToPage = (page: number) => {
      fetchTenants({ page });
    };

    const viewTenant = (tenant: any) => {
      // Navigate to tenant details
      console.log('View tenant:', tenant);
    };

    const editTenant = (tenant: any) => {
      // Open edit modal
      console.log('Edit tenant:', tenant);
    };

    const suspendTenant = async (tenant: any) => {
      if (confirm(`Are you sure you want to suspend ${tenant.name}?`)) {
        try {
          await store.dispatch('tenants/suspendTenant', {
            tenantId: tenant.id,
            reason: 'Suspended by admin'
          });
        } catch (error) {
          console.error('Failed to suspend tenant:', error);
        }
      }
    };

    const activateTenant = async (tenant: any) => {
      try {
        await store.dispatch('tenants/activateTenant', tenant.id);
      } catch (error) {
        console.error('Failed to activate tenant:', error);
      }
    };

    const deleteTenant = async (tenant: any) => {
      if (confirm(`Are you sure you want to delete ${tenant.name}? This action cannot be undone.`)) {
        try {
          await store.dispatch('tenants/deleteTenant', tenant.id);
        } catch (error) {
          console.error('Failed to delete tenant:', error);
        }
      }
    };

    const createTenant = async () => {
      try {
        await store.dispatch('tenants/createTenant', newTenant.value);
        closeCreateModal();
        // Reset form
        newTenant.value = {
          name: '',
          domain: '',
          plan: 'free',
          owner_email: ''
        };
      } catch (error) {
        console.error('Failed to create tenant:', error);
      }
    };

    const closeCreateModal = () => {
      showCreateModal.value = false;
    };

    const formatDate = (dateString: string) => {
      return new Date(dateString).toLocaleDateString();
    };

    // Lifecycle
    onMounted(() => {
      fetchTenants();
    });

    return {
      tenants,
      isLoading,
      error,
      pagination,
      filters,
      showCreateModal,
      newTenant,
      fetchTenants,
      applyFilters,
      clearFilters,
      goToPage,
      viewTenant,
      editTenant,
      suspendTenant,
      activateTenant,
      deleteTenant,
      createTenant,
      closeCreateModal,
      formatDate
    };
  }
});
</script>

<style scoped>
.tenants {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.tenants-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.tenants-title {
  font-size: 2rem;
  font-weight: bold;
  color: #1f2937;
  margin: 0;
}

.tenants-actions {
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

.btn-primary:hover {
  background-color: #2563eb;
}

.btn-secondary {
  background-color: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background-color: #4b5563;
}

.btn-success {
  background-color: #10b981;
  color: white;
}

.btn-success:hover {
  background-color: #059669;
}

.btn-warning {
  background-color: #f59e0b;
  color: white;
}

.btn-warning:hover {
  background-color: #d97706;
}

.btn-danger {
  background-color: #ef4444;
  color: white;
}

.btn-danger:hover {
  background-color: #dc2626;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.filter-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.filter-group input,
.filter-group select {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.tenants-table {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

th {
  background-color: #f9fafb;
  font-weight: 600;
  color: #374151;
}

.tenant-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.tenant-name {
  font-weight: 500;
  color: #1f2937;
}

.tenant-email {
  font-size: 0.875rem;
  color: #6b7280;
}

.tenant-domain {
  color: #3b82f6;
  text-decoration: none;
}

.tenant-domain:hover {
  text-decoration: underline;
}

.plan-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.plan-badge.free {
  background-color: #f3f4f6;
  color: #374151;
}

.plan-badge.starter {
  background-color: #dbeafe;
  color: #1e40af;
}

.plan-badge.professional {
  background-color: #d1fae5;
  color: #065f46;
}

.plan-badge.enterprise {
  background-color: #fef3c7;
  color: #92400e;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.active {
  background-color: #d1fae5;
  color: #065f46;
}

.status-badge.suspended {
  background-color: #fef2f2;
  color: #dc2626;
}

.status-badge.cancelled {
  background-color: #f3f4f6;
  color: #374151;
}

.status-badge.trial {
  background-color: #dbeafe;
  color: #1e40af;
}

.action-buttons {
  display: flex;
  gap: 0.25rem;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2rem;
  padding: 1rem;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.pagination-info {
  color: #6b7280;
  font-size: 0.875rem;
}

.loading {
  text-align: center;
  padding: 2rem;
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #6b7280;
  cursor: pointer;
  padding: 0.25rem;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

@media (max-width: 768px) {
  .tenants {
    padding: 1rem;
  }

  .tenants-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .filters {
    flex-direction: column;
  }

  .tenants-table {
    overflow-x: auto;
  }

  .pagination {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
