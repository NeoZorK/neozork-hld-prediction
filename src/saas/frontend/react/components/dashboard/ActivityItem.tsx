/**
 * Activity Item Component
 * 
 * This component displays individual activity items in the recent activity list.
 */

import React from 'react';
import { Activity } from './RecentActivity';
import './ActivityItem.css';

// ============================================================================
// INTERFACES
// ============================================================================

interface ActivityItemProps {
  activity: Activity;
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export const ActivityItem: React.FC<ActivityItemProps> = ({ activity }) => {
  const getActivityIcon = (type: string, status?: string) => {
    if (activity.icon) return activity.icon;
    
    switch (type) {
      case 'user':
        return status === 'success' ? '👤' : '👤';
      case 'system':
        return status === 'error' ? '⚠️' : '⚙️';
      case 'billing':
        return status === 'success' ? '💳' : '💰';
      case 'usage':
        return '📊';
      default:
        return '📝';
    }
  };

  const getStatusClass = (status?: string) => {
    if (!status) return '';
    return `activity-item--${status}`;
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className={`activity-item ${getStatusClass(activity.status)}`}>
      <div className="activity-item__icon">
        {getActivityIcon(activity.type, activity.status)}
      </div>
      
      <div className="activity-item__content">
        <div className="activity-item__header">
          <h4 className="activity-item__title">{activity.title}</h4>
          <span className="activity-item__timestamp">
            {formatTimestamp(activity.timestamp)}
          </span>
        </div>
        
        <p className="activity-item__description">
          {activity.description}
        </p>
        
        {activity.user && (
          <div className="activity-item__user">
            by {activity.user}
          </div>
        )}
      </div>
    </div>
  );
};

export default ActivityItem;
