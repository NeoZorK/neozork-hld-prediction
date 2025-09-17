/**
 * Quick Actions Component for Dashboard
 * 
 * This component provides quick access to common actions and features.
 */

import React from 'react';
import { Button } from './ui/Button';
import { Tenant, User } from '../../types';
import './QuickActions.css';

// ============================================================================
// INTERFACES
// ============================================================================

interface QuickActionsProps {
  tenant?: Tenant;
  user?: User;
  onError?: (error: string) => void;
}

interface Action {
  id: string;
  label: string;
  icon: string;
  variant: 'primary' | 'secondary' | 'success' | 'warning' | 'info';
  onClick: () => void;
  disabled?: boolean;
  requiresPermission?: string;
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export const QuickActions: React.FC<QuickActionsProps> = ({
  tenant,
  user,
  onError
}) => {
  const handleCreateTenant = () => {
    // Navigate to create tenant page
    console.log('Navigate to create tenant');
  };

  const handleCreateUser = () => {
    // Navigate to create user page
    console.log('Navigate to create user');
  };

  const handleViewBilling = () => {
    // Navigate to billing page
    console.log('Navigate to billing');
  };

  const handleViewAnalytics = () => {
    // Navigate to analytics page
    console.log('Navigate to analytics');
  };

  const handleExportData = () => {
    // Export data
    console.log('Export data');
  };

  const handleSystemSettings = () => {
    // Navigate to system settings
    console.log('Navigate to system settings');
  };

  const handleSupport = () => {
    // Open support
    console.log('Open support');
  };

  const handleRefreshCache = () => {
    // Refresh cache
    console.log('Refresh cache');
  };

  const actions: Action[] = [
    {
      id: 'create-tenant',
      label: 'Create Tenant',
      icon: '🏢',
      variant: 'primary',
      onClick: handleCreateTenant,
      requiresPermission: 'tenants:create'
    },
    {
      id: 'create-user',
      label: 'Create User',
      icon: '👤',
      variant: 'secondary',
      onClick: handleCreateUser,
      requiresPermission: 'users:create'
    },
    {
      id: 'view-billing',
      label: 'View Billing',
      icon: '💳',
      variant: 'info',
      onClick: handleViewBilling,
      requiresPermission: 'billing:read'
    },
    {
      id: 'view-analytics',
      label: 'Analytics',
      icon: '📊',
      variant: 'success',
      onClick: handleViewAnalytics,
      requiresPermission: 'analytics:read'
    },
    {
      id: 'export-data',
      label: 'Export Data',
      icon: '📤',
      variant: 'warning',
      onClick: handleExportData,
      requiresPermission: 'data:export'
    },
    {
      id: 'system-settings',
      label: 'Settings',
      icon: '⚙️',
      variant: 'secondary',
      onClick: handleSystemSettings,
      requiresPermission: 'system:read'
    },
    {
      id: 'support',
      label: 'Support',
      icon: '🆘',
      variant: 'info',
      onClick: handleSupport
    },
    {
      id: 'refresh-cache',
      label: 'Refresh Cache',
      icon: '🔄',
      variant: 'secondary',
      onClick: handleRefreshCache,
      requiresPermission: 'system:admin'
    }
  ];

  const hasPermission = (permission?: string): boolean => {
    if (!permission) return true;
    if (!user) return false;
    
    // Simple permission check - in real app, you'd have a proper permission system
    const userPermissions = user.role === 'admin' ? ['*'] : ['read'];
    return userPermissions.includes('*') || userPermissions.includes(permission);
  };

  const filteredActions = actions.filter(action => 
    hasPermission(action.requiresPermission)
  );

  return (
    <div className="quick-actions">
      <div className="quick-actions__grid">
        {filteredActions.map(action => (
          <Button
            key={action.id}
            variant={action.variant}
            size="small"
            onClick={action.onClick}
            disabled={action.disabled}
            className="quick-actions__button"
          >
            <span className="quick-actions__icon">{action.icon}</span>
            <span className="quick-actions__label">{action.label}</span>
          </Button>
        ))}
      </div>
      
      {tenant && (
        <div className="quick-actions__tenant-info">
          <h4>Current Tenant</h4>
          <p>{tenant.name}</p>
          <p className="quick-actions__tenant-status">
            Status: <span className={`status status--${tenant.status}`}>
              {tenant.status}
            </span>
          </p>
        </div>
      )}
    </div>
  );
};

export default QuickActions;
