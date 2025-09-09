/**
 * NeoZork SaaS Frontend React Components
 * 
 * This is the main entry point for the React frontend components
 * used in the NeoZork SaaS platform.
 */

// ============================================================================
// COMPONENTS
// ============================================================================

// Dashboard Components
export { Dashboard } from './src/components/dashboard/Dashboard';
export { StatsGrid } from './src/components/dashboard/StatsGrid';
export { UsageChart } from './src/components/dashboard/UsageChart';
export { RecentActivity } from './src/components/dashboard/RecentActivity';
export { ActivityItem } from './src/components/dashboard/ActivityItem';
export { QuickActions } from './src/components/dashboard/QuickActions';
export { SystemHealth } from './src/components/dashboard/SystemHealth';

// UI Components
export { Card, CardHeader, CardContent, CardFooter, CardTitle } from './src/components/ui/Card';
export { Button } from './src/components/ui/Button';

// ============================================================================
// SERVICES
// ============================================================================

export { dashboardService } from './src/services/dashboardService';
export { chartService } from './src/services/chartService';
export { apiClient } from './src/services/apiClient';

// ============================================================================
// HOOKS
// ============================================================================

export { 
  useWebSocket, 
  useDashboardWebSocket, 
  useUsageTrackingWebSocket, 
  useBillingWebSocket 
} from './src/hooks/useWebSocket';

// ============================================================================
// TYPES
// ============================================================================

export * from './src/types';

// ============================================================================
// VERSION
// ============================================================================

export const VERSION = '1.0.0';
