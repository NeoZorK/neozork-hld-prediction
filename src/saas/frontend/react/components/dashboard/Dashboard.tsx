/**
 * Main Dashboard Component for SaaS Platform
 * 
 * This component provides the main dashboard view with statistics,
 * charts, and quick access to key features.
 */

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { StatsGrid } from './StatsGrid';
import { UsageChart } from './UsageChart';
import { RecentActivity } from './RecentActivity';
import { QuickActions } from './QuickActions';
import { SystemHealth } from './SystemHealth';
import { DashboardStats, Tenant, User } from '../../types';
import { dashboardService } from '../../services/dashboardService';
import { useWebSocket } from '../../hooks/useWebSocket';
import './Dashboard.css';

// ============================================================================
// INTERFACES
// ============================================================================

interface DashboardProps {
  tenant?: Tenant;
  user?: User;
  onRefresh?: () => void;
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export const Dashboard: React.FC<DashboardProps> = ({
  tenant,
  user,
  onRefresh
}) => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  // WebSocket connection for real-time updates
  const { isConnected, lastMessage } = useWebSocket('/ws/dashboard');

  // Load dashboard data
  useEffect(() => {
    loadDashboardData();
  }, [tenant?.id]);

  // Handle real-time updates
  useEffect(() => {
    if (lastMessage) {
      handleRealtimeUpdate(lastMessage);
    }
  }, [lastMessage]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await dashboardService.getStats(tenant?.id);
      
      if (response.success) {
        setStats(response.data);
        setLastUpdated(new Date());
      } else {
        setError(response.error || 'Failed to load dashboard data');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleRealtimeUpdate = (message: any) => {
    if (message.type === 'stats_update' && message.tenant_id === tenant?.id) {
      setStats(prevStats => ({
        ...prevStats,
        ...message.data
      }));
      setLastUpdated(new Date());
    }
  };

  const handleRefresh = () => {
    loadDashboardData();
    onRefresh?.();
  };

  const handleError = (error: string) => {
    setError(error);
  };

  if (loading && !stats) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner" />
        <p>Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <div className="error-icon">⚠️</div>
        <h3>Error Loading Dashboard</h3>
        <p>{error}</p>
        <Button onClick={handleRefresh} variant="primary">
          Try Again
        </Button>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div className="dashboard-title">
          <h1>Dashboard</h1>
          {tenant && (
            <span className="tenant-name">{tenant.name}</span>
          )}
        </div>
        <div className="dashboard-actions">
          <div className="connection-status">
            <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`} />
            {isConnected ? 'Connected' : 'Disconnected'}
          </div>
          {lastUpdated && (
            <span className="last-updated">
              Last updated: {lastUpdated.toLocaleTimeString()}
            </span>
          )}
          <Button 
            onClick={handleRefresh} 
            variant="secondary"
            disabled={loading}
          >
            {loading ? 'Refreshing...' : 'Refresh'}
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      {stats && (
        <StatsGrid 
          stats={stats}
          onError={handleError}
        />
      )}

      {/* Main Content */}
      <div className="dashboard-content">
        <div className="dashboard-main">
          {/* Usage Chart */}
          <Card className="usage-chart-card">
            <CardHeader>
              <CardTitle>Usage Analytics</CardTitle>
            </CardHeader>
            <CardContent>
              <UsageChart 
                data={stats?.usage_stats}
                onError={handleError}
              />
            </CardContent>
          </Card>

          {/* Recent Activity */}
          <Card className="recent-activity-card">
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
            </CardHeader>
            <CardContent>
              <RecentActivity 
                tenantId={tenant?.id}
                onError={handleError}
              />
            </CardContent>
          </Card>
        </div>

        <div className="dashboard-sidebar">
          {/* System Health */}
          <Card className="system-health-card">
            <CardHeader>
              <CardTitle>System Health</CardTitle>
            </CardHeader>
            <CardContent>
              <SystemHealth 
                health={stats?.system_health}
                onError={handleError}
              />
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card className="quick-actions-card">
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent>
              <QuickActions 
                tenant={tenant}
                user={user}
                onError={handleError}
              />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
