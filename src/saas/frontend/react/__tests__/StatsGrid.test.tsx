/**
 * Stats Grid Component Tests
 * 
 * Unit tests for the StatsGrid component.
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { StatsGrid } from '../components/dashboard/StatsGrid';
import { DashboardStats } from '../types';

// ============================================================================
// TEST DATA
// ============================================================================

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

describe('StatsGrid Component', () => {
  it('renders all stat cards', () => {
    render(<StatsGrid stats={mockStats} />);
    
    expect(screen.getByText('Total Tenants')).toBeInTheDocument();
    expect(screen.getByText('Total Users')).toBeInTheDocument();
    expect(screen.getByText('Monthly Revenue')).toBeInTheDocument();
    expect(screen.getByText('API Calls')).toBeInTheDocument();
    expect(screen.getByText('Storage Used')).toBeInTheDocument();
    expect(screen.getByText('Active Users')).toBeInTheDocument();
  });

  it('displays correct values', () => {
    render(<StatsGrid stats={mockStats} />);
    
    expect(screen.getByText('10')).toBeInTheDocument(); // Total tenants
    expect(screen.getByText('50')).toBeInTheDocument(); // Total users
    expect(screen.getByText('$1,000')).toBeInTheDocument(); // Monthly revenue
    expect(screen.getByText('5,000')).toBeInTheDocument(); // API calls
    expect(screen.getByText('25.5 GB')).toBeInTheDocument(); // Storage used
    expect(screen.getByText('15')).toBeInTheDocument(); // Active users
  });

  it('displays subtitles correctly', () => {
    render(<StatsGrid stats={mockStats} />);
    
    expect(screen.getByText('8 active')).toBeInTheDocument();
    expect(screen.getByText('Across all tenants')).toBeInTheDocument();
    expect(screen.getByText('$10,000 total')).toBeInTheDocument();
    expect(screen.getByText('This month')).toBeInTheDocument();
    expect(screen.getByText('Across all tenants')).toBeInTheDocument();
    expect(screen.getByText('Currently online')).toBeInTheDocument();
  });

  it('displays icons for each stat card', () => {
    render(<StatsGrid stats={mockStats} />);
    
    expect(screen.getByText('🏢')).toBeInTheDocument(); // Tenants icon
    expect(screen.getByText('👥')).toBeInTheDocument(); // Users icon
    expect(screen.getByText('💰')).toBeInTheDocument(); // Revenue icon
    expect(screen.getByText('📊')).toBeInTheDocument(); // API calls icon
    expect(screen.getByText('💾')).toBeInTheDocument(); // Storage icon
    expect(screen.getByText('🟢')).toBeInTheDocument(); // Active users icon
  });

  it('handles large numbers correctly', () => {
    const largeStats: DashboardStats = {
      ...mockStats,
      total_users: 1000000,
      monthly_revenue: 5000000,
      usage_stats: {
        ...mockStats.usage_stats,
        total_api_calls: 2500000
      }
    };

    render(<StatsGrid stats={largeStats} />);
    
    expect(screen.getByText('1.0M')).toBeInTheDocument(); // Total users
    expect(screen.getByText('$5,000,000')).toBeInTheDocument(); // Monthly revenue
    expect(screen.getByText('2.5M')).toBeInTheDocument(); // API calls
  });

  it('handles zero values correctly', () => {
    const zeroStats: DashboardStats = {
      ...mockStats,
      total_tenants: 0,
      active_tenants: 0,
      total_users: 0,
      monthly_revenue: 0,
      usage_stats: {
        ...mockStats.usage_stats,
        total_api_calls: 0,
        active_users: 0
      }
    };

    render(<StatsGrid stats={zeroStats} />);
    
    expect(screen.getByText('0')).toBeInTheDocument();
    expect(screen.getByText('0 active')).toBeInTheDocument();
  });

  it('calls onError when provided', () => {
    const onError = jest.fn();
    render(<StatsGrid stats={mockStats} onError={onError} />);
    
    // Component should render without calling onError
    expect(onError).not.toHaveBeenCalled();
  });

  it('applies correct CSS classes', () => {
    const { container } = render(<StatsGrid stats={mockStats} />);
    
    expect(container.querySelector('.stats-grid')).toBeInTheDocument();
    expect(container.querySelectorAll('.stat-card')).toHaveLength(6);
    expect(container.querySelector('.stat-card--primary')).toBeInTheDocument();
    expect(container.querySelector('.stat-card--secondary')).toBeInTheDocument();
    expect(container.querySelector('.stat-card--success')).toBeInTheDocument();
    expect(container.querySelector('.stat-card--info')).toBeInTheDocument();
    expect(container.querySelector('.stat-card--warning')).toBeInTheDocument();
  });
});
