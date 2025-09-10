/**
 * TypeScript type definitions for Pocket Hedge Fund Mobile App
 * 
 * This file contains all type definitions for the React Native mobile application,
 * API responses, navigation, and mobile-specific data structures.
 */

import { NavigationProp } from '@react-navigation/native';

// ============================================================================
// NAVIGATION TYPES
// ============================================================================

export type RootStackParamList = {
  Login: undefined;
  Register: undefined;
  Dashboard: undefined;
  FundList: undefined;
  FundDetails: { fundId: string };
  Portfolio: undefined;
  Profile: undefined;
  Settings: undefined;
  Notifications: undefined;
};

export type TabParamList = {
  Dashboard: undefined;
  Funds: undefined;
  Portfolio: undefined;
  Profile: undefined;
};

export type NavigationProps<T extends keyof RootStackParamList> = {
  navigation: NavigationProp<RootStackParamList, T>;
  route: {
    params: RootStackParamList[T];
  };
};

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
  avatar_url?: string;
}

export type UserRole = 'admin' | 'manager' | 'investor' | 'viewer';

export type KYCStatus = 'pending' | 'verified' | 'rejected' | 'expired';

export interface LoginRequest {
  email: string;
  password: string;
  mfa_code?: string;
  device_token?: string;
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
  device_token?: string;
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
  performance_24h?: number;
  performance_7d?: number;
  performance_30d?: number;
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

export interface FundDetails extends Fund {
  performance: FundPerformance;
  risk_metrics: FundRiskMetrics;
  portfolio: PortfolioPosition[];
  strategies: TradingStrategy[];
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
  change_24h?: number;
  change_24h_percentage?: number;
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
  performance_metrics?: {
    total_return: number;
    sharpe_ratio: number;
    max_drawdown: number;
  };
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
  avatar_url?: string;
}

export type InvestorStatus = 'active' | 'withdrawn' | 'suspended';

// ============================================================================
// MOBILE-SPECIFIC TYPES
// ============================================================================

export interface DeviceInfo {
  platform: 'ios' | 'android';
  version: string;
  device_id: string;
  push_token?: string;
  timezone: string;
  language: string;
}

export interface NotificationData {
  id: string;
  type: NotificationType;
  title: string;
  message: string;
  data?: Record<string, any>;
  timestamp: string;
  read: boolean;
  action_url?: string;
}

export type NotificationType = 
  | 'fund_update'
  | 'investment_alert'
  | 'performance_notification'
  | 'system_announcement'
  | 'security_alert';

export interface BiometricAuth {
  is_available: boolean;
  is_enabled: boolean;
  type: 'fingerprint' | 'face' | 'iris' | null;
}

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
  code?: number;
}

// ============================================================================
// UI COMPONENT TYPES
// ============================================================================

export interface ListItemProps<T> {
  item: T;
  index: number;
  onPress?: (item: T) => void;
  onLongPress?: (item: T) => void;
}

export interface ChartDataPoint {
  x: number | string;
  y: number;
  label?: string;
  color?: string;
}

export interface ChartProps {
  data: ChartDataPoint[];
  height?: number;
  width?: number;
  color?: string;
  showGrid?: boolean;
  showTooltip?: boolean;
  showLegend?: boolean;
  animated?: boolean;
}

export interface LoadingState {
  isLoading: boolean;
  error: string | null;
  data: any | null;
}

// ============================================================================
// FORM TYPES
// ============================================================================

export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'password' | 'number' | 'select' | 'textarea' | 'date' | 'phone';
  required?: boolean;
  placeholder?: string;
  options?: { value: string; label: string }[];
  validation?: {
    min?: number;
    max?: number;
    pattern?: string;
    message?: string;
  };
  secureTextEntry?: boolean;
  keyboardType?: 'default' | 'numeric' | 'email-address' | 'phone-pad';
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
  portfolio_value: number;
  daily_change: number;
  daily_change_percentage: number;
}

export interface DashboardChart {
  title: string;
  type: 'line' | 'bar' | 'pie' | 'area' | 'candlestick';
  data: ChartDataPoint[];
  color?: string;
  height?: number;
  period?: '1d' | '7d' | '30d' | '90d' | '1y';
}

// ============================================================================
// STORE TYPES
// ============================================================================

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  biometricEnabled: boolean;
}

export interface FundState {
  funds: Fund[];
  selectedFund: Fund | null;
  isLoading: boolean;
  error: string | null;
  lastUpdated: string | null;
}

export interface PortfolioState {
  positions: PortfolioPosition[];
  totalValue: number;
  totalReturn: number;
  totalReturnPercentage: number;
  isLoading: boolean;
  error: string | null;
}

export interface NotificationState {
  notifications: NotificationData[];
  unreadCount: number;
  isLoading: boolean;
  error: string | null;
}

export interface AppState {
  theme: 'light' | 'dark' | 'auto';
  language: string;
  notificationsEnabled: boolean;
  biometricEnabled: boolean;
  offlineMode: boolean;
}

// ============================================================================
// EXPORT ALL TYPES
// ============================================================================

export * from './api';
export * from './navigation';
export * from './components';
