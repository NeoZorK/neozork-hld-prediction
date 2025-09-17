/**
 * Main Dashboard Component for Pocket Hedge Fund React Dashboard
 * 
 * This component renders the main dashboard view with statistics,
 * charts, and recent activity for fund management.
 */

import React from 'react';
import { useDashboard } from '../hooks/useDashboard';
import { useAuth } from '../hooks/useAuth';
import { DashboardStats, DashboardChart } from '../types';

// ============================================================================
// STATS CARD COMPONENT
// ============================================================================

interface StatsCardProps {
  title: string;
  value: string | number;
  change?: number;
  changeType?: 'positive' | 'negative' | 'neutral';
  icon?: React.ReactNode;
  loading?: boolean;
}

const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  change,
  changeType = 'neutral',
  icon,
  loading = false
}) => {
  const getChangeColor = () => {
    switch (changeType) {
      case 'positive': return 'text-green-600';
      case 'negative': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getChangeIcon = () => {
    switch (changeType) {
      case 'positive': return '↗';
      case 'negative': return '↘';
      default: return '';
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6 animate-pulse">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-8 bg-gray-200 rounded w-1/2"></div>
          </div>
          <div className="h-8 w-8 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {change !== undefined && (
            <p className={`text-sm ${getChangeColor()} mt-1`}>
              {getChangeIcon()} {Math.abs(change).toFixed(1)}%
            </p>
          )}
        </div>
        {icon && (
          <div className="text-gray-400 text-2xl">
            {icon}
          </div>
        )}
      </div>
    </div>
  );
};

// ============================================================================
// CHART COMPONENT
// ============================================================================

interface ChartProps {
  chart: DashboardChart;
  loading?: boolean;
}

const Chart: React.FC<ChartProps> = ({ chart, loading = false }) => {
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6 animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }

  // Simple chart placeholder - would integrate with actual charting library
  const renderChart = () => {
    switch (chart.type) {
      case 'line':
        return (
          <div className="h-64 flex items-end justify-between space-x-2 p-4">
            {chart.data.map((point, index) => (
              <div
                key={index}
                className="bg-blue-500 rounded-t"
                style={{
                  height: `${Math.max(10, (point.value / Math.max(...chart.data.map(d => d.value))) * 200)}px`,
                  width: `${100 / chart.data.length}%`
                }}
                title={`${point.label}: ${point.value.toFixed(1)}%`}
              />
            ))}
          </div>
        );
      case 'pie':
        return (
          <div className="h-64 flex items-center justify-center">
            <div className="text-center">
              <div className="text-3xl font-bold text-gray-900">
                {chart.data.length}
              </div>
              <div className="text-sm text-gray-600">Fund Types</div>
            </div>
          </div>
        );
      default:
        return (
          <div className="h-64 flex items-center justify-center text-gray-500">
            Chart type not supported
          </div>
        );
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{chart.title}</h3>
      {renderChart()}
    </div>
  );
};

// ============================================================================
// RECENT FUNDS COMPONENT
// ============================================================================

interface RecentFundsProps {
  funds: any[];
  loading?: boolean;
}

const RecentFunds: React.FC<RecentFundsProps> = ({ funds, loading = false }) => {
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="space-y-3">
          {[1, 2, 3].map(i => (
            <div key={i} className="flex items-center space-x-3">
              <div className="h-10 w-10 bg-gray-200 rounded"></div>
              <div className="flex-1">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-1"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Funds</h3>
      <div className="space-y-3">
        {funds.map((fund) => (
          <div key={fund.fund_id} className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded">
            <div className="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center">
              <span className="text-blue-600 font-semibold text-sm">
                {fund.name.charAt(0)}
              </span>
            </div>
            <div className="flex-1">
              <p className="font-medium text-gray-900">{fund.name}</p>
              <p className="text-sm text-gray-600">
                {fund.fund_type} • ${fund.current_value.toLocaleString()}
              </p>
            </div>
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900">
                {fund.current_investors} investors
              </p>
              <p className={`text-xs ${fund.status === 'active' ? 'text-green-600' : 'text-gray-600'}`}>
                {fund.status}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// ============================================================================
// MAIN DASHBOARD COMPONENT
// ============================================================================

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const {
    stats,
    charts,
    recentFunds,
    topPerformers,
    isLoading,
    error,
    lastUpdated,
    refresh
  } = useDashboard();

  // ============================================================================
  // RENDER HELPERS
  // ============================================================================

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };

  const formatPercentage = (value: number) => {
    return `${value.toFixed(2)}%`;
  };

  // ============================================================================
  // ERROR STATE
  // ============================================================================

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Error Loading Dashboard</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={refresh}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // ============================================================================
  // MAIN RENDER
  // ============================================================================

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
              <p className="text-gray-600">
                Welcome back, {user?.first_name || user?.username}!
              </p>
            </div>
            <div className="flex items-center space-x-4">
              {lastUpdated && (
                <p className="text-sm text-gray-500">
                  Last updated: {new Date(lastUpdated).toLocaleTimeString()}
                </p>
              )}
              <button
                onClick={refresh}
                disabled={isLoading}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {isLoading ? 'Refreshing...' : 'Refresh'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="Total Funds"
            value={stats?.total_funds || 0}
            icon="🏦"
            loading={isLoading}
          />
          <StatsCard
            title="Total Investors"
            value={stats?.total_investors || 0}
            icon="👥"
            loading={isLoading}
          />
          <StatsCard
            title="Assets Under Management"
            value={formatCurrency(stats?.total_assets_under_management || 0)}
            icon="💰"
            loading={isLoading}
          />
          <StatsCard
            title="Average Return"
            value={formatPercentage(stats?.total_return_percentage || 0)}
            change={stats?.total_return_percentage}
            changeType={stats?.total_return_percentage && stats.total_return_percentage > 0 ? 'positive' : 'negative'}
            icon="📈"
            loading={isLoading}
          />
        </div>

        {/* Charts and Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Charts */}
          <div className="lg:col-span-2 space-y-6">
            {charts.map((chart, index) => (
              <Chart key={index} chart={chart} loading={isLoading} />
            ))}
          </div>

          {/* Recent Funds */}
          <div className="space-y-6">
            <RecentFunds funds={recentFunds} loading={isLoading} />
            
            {/* Top Performers */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Performers</h3>
              <div className="space-y-3">
                {topPerformers.map((fund, index) => (
                  <div key={fund.fund_id} className="flex items-center justify-between p-3 hover:bg-gray-50 rounded">
                    <div className="flex items-center space-x-3">
                      <div className="h-8 w-8 bg-green-100 rounded-full flex items-center justify-center">
                        <span className="text-green-600 font-semibold text-sm">#{index + 1}</span>
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">{fund.name}</p>
                        <p className="text-sm text-gray-600">{fund.fund_type}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-green-600">
                        {formatPercentage(((fund.current_value - fund.initial_capital) / fund.initial_capital) * 100)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
