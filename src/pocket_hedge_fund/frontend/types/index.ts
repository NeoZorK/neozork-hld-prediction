/**
 * TypeScript type definitions for Pocket Hedge Fund React Dashboard
 * 
 * This file contains all type definitions for the React frontend components,
 * API responses, and data structures used throughout the application.
 */

// ============================================================================
// AUTHENTICATION TYPES
// ============================================================================

export interface User {
  id: string;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  kyc_status: KYCStatus;
  is_active: boolean;
  mfa_enabled: boolean;
  created_at: string;
  last_login?: string;
}

export type UserRole = 'admin' | 'manager' | 'investor' | 'viewer';

export type KYCStatus = 'pending' | 'verified' | 'rejected' | 'expired';

export interface LoginRequest {
  email: string;
  password: string;
  mfa_code?: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  first_name: string;
  last_name: string;
  phone?: string;
  country?: string;
}

// ============================================================================
// FUND TYPES
// ============================================================================

export interface Fund {
  fund_id: string;
  name: string;
  description: string;
  fund_type: FundType;
  initial_capital: number;
  current_value: number;
  management_fee: number;
  performance_fee: number;
  min_investment: number;
  max_investment?: number;
  max_investors?: number;
  current_investors: number;
  status: FundStatus;
  risk_level: RiskLevel;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export type FundType = 'mini' | 'standard' | 'premium';

export type FundStatus = 'active' | 'paused' | 'closed' | 'suspended';

export type RiskLevel = 'low' | 'medium' | 'high';

export interface FundPerformance {
  total_return: number;
  total_return_percentage: number;
  daily_return: number;
  daily_return_percentage: number;
  sharpe_ratio: number;
  max_drawdown: number;
  volatility: number;
  snapshot_date: string;
}

export interface FundRiskMetrics {
  var_95: number;
  var_99: number;
  cvar_95: number;
  cvar_99: number;
  beta: number;
  correlation_spy: number;
  tracking_error: number;
  information_ratio: number;
  calculation_date: string;
}

export interface FundDetails extends Fund {
  performance: FundPerformance;
  risk_metrics: FundRiskMetrics;
  portfolio: PortfolioPosition[];
  strategies: TradingStrategy[];
}

// ============================================================================
// PORTFOLIO TYPES
// ============================================================================

export interface PortfolioPosition {
  asset_symbol: string;
  asset_name: string;
  asset_type: AssetType;
  quantity: number;
  average_price: number;
  current_price: number;
  current_value: number;
  unrealized_pnl: number;
  unrealized_pnl_percentage: number;
  weight_percentage: number;
}

export type AssetType = 'crypto' | 'stock' | 'forex' | 'commodity' | 'bond';

export interface TradingStrategy {
  strategy_id: string;
  name: string;
  description: string;
  strategy_type: StrategyType;
  allocation_percentage: number;
  parameters: Record<string, any>;
  is_active: boolean;
}

export type StrategyType = 'momentum' | 'mean_reversion' | 'arbitrage' | 'ml' | 'trend_following';

// ============================================================================
// INVESTOR TYPES
// ============================================================================

export interface Investor {
  investor_id: string;
  user_id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  investment_amount: number;
  shares_owned: number;
  current_value: number;
  total_return: number;
  total_return_percentage: number;
  investment_date: string;
  status: InvestorStatus;
}

export type InvestorStatus = 'active' | 'withdrawn' | 'suspended';

// ============================================================================
// API RESPONSE TYPES
// ============================================================================

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
  timestamp: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  page: number;
  page_size: number;
  total_count: number;
  has_more: boolean;
}

export interface ApiError {
  error: string;
  message: string;
  details?: Record<string, any>;
  timestamp: string;
  request_id?: string;
}

// ============================================================================
// UI COMPONENT TYPES
// ============================================================================

export interface TableColumn<T> {
  key: keyof T;
  title: string;
  sortable?: boolean;
  render?: (value: any, item: T) => React.ReactNode;
  width?: string;
  align?: 'left' | 'center' | 'right';
}

export interface TableProps<T> {
  data: T[];
  columns: TableColumn<T>[];
  loading?: boolean;
  pagination?: PaginationProps;
  onRowClick?: (item: T) => void;
  onSort?: (key: keyof T, direction: 'asc' | 'desc') => void;
}

export interface PaginationProps {
  current: number;
  pageSize: number;
  total: number;
  onChange: (page: number, pageSize: number) => void;
  showSizeChanger?: boolean;
  showQuickJumper?: boolean;
}

export interface ChartDataPoint {
  date: string;
  value: number;
  label?: string;
}

export interface ChartProps {
  data: ChartDataPoint[];
  height?: number;
  color?: string;
  showGrid?: boolean;
  showTooltip?: boolean;
  showLegend?: boolean;
}

// ============================================================================
// FORM TYPES
// ============================================================================

export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'password' | 'number' | 'select' | 'textarea' | 'date';
  required?: boolean;
  placeholder?: string;
  options?: { value: string; label: string }[];
  validation?: {
    min?: number;
    max?: number;
    pattern?: string;
    message?: string;
  };
}

export interface FormProps {
  fields: FormField[];
  onSubmit: (values: Record<string, any>) => void;
  loading?: boolean;
  submitText?: string;
  initialValues?: Record<string, any>;
}

// ============================================================================
// DASHBOARD TYPES
// ============================================================================

export interface DashboardStats {
  total_funds: number;
  total_investors: number;
  total_assets_under_management: number;
  total_return_percentage: number;
  active_strategies: number;
  risk_score: number;
}

export interface DashboardChart {
  title: string;
  type: 'line' | 'bar' | 'pie' | 'area';
  data: ChartDataPoint[];
  color?: string;
  height?: number;
}

export interface DashboardWidget {
  id: string;
  title: string;
  type: 'stat' | 'chart' | 'table' | 'list';
  data: any;
  size: 'small' | 'medium' | 'large';
  position: { x: number; y: number };
  refreshInterval?: number;
}

// ============================================================================
// NOTIFICATION TYPES
// ============================================================================

export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  timestamp: string;
  read: boolean;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export interface NotificationContextType {
  notifications: Notification[];
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => void;
  removeNotification: (id: string) => void;
  markAsRead: (id: string) => void;
  clearAll: () => void;
}

// ============================================================================
// THEME TYPES
// ============================================================================

export interface Theme {
  name: string;
  colors: {
    primary: string;
    secondary: string;
    success: string;
    warning: string;
    error: string;
    info: string;
    background: string;
    surface: string;
    text: string;
    textSecondary: string;
    border: string;
  };
  typography: {
    fontFamily: string;
    fontSize: {
      xs: string;
      sm: string;
      md: string;
      lg: string;
      xl: string;
    };
  };
  spacing: {
    xs: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
  };
  borderRadius: string;
  shadows: {
    sm: string;
    md: string;
    lg: string;
  };
}

export interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}

// ============================================================================
// EXPORT ALL TYPES
// ============================================================================

export * from './api';
export * from './components';
export * from './forms';
