/**
 * TypeScript type definitions for SaaS Frontend
 * 
 * This file contains all type definitions used across the SaaS frontend components.
 */

// ============================================================================
// CORE TYPES
// ============================================================================

export interface Tenant {
  id: string;
  name: string;
  domain: string;
  status: TenantStatus;
  plan: Plan;
  created_at: string;
  updated_at: string;
  settings: TenantSettings;
}

export interface Plan {
  id: string;
  name: string;
  description: string;
  price: number;
  currency: string;
  billing_cycle: BillingCycle;
  features: Feature[];
  limits: PlanLimits;
  status: PlanStatus;
}

export interface Feature {
  id: string;
  name: string;
  description: string;
  type: FeatureType;
  access_level: FeatureAccess;
  limits?: FeatureLimits;
}

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  tenant_id: string;
  status: UserStatus;
  last_login: string;
  created_at: string;
}

export interface Subscription {
  id: string;
  tenant_id: string;
  plan_id: string;
  status: SubscriptionStatus;
  current_period_start: string;
  current_period_end: string;
  cancel_at_period_end: boolean;
  created_at: string;
}

export interface Usage {
  id: string;
  tenant_id: string;
  feature_id: string;
  usage_count: number;
  usage_limit: number;
  period_start: string;
  period_end: string;
  created_at: string;
}

export interface Billing {
  id: string;
  tenant_id: string;
  subscription_id: string;
  amount: number;
  currency: string;
  status: BillingStatus;
  due_date: string;
  paid_at?: string;
  created_at: string;
}

// ============================================================================
// ENUMS
// ============================================================================

export enum TenantStatus {
  ACTIVE = 'active',
  SUSPENDED = 'suspended',
  INACTIVE = 'inactive',
  PENDING = 'pending'
}

export enum PlanStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  DEPRECATED = 'deprecated'
}

export enum UserRole {
  ADMIN = 'admin',
  MANAGER = 'manager',
  USER = 'user',
  VIEWER = 'viewer'
}

export enum UserStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  PENDING = 'pending',
  SUSPENDED = 'suspended'
}

export enum SubscriptionStatus {
  ACTIVE = 'active',
  CANCELLED = 'cancelled',
  PAST_DUE = 'past_due',
  UNPAID = 'unpaid',
  TRIALING = 'trialing'
}

export enum BillingStatus {
  PAID = 'paid',
  UNPAID = 'unpaid',
  OVERDUE = 'overdue',
  REFUNDED = 'refunded'
}

export enum BillingCycle {
  MONTHLY = 'monthly',
  QUARTERLY = 'quarterly',
  YEARLY = 'yearly'
}

export enum FeatureType {
  API_CALLS = 'api_calls',
  STORAGE = 'storage',
  USERS = 'users',
  ANALYTICS = 'analytics',
  SUPPORT = 'support'
}

export enum FeatureAccess {
  INCLUDED = 'included',
  ADDON = 'addon',
  RESTRICTED = 'restricted'
}

// ============================================================================
// COMPLEX TYPES
// ============================================================================

export interface TenantSettings {
  timezone: string;
  language: string;
  notifications: NotificationSettings;
  integrations: IntegrationSettings;
}

export interface NotificationSettings {
  email: boolean;
  sms: boolean;
  push: boolean;
  billing_alerts: boolean;
  usage_alerts: boolean;
}

export interface IntegrationSettings {
  webhooks: WebhookConfig[];
  api_keys: ApiKeyConfig[];
}

export interface WebhookConfig {
  id: string;
  url: string;
  events: string[];
  secret: string;
  active: boolean;
}

export interface ApiKeyConfig {
  id: string;
  name: string;
  key: string;
  permissions: string[];
  expires_at?: string;
}

export interface PlanLimits {
  api_calls_per_month: number;
  storage_gb: number;
  users: number;
  analytics_retention_days: number;
  support_level: SupportLevel;
}

export interface FeatureLimits {
  max_usage: number;
  current_usage: number;
  reset_period: string;
}

export enum SupportLevel {
  BASIC = 'basic',
  STANDARD = 'standard',
  PREMIUM = 'premium',
  ENTERPRISE = 'enterprise'
}

// ============================================================================
// DASHBOARD TYPES
// ============================================================================

export interface DashboardStats {
  total_tenants: number;
  active_tenants: number;
  total_users: number;
  total_revenue: number;
  monthly_revenue: number;
  usage_stats: UsageStats;
  system_health: SystemHealth;
}

export interface UsageStats {
  total_api_calls: number;
  total_storage_used: number;
  active_users: number;
  peak_usage: number;
}

export interface SystemHealth {
  status: 'healthy' | 'warning' | 'critical';
  uptime: number;
  response_time: number;
  error_rate: number;
}

export interface ChartDataPoint {
  date: string;
  value: number;
  label?: string;
}

export interface ChartData {
  labels: string[];
  datasets: ChartDataset[];
}

export interface ChartDataset {
  label: string;
  data: number[];
  backgroundColor?: string | string[];
  borderColor?: string | string[];
  borderWidth?: number;
}

// ============================================================================
// API TYPES
// ============================================================================

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: Pagination;
}

export interface Pagination {
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, any>;
}

// ============================================================================
// COMPONENT PROPS
// ============================================================================

export interface DashboardProps {
  tenant?: Tenant;
  user?: User;
  onRefresh?: () => void;
}

export interface TenantCardProps {
  tenant: Tenant;
  onEdit?: (tenant: Tenant) => void;
  onDelete?: (tenant: Tenant) => void;
}

export interface UsageChartProps {
  data: ChartData;
  type: 'line' | 'bar' | 'pie';
  title?: string;
  height?: number;
}

export interface BillingCardProps {
  billing: Billing;
  onPay?: (billing: Billing) => void;
  onView?: (billing: Billing) => void;
}

// ============================================================================
// FORM TYPES
// ============================================================================

export interface CreateTenantForm {
  name: string;
  domain: string;
  plan_id: string;
  admin_email: string;
  admin_first_name: string;
  admin_last_name: string;
}

export interface UpdateTenantForm {
  name?: string;
  domain?: string;
  plan_id?: string;
  settings?: Partial<TenantSettings>;
}

export interface CreateUserForm {
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  tenant_id: string;
}

export interface UpdateUserForm {
  first_name?: string;
  last_name?: string;
  role?: UserRole;
  status?: UserStatus;
}

// ============================================================================
// FILTER TYPES
// ============================================================================

export interface TenantFilters {
  status?: TenantStatus;
  plan_id?: string;
  created_after?: string;
  created_before?: string;
  search?: string;
}

export interface UserFilters {
  tenant_id?: string;
  role?: UserRole;
  status?: UserStatus;
  created_after?: string;
  created_before?: string;
  search?: string;
}

export interface UsageFilters {
  tenant_id?: string;
  feature_id?: string;
  period_start?: string;
  period_end?: string;
}

export interface BillingFilters {
  tenant_id?: string;
  status?: BillingStatus;
  due_after?: string;
  due_before?: string;
  amount_min?: number;
  amount_max?: number;
}
