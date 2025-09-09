/**
 * Stats Grid Component for Dashboard
 * 
 * This component displays key statistics in a grid layout
 * with visual indicators and trend information.
 */

import React from 'react';
import { Card, CardContent } from './ui/Card';
import { DashboardStats } from '../../types';
import './StatsGrid.css';

// ============================================================================
// INTERFACES
// ============================================================================

interface StatsGridProps {
  stats: DashboardStats;
  onError?: (error: string) => void;
}

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: {
    value: number;
    direction: 'up' | 'down' | 'neutral';
  };
  icon?: string;
  color?: string;
}

// ============================================================================
// COMPONENTS
// ============================================================================

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  trend,
  icon,
  color = 'primary'
}) => {
  const formatValue = (val: string | number): string => {
    if (typeof val === 'number') {
      if (val >= 1000000) {
        return `${(val / 1000000).toFixed(1)}M`;
      } else if (val >= 1000) {
        return `${(val / 1000).toFixed(1)}K`;
      }
      return val.toLocaleString();
    }
    return val;
  };

  const getTrendIcon = (direction: 'up' | 'down' | 'neutral') => {
    switch (direction) {
      case 'up': return '↗️';
      case 'down': return '↘️';
      case 'neutral': return '→';
      default: return '';
    }
  };

  const getTrendColor = (direction: 'up' | 'down' | 'neutral') => {
    switch (direction) {
      case 'up': return 'trend-up';
      case 'down': return 'trend-down';
      case 'neutral': return 'trend-neutral';
      default: return '';
    }
  };

  return (
    <Card className={`stat-card stat-card--${color}`}>
      <CardContent>
        <div className="stat-card__header">
          {icon && <span className="stat-card__icon">{icon}</span>}
          <h3 className="stat-card__title">{title}</h3>
        </div>
        
        <div className="stat-card__value">
          {formatValue(value)}
        </div>
        
        {subtitle && (
          <div className="stat-card__subtitle">
            {subtitle}
          </div>
        )}
        
        {trend && (
          <div className={`stat-card__trend ${getTrendColor(trend.direction)}`}>
            <span className="trend-icon">
              {getTrendIcon(trend.direction)}
            </span>
            <span className="trend-value">
              {Math.abs(trend.value)}%
            </span>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export const StatsGrid: React.FC<StatsGridProps> = ({
  stats,
  onError
}) => {
  const calculateTrend = (current: number, previous: number): { value: number; direction: 'up' | 'down' | 'neutral' } => {
    if (previous === 0) return { value: 0, direction: 'neutral' };
    
    const change = ((current - previous) / previous) * 100;
    const absChange = Math.abs(change);
    
    if (absChange < 1) return { value: 0, direction: 'neutral' };
    
    return {
      value: Math.round(absChange),
      direction: change > 0 ? 'up' : 'down'
    };
  };

  // Calculate trends (simplified - in real app, you'd have historical data)
  const tenantTrend = calculateTrend(stats.active_tenants, stats.total_tenants * 0.9);
  const userTrend = calculateTrend(stats.total_users, stats.total_users * 0.95);
  const revenueTrend = calculateTrend(stats.monthly_revenue, stats.monthly_revenue * 0.8);

  return (
    <div className="stats-grid">
      <StatCard
        title="Total Tenants"
        value={stats.total_tenants}
        subtitle={`${stats.active_tenants} active`}
        trend={tenantTrend}
        icon="🏢"
        color="primary"
      />
      
      <StatCard
        title="Total Users"
        value={stats.total_users}
        subtitle="Across all tenants"
        trend={userTrend}
        icon="👥"
        color="secondary"
      />
      
      <StatCard
        title="Monthly Revenue"
        value={`$${stats.monthly_revenue.toLocaleString()}`}
        subtitle={`$${stats.total_revenue.toLocaleString()} total`}
        trend={revenueTrend}
        icon="💰"
        color="success"
      />
      
      <StatCard
        title="API Calls"
        value={stats.usage_stats.total_api_calls.toLocaleString()}
        subtitle="This month"
        icon="📊"
        color="info"
      />
      
      <StatCard
        title="Storage Used"
        value={`${stats.usage_stats.total_storage_used.toFixed(1)} GB`}
        subtitle="Across all tenants"
        icon="💾"
        color="warning"
      />
      
      <StatCard
        title="Active Users"
        value={stats.usage_stats.active_users}
        subtitle="Currently online"
        icon="🟢"
        color="success"
      />
    </div>
  );
};

export default StatsGrid;
