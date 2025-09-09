/**
 * Recent Activity Component for Dashboard
 * 
 * This component displays recent activity and events in the system.
 */

import React, { useState, useEffect } from 'react';
import { ActivityItem } from './ActivityItem';
import { Button } from './ui/Button';
import { dashboardService } from '../../services/dashboardService';
import './RecentActivity.css';

// ============================================================================
// INTERFACES
// ============================================================================

interface RecentActivityProps {
  tenantId?: string;
  onError?: (error: string) => void;
}

interface Activity {
  id: string;
  type: 'user' | 'system' | 'billing' | 'usage';
  title: string;
  description: string;
  timestamp: string;
  user?: string;
  icon?: string;
  status?: 'success' | 'warning' | 'error' | 'info';
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export const RecentActivity: React.FC<RecentActivityProps> = ({
  tenantId,
  onError
}) => {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadRecentActivity();
  }, [tenantId]);

  const loadRecentActivity = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await dashboardService.getRecentActivity(tenantId, 10);
      
      if (response.success) {
        setActivities(response.data);
      } else {
        setError(response.error || 'Failed to load recent activity');
        onError?.(response.error || 'Failed to load recent activity');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMessage);
      onError?.(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    loadRecentActivity();
  };

  if (loading) {
    return (
      <div className="recent-activity-loading">
        <div className="loading-spinner" />
        <p>Loading recent activity...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="recent-activity-error">
        <p>Error loading activity: {error}</p>
        <Button onClick={handleRefresh} variant="secondary" size="small">
          Try Again
        </Button>
      </div>
    );
  }

  return (
    <div className="recent-activity">
      <div className="recent-activity__header">
        <h3>Recent Activity</h3>
        <Button 
          onClick={handleRefresh} 
          variant="secondary" 
          size="small"
        >
          Refresh
        </Button>
      </div>
      
      <div className="recent-activity__list">
        {activities.length === 0 ? (
          <div className="recent-activity__empty">
            <p>No recent activity</p>
          </div>
        ) : (
          activities.map(activity => (
            <ActivityItem
              key={activity.id}
              activity={activity}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default RecentActivity;
