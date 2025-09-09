/**
 * Dashboard Component Tests
 * 
 * Unit tests for the main Dashboard component.
 */

import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Dashboard } from '../components/dashboard/Dashboard';
import { dashboardService } from '../services/dashboardService';
import { Tenant, User, DashboardStats } from '../types';

// Mock the dashboard service
jest.mock('../services/dashboardService');
const mockDashboardService = dashboardService as jest.Mocked<typeof dashboardService>;

// Mock the WebSocket hook
jest.mock('../hooks/useWebSocket', () => ({
  useWebSocket: () => ({
    isConnected: true,
    lastMessage: null
  })
}));

// ============================================================================
// TEST DATA
// ============================================================================

const mockTenant: Tenant = {
  id: 'tenant-1',
  name: 'Test Tenant',
  domain: 'test.example.com',
  status: 'active' as any,
  plan: {
    id: 'plan-1',
    name: 'Basic Plan',
    description: 'Basic plan description',
    price: 29.99,
    currency: 'USD',
    billing_cycle: 'monthly' as any,
    features: [],
    limits: {
      api_calls_per_month: 1000,
      storage_gb: 10,
      users: 5,
      analytics_retention_days: 30,
      support_level: 'basic' as any
    },
    status: 'active' as any
  },
  created_at: '2023-01-01T00:00:00Z',
  updated_at: '2023-01-01T00:00:00Z',
  settings: {
    timezone: 'UTC',
    language: 'en',
    notifications: {
      email: true,
      sms: false,
      push: true,
      billing_alerts: true,
      usage_alerts: true
    },
    integrations: {
      webhooks: [],
      api_keys: []
    }
  }
};

const mockUser: User = {
  id: 'user-1',
  email: 'test@example.com',
  first_name: 'Test',
  last_name: 'User',
  role: 'admin' as any,
  tenant_id: 'tenant-1',
  status: 'active' as any,
  last_login: '2023-01-01T00:00:00Z',
  created_at: '2023-01-01T00:00:00Z'
};

const mockStats: DashboardStats = {
  total_tenants: 10,
  active_tenants: 8,
  total_users: 50,
  total_revenue: 10000,
  monthly_revenue: 1000,
  usage_stats: {
    total_api_calls: 5000,
    total_storage_used: 25.5,
    active_users: 15,
    peak_usage: 1000
  },
  system_health: {
    status: 'healthy',
    uptime: 86400,
    response_time: 150,
    error_rate: 0.1
  }
};

// ============================================================================
// TESTS
// ============================================================================

describe('Dashboard Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders loading state initially', () => {
    mockDashboardService.getStats.mockResolvedValue({
      success: false,
      data: {} as DashboardStats,
      error: 'Loading...'
    });

    render(<Dashboard tenant={mockTenant} user={mockUser} />);
    
    expect(screen.getByText('Loading dashboard...')).toBeInTheDocument();
  });

  it('renders error state when API fails', async () => {
    mockDashboardService.getStats.mockResolvedValue({
      success: false,
      data: {} as DashboardStats,
      error: 'API Error'
    });

    render(<Dashboard tenant={mockTenant} user={mockUser} />);
    
    await waitFor(() => {
      expect(screen.getByText('Error Loading Dashboard')).toBeInTheDocument();
      expect(screen.getByText('API Error')).toBeInTheDocument();
    });
  });

  it('renders dashboard with stats when API succeeds', async () => {
    mockDashboardService.getStats.mockResolvedValue({
      success: true,
      data: mockStats
    });

    render(<Dashboard tenant={mockTenant} user={mockUser} />);
    
    await waitFor(() => {
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
      expect(screen.getByText('Test Tenant')).toBeInTheDocument();
      expect(screen.getByText('10')).toBeInTheDocument(); // Total tenants
      expect(screen.getByText('50')).toBeInTheDocument(); // Total users
    });
  });

  it('displays connection status', async () => {
    mockDashboardService.getStats.mockResolvedValue({
      success: true,
      data: mockStats
    });

    render(<Dashboard tenant={mockTenant} user={mockUser} />);
    
    await waitFor(() => {
      expect(screen.getByText('Connected')).toBeInTheDocument();
    });
  });

  it('calls refresh when refresh button is clicked', async () => {
    mockDashboardService.getStats.mockResolvedValue({
      success: true,
      data: mockStats
    });

    const onRefresh = jest.fn();
    render(<Dashboard tenant={mockTenant} user={mockUser} onRefresh={onRefresh} />);
    
    await waitFor(() => {
      expect(screen.getByText('Refresh')).toBeInTheDocument();
    });

    const refreshButton = screen.getByText('Refresh');
    refreshButton.click();

    expect(mockDashboardService.getStats).toHaveBeenCalledTimes(2);
    expect(onRefresh).toHaveBeenCalled();
  });

  it('renders without tenant and user props', async () => {
    mockDashboardService.getStats.mockResolvedValue({
      success: true,
      data: mockStats
    });

    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
    });
  });

  it('handles real-time updates', async () => {
    mockDashboardService.getStats.mockResolvedValue({
      success: true,
      data: mockStats
    });

    // Mock WebSocket hook to return a message
    jest.doMock('../hooks/useWebSocket', () => ({
      useWebSocket: () => ({
        isConnected: true,
        lastMessage: {
          type: 'stats_update',
          tenant_id: 'tenant-1',
          data: { total_tenants: 11 }
        }
      })
    }));

    render(<Dashboard tenant={mockTenant} user={mockUser} />);
    
    await waitFor(() => {
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
    });
  });
});
