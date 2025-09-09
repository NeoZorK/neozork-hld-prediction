/**
 * System Health Component for Dashboard
 * 
 * This component displays system health status and metrics.
 */

import React, { useState, useEffect } from 'react';
import { SystemHealth as SystemHealthType } from '../../types';
import { dashboardService } from '../../services/dashboardService';
import './SystemHealth.css';

// ============================================================================
// INTERFACES
// ============================================================================

interface SystemHealthProps {
  health?: SystemHealthType;
  onError?: (error: string) => void;
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export const SystemHealth: React.FC<SystemHealthProps> = ({
  health,
  onError
}) => {
  const [systemHealth, setSystemHealth] = useState<SystemHealthType | null>(health || null);
  const [loading, setLoading] = useState(!health);

  useEffect(() => {
    if (!health) {
      loadSystemHealth();
    }
  }, [health]);

  const loadSystemHealth = async () => {
    try {
      setLoading(true);
      const response = await dashboardService.getSystemHealth();
      
      if (response.success) {
        setSystemHealth(response.data);
      } else {
        onError?.(response.error || 'Failed to load system health');
      }
    } catch (error) {
      onError?.(error instanceof Error ? error.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return '🟢';
      case 'warning':
        return '🟡';
      case 'critical':
        return '🔴';
      default:
        return '⚪';
    }
  };

  const getStatusClass = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'system-health--healthy';
      case 'warning':
        return 'system-health--warning';
      case 'critical':
        return 'system-health--critical';
      default:
        return 'system-health--unknown';
    }
  };

  const formatUptime = (uptime: number) => {
    const days = Math.floor(uptime / 86400);
    const hours = Math.floor((uptime % 86400) / 3600);
    const minutes = Math.floor((uptime % 3600) / 60);
    
    if (days > 0) return `${days}d ${hours}h ${minutes}m`;
    if (hours > 0) return `${hours}h ${minutes}m`;
    return `${minutes}m`;
  };

  const formatResponseTime = (time: number) => {
    if (time < 1000) return `${time}ms`;
    return `${(time / 1000).toFixed(1)}s`;
  };

  if (loading) {
    return (
      <div className="system-health-loading">
        <div className="loading-spinner" />
        <p>Loading system health...</p>
      </div>
    );
  }

  if (!systemHealth) {
    return (
      <div className="system-health-error">
        <p>Unable to load system health</p>
      </div>
    );
  }

  return (
    <div className={`system-health ${getStatusClass(systemHealth.status)}`}>
      <div className="system-health__header">
        <div className="system-health__status">
          <span className="system-health__icon">
            {getStatusIcon(systemHealth.status)}
          </span>
          <span className="system-health__label">
            {systemHealth.status.toUpperCase()}
          </span>
        </div>
      </div>
      
      <div className="system-health__metrics">
        <div className="system-health__metric">
          <span className="metric__label">Uptime</span>
          <span className="metric__value">
            {formatUptime(systemHealth.uptime)}
          </span>
        </div>
        
        <div className="system-health__metric">
          <span className="metric__label">Response Time</span>
          <span className="metric__value">
            {formatResponseTime(systemHealth.response_time)}
          </span>
        </div>
        
        <div className="system-health__metric">
          <span className="metric__label">Error Rate</span>
          <span className="metric__value">
            {systemHealth.error_rate.toFixed(2)}%
          </span>
        </div>
      </div>
      
      <div className="system-health__footer">
        <button 
          className="system-health__refresh"
          onClick={loadSystemHealth}
        >
          Refresh
        </button>
      </div>
    </div>
  );
};

export default SystemHealth;
