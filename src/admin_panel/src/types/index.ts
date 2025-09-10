/**
 * TypeScript type definitions for Pocket Hedge Fund Admin Panel
 * 
 * This file contains all type definitions for the Vue.js admin panel,
 * SaaS management, tenant operations, and admin-specific data structures.
 */

// ============================================================================
// ADMIN USER TYPES
// ============================================================================

export interface AdminUser {
  id: string;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  role: AdminRole;
  permissions: AdminPermission[];
  is_active: boolean;
  last_login?: string;
  created_at: string;
  updated_at: string;
  avatar_url?: string;
  department?: string;
  phone?: string;
}

export type AdminRole = 'super_admin' | 'admin' | 'manager' | 'support' | 'analyst';

export type AdminPermission = 
  | 'users:read' | 'users:write' | 'users:delete'
  | 'tenants:read' | 'tenants:write' | 'tenants:delete'
  | 'funds:read' | 'funds:write' | 'funds:delete'
  | 'analytics:read' | 'analytics:write'
  | 'billing:read' | 'billing:write'
  | 'settings:read' | 'settings:write'
  | 'reports:read' | 'reports:write';

// ============================================================================
// TENANT MANAGEMENT TYPES
// ============================================================================

export interface Tenant {
  id: string;
  name: string;
  domain: string;
  subdomain: string;
  status: TenantStatus;
  plan: TenantPlan;
  created_at: string;
  updated_at: string;
  owner_id: string;
  owner_email: string;
  settings: TenantSettings;
  limits: TenantLimits;
  usage: TenantUsage;
  billing_info: BillingInfo;
}

export type TenantStatus = 'active' | 'suspended' | 'cancelled' | 'trial' | 'expired';

export type TenantPlan = 'free' | 'starter' | 'professional' | 'enterprise' | 'custom';

export interface TenantSettings {
  theme: string;
  language: string;
  timezone: string;
  features: Record<string, boolean>;
  integrations: Record<string, any>;
  notifications: NotificationSettings;
  security: SecuritySettings;
}

export interface TenantLimits {
  max_users: number;
  max_funds: number;
  max_storage_gb: number;
  api_calls_per_hour: number;
  data_retention_days: number;
  custom_domains: number;
  sso_enabled: boolean;
  white_label: boolean;
}

export interface TenantUsage {
  current_users: number;
  current_funds: number;
  storage_used_gb: number;
  api_calls_last_hour: number;
  data_volume_gb: number;
  last_updated: string;
}

export interface BillingInfo {
  billing_email: string;
  billing_address: BillingAddress;
  payment_method: PaymentMethod;
  subscription_id?: string;
  next_billing_date?: string;
  amount_due: number;
  currency: string;
}

export interface BillingAddress {
  street: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
}

export interface PaymentMethod {
  type: 'card' | 'bank' | 'paypal' | 'crypto';
  last_four?: string;
  brand?: string;
  expiry_month?: number;
  expiry_year?: number;
}

// ============================================================================
// USER MANAGEMENT TYPES
// ============================================================================

export interface User {
  id: string;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  tenant_id: string;
  tenant_name: string;
  status: UserStatus;
  last_login?: string;
  created_at: string;
  updated_at: string;
  avatar_url?: string;
  phone?: string;
  department?: string;
  permissions: string[];
  mfa_enabled: boolean;
  login_attempts: number;
  locked_until?: string;
}

export type UserRole = 'admin' | 'manager' | 'investor' | 'viewer' | 'api';

export type UserStatus = 'active' | 'inactive' | 'suspended' | 'pending' | 'locked';

export interface UserActivity {
  id: string;
  user_id: string;
  action: string;
  resource: string;
  resource_id?: string;
  ip_address: string;
  user_agent: string;
  timestamp: string;
  details?: Record<string, any>;
}

// ============================================================================
// FUND MANAGEMENT TYPES
// ============================================================================

export interface Fund {
  id: string;
  name: string;
  description: string;
  fund_type: FundType;
  status: FundStatus;
  tenant_id: string;
  tenant_name: string;
  created_by: string;
  created_at: string;
  updated_at: string;
  initial_capital: number;
  current_value: number;
  management_fee: number;
  performance_fee: number;
  min_investment: number;
  max_investment?: number;
  max_investors?: number;
  current_investors: number;
  risk_level: RiskLevel;
  performance_metrics: FundPerformance;
  compliance_status: ComplianceStatus;
}

export type FundType = 'mini' | 'standard' | 'premium' | 'custom';

export type FundStatus = 'active' | 'paused' | 'closed' | 'suspended' | 'under_review';

export type RiskLevel = 'low' | 'medium' | 'high' | 'very_high';

export interface FundPerformance {
  total_return: number;
  total_return_percentage: number;
  daily_return: number;
  daily_return_percentage: number;
  sharpe_ratio: number;
  max_drawdown: number;
  volatility: number;
  alpha: number;
  beta: number;
  tracking_error: number;
  information_ratio: number;
  calmar_ratio: number;
  sortino_ratio: number;
  treynor_ratio: number;
  jensen_alpha: number;
  last_updated: string;
}

export interface ComplianceStatus {
  kyc_verified: boolean;
  aml_cleared: boolean;
  regulatory_approved: boolean;
  audit_passed: boolean;
  last_audit_date?: string;
  next_audit_date?: string;
  compliance_score: number;
  issues: ComplianceIssue[];
}

export interface ComplianceIssue {
  id: string;
  type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  status: 'open' | 'in_progress' | 'resolved' | 'dismissed';
  created_at: string;
  due_date?: string;
  assigned_to?: string;
}

// ============================================================================
// ANALYTICS TYPES
// ============================================================================

export interface DashboardStats {
  total_tenants: number;
  total_users: number;
  total_funds: number;
  total_assets_under_management: number;
  total_revenue: number;
  monthly_revenue: number;
  revenue_growth: number;
  active_subscriptions: number;
  churn_rate: number;
  user_growth: number;
  fund_performance_avg: number;
  system_health: SystemHealth;
}

export interface SystemHealth {
  status: 'healthy' | 'warning' | 'critical';
  uptime: number;
  response_time: number;
  error_rate: number;
  database_status: string;
  redis_status: string;
  api_status: string;
  last_updated: string;
}

export interface AnalyticsData {
  period: string;
  metrics: Record<string, number>;
  trends: TrendData[];
  comparisons: ComparisonData[];
}

export interface TrendData {
  date: string;
  value: number;
  change?: number;
  change_percentage?: number;
}

export interface ComparisonData {
  metric: string;
  current: number;
  previous: number;
  change: number;
  change_percentage: number;
}

// ============================================================================
// BILLING TYPES
// ============================================================================

export interface BillingRecord {
  id: string;
  tenant_id: string;
  tenant_name: string;
  amount: number;
  currency: string;
  status: BillingStatus;
  period_start: string;
  period_end: string;
  due_date: string;
  paid_date?: string;
  payment_method: string;
  invoice_url?: string;
  description: string;
  line_items: BillingLineItem[];
  created_at: string;
  updated_at: string;
}

export type BillingStatus = 'pending' | 'paid' | 'overdue' | 'cancelled' | 'refunded';

export interface BillingLineItem {
  description: string;
  quantity: number;
  unit_price: number;
  total: number;
  type: 'subscription' | 'usage' | 'overage' | 'discount' | 'tax';
}

export interface RevenueReport {
  period: string;
  total_revenue: number;
  recurring_revenue: number;
  one_time_revenue: number;
  churn_revenue: number;
  new_revenue: number;
  growth_rate: number;
  by_plan: Record<string, number>;
  by_tenant: Record<string, number>;
}

// ============================================================================
// SYSTEM CONFIGURATION TYPES
// ============================================================================

export interface SystemConfig {
  general: GeneralConfig;
  security: SecurityConfig;
  features: FeatureConfig;
  integrations: IntegrationConfig;
  notifications: NotificationConfig;
  maintenance: MaintenanceConfig;
}

export interface GeneralConfig {
  site_name: string;
  site_url: string;
  support_email: string;
  default_language: string;
  default_timezone: string;
  maintenance_mode: boolean;
  registration_enabled: boolean;
  email_verification_required: boolean;
}

export interface SecurityConfig {
  password_min_length: number;
  password_require_special: boolean;
  password_require_numbers: boolean;
  password_require_uppercase: boolean;
  session_timeout: number;
  max_login_attempts: number;
  lockout_duration: number;
  mfa_required: boolean;
  ip_whitelist: string[];
  rate_limiting: RateLimitConfig;
}

export interface RateLimitConfig {
  enabled: boolean;
  requests_per_minute: number;
  requests_per_hour: number;
  requests_per_day: number;
  burst_limit: number;
}

export interface FeatureConfig {
  multi_tenant: boolean;
  white_label: boolean;
  sso: boolean;
  api_access: boolean;
  webhooks: boolean;
  analytics: boolean;
  reporting: boolean;
  custom_domains: boolean;
}

export interface IntegrationConfig {
  stripe: StripeConfig;
  sendgrid: SendGridConfig;
  aws: AWSConfig;
  google: GoogleConfig;
  microsoft: MicrosoftConfig;
}

export interface StripeConfig {
  enabled: boolean;
  public_key: string;
  secret_key: string;
  webhook_secret: string;
  test_mode: boolean;
}

export interface SendGridConfig {
  enabled: boolean;
  api_key: string;
  from_email: string;
  from_name: string;
}

export interface AWSConfig {
  enabled: boolean;
  access_key_id: string;
  secret_access_key: string;
  region: string;
  s3_bucket: string;
}

export interface GoogleConfig {
  enabled: boolean;
  client_id: string;
  client_secret: string;
  redirect_uri: string;
}

export interface MicrosoftConfig {
  enabled: boolean;
  client_id: string;
  client_secret: string;
  tenant_id: string;
}

export interface NotificationConfig {
  email_enabled: boolean;
  sms_enabled: boolean;
  push_enabled: boolean;
  webhook_enabled: boolean;
  templates: NotificationTemplate[];
}

export interface NotificationTemplate {
  id: string;
  name: string;
  type: string;
  subject: string;
  body: string;
  variables: string[];
  enabled: boolean;
}

export interface MaintenanceConfig {
  enabled: boolean;
  start_time: string;
  end_time: string;
  message: string;
  allowed_ips: string[];
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
  pagination?: PaginationInfo;
}

export interface PaginationInfo {
  page: number;
  page_size: number;
  total_count: number;
  total_pages: number;
  has_next: boolean;
  has_previous: boolean;
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

export interface TableColumn {
  key: string;
  title: string;
  sortable?: boolean;
  filterable?: boolean;
  width?: string;
  align?: 'left' | 'center' | 'right';
  render?: (value: any, row: any) => any;
}

export interface TableAction {
  key: string;
  label: string;
  icon?: string;
  color?: string;
  condition?: (row: any) => boolean;
  handler: (row: any) => void;
}

export interface FilterOption {
  key: string;
  label: string;
  type: 'text' | 'select' | 'date' | 'number' | 'boolean';
  options?: { value: any; label: string }[];
  placeholder?: string;
}

export interface ChartConfig {
  type: 'line' | 'bar' | 'pie' | 'doughnut' | 'area' | 'scatter';
  data: any;
  options?: any;
  height?: number;
  responsive?: boolean;
}

export interface FormField {
  key: string;
  label: string;
  type: 'text' | 'email' | 'password' | 'number' | 'select' | 'textarea' | 'date' | 'boolean' | 'file';
  required?: boolean;
  placeholder?: string;
  options?: { value: any; label: string }[];
  validation?: ValidationRule[];
  disabled?: boolean;
  readonly?: boolean;
}

export interface ValidationRule {
  type: 'required' | 'email' | 'min' | 'max' | 'pattern' | 'custom';
  value?: any;
  message: string;
  validator?: (value: any) => boolean;
}

// ============================================================================
// STORE TYPES
// ============================================================================

export interface AdminState {
  user: AdminUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  permissions: AdminPermission[];
}

export interface TenantState {
  tenants: Tenant[];
  selectedTenant: Tenant | null;
  isLoading: boolean;
  error: string | null;
  pagination: PaginationInfo | null;
  filters: Record<string, any>;
}

export interface UserState {
  users: User[];
  selectedUser: User | null;
  isLoading: boolean;
  error: string | null;
  pagination: PaginationInfo | null;
  filters: Record<string, any>;
}

export interface FundState {
  funds: Fund[];
  selectedFund: Fund | null;
  isLoading: boolean;
  error: string | null;
  pagination: PaginationInfo | null;
  filters: Record<string, any>;
}

export interface AnalyticsState {
  stats: DashboardStats | null;
  analyticsData: AnalyticsData | null;
  isLoading: boolean;
  error: string | null;
  period: string;
  filters: Record<string, any>;
}

export interface BillingState {
  records: BillingRecord[];
  revenueReport: RevenueReport | null;
  isLoading: boolean;
  error: string | null;
  pagination: PaginationInfo | null;
  filters: Record<string, any>;
}

export interface SystemState {
  config: SystemConfig | null;
  health: SystemHealth | null;
  isLoading: boolean;
  error: string | null;
  isMaintenanceMode: boolean;
}

// ============================================================================
// EXPORT ALL TYPES
// ============================================================================

export * from './api';
export * from './components';
export * from './forms';
