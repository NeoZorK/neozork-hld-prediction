"""
Admin Panel Data Models

This module defines Pydantic models for admin panel data structures.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from decimal import Decimal
from enum import Enum
import uuid

from pydantic import BaseModel, Field, validator, EmailStr


class AdminRoleType(str, Enum):
    """Admin role types."""
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    MODERATOR = "moderator"
    VIEWER = "viewer"
    AUDITOR = "auditor"


class AdminPermissionType(str, Enum):
    """Admin permission types."""
    USER_MANAGEMENT = "user_management"
    SYSTEM_MONITORING = "system_monitoring"
    ANALYTICS_VIEW = "analytics_view"
    CONFIGURATION_MANAGE = "configuration_manage"
    AUDIT_LOG_VIEW = "audit_log_view"
    REPORTS_GENERATE = "reports_generate"
    SECURITY_MANAGE = "security_manage"
    BACKUP_MANAGE = "backup_manage"
    MAINTENANCE_EXECUTE = "maintenance_execute"


class AdminSessionStatus(str, Enum):
    """Admin session status."""
    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"
    SUSPENDED = "suspended"


class AdminAlertLevel(str, Enum):
    """Admin alert levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AdminReportType(str, Enum):
    """Admin report types."""
    SYSTEM_HEALTH = "system_health"
    USER_ACTIVITY = "user_activity"
    PERFORMANCE = "performance"
    SECURITY = "security"
    FINANCIAL = "financial"
    AUDIT = "audit"
    CUSTOM = "custom"


class AdminBackupType(str, Enum):
    """Admin backup types."""
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"
    CONFIGURATION = "configuration"
    DATABASE = "database"
    FILES = "files"


class AdminMaintenanceType(str, Enum):
    """Admin maintenance types."""
    DATABASE_OPTIMIZATION = "database_optimization"
    CACHE_CLEAR = "cache_clear"
    LOG_ROTATION = "log_rotation"
    SECURITY_SCAN = "security_scan"
    PERFORMANCE_TUNE = "performance_tune"
    BACKUP_CREATE = "backup_create"
    SYSTEM_UPDATE = "system_update"


class AdminUser(BaseModel):
    """Admin user model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    role: AdminRoleType
    permissions: List[AdminPermissionType] = Field(default_factory=list)
    is_active: bool = True
    is_verified: bool = False
    last_login: Optional[datetime] = None
    login_attempts: int = Field(default=0, ge=0)
    locked_until: Optional[datetime] = None
    password_hash: Optional[str] = None
    two_factor_enabled: bool = False
    two_factor_secret: Optional[str] = None
    timezone: str = Field(default="UTC")
    language: str = Field(default="en")
    preferences: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    created_by: Optional[str] = None

    @validator('username')
    def validate_username(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username must contain only alphanumeric characters, underscores, and hyphens')
        return v.lower()

    @validator('permissions')
    def validate_permissions(cls, v, values):
        if 'role' in values:
            role = values['role']
            if role == AdminRoleType.SUPER_ADMIN:
                # Super admin has all permissions
                return list(AdminPermissionType)
            elif role == AdminRoleType.VIEWER:
                # Viewer has limited permissions
                allowed = [AdminPermissionType.ANALYTICS_VIEW, AdminPermissionType.AUDIT_LOG_VIEW]
                if any(p not in allowed for p in v):
                    raise ValueError('Viewer role has limited permissions')
        return v


class AdminRole(BaseModel):
    """Admin role model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = None
    permissions: List[AdminPermissionType] = Field(default_factory=list)
    is_system_role: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    created_by: Optional[str] = None

    @validator('name')
    def validate_name(cls, v):
        return v.lower().replace(' ', '_')


class AdminPermission(BaseModel):
    """Admin permission model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: AdminPermissionType
    description: str
    resource: str  # e.g., "users", "system", "reports"
    action: str    # e.g., "read", "write", "delete"
    conditions: Optional[Dict[str, Any]] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class SystemMetrics(BaseModel):
    """System metrics model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    cpu_usage: float = Field(..., ge=0.0, le=100.0)
    memory_usage: float = Field(..., ge=0.0, le=100.0)
    disk_usage: float = Field(..., ge=0.0, le=100.0)
    network_io: Dict[str, float] = Field(default_factory=dict)
    active_connections: int = Field(default=0, ge=0)
    response_time: float = Field(default=0.0, ge=0.0)
    error_rate: float = Field(default=0.0, ge=0.0, le=100.0)
    throughput: float = Field(default=0.0, ge=0.0)
    queue_size: int = Field(default=0, ge=0)
    cache_hit_rate: float = Field(default=0.0, ge=0.0, le=100.0)
    database_connections: int = Field(default=0, ge=0)
    custom_metrics: Optional[Dict[str, Any]] = None


class AuditLog(BaseModel):
    """Audit log model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    username: Optional[str] = None
    action: str = Field(..., min_length=1, max_length=100)
    resource: str = Field(..., min_length=1, max_length=100)
    resource_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    success: bool = True
    error_message: Optional[str] = None
    severity: AdminAlertLevel = AdminAlertLevel.INFO

    @validator('ip_address')
    def validate_ip_address(cls, v):
        if v and not (v.count('.') == 3 or v.count(':') >= 2):
            raise ValueError('Invalid IP address format')
        return v


class AdminSession(BaseModel):
    """Admin session model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    username: str
    session_token: str
    status: AdminSessionStatus = AdminSessionStatus.ACTIVE
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    expires_at: datetime = Field(default_factory=lambda: datetime.now() + timedelta(hours=8))
    terminated_at: Optional[datetime] = None
    terminated_by: Optional[str] = None
    termination_reason: Optional[str] = None

    @validator('expires_at')
    def validate_expires_at(cls, v, values):
        if 'created_at' in values and v <= values['created_at']:
            raise ValueError('Expires at must be after created at')
        return v


class AdminConfiguration(BaseModel):
    """Admin configuration model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    key: str = Field(..., min_length=1, max_length=100)
    value: Union[str, int, float, bool, Dict[str, Any], List[Any]]
    description: Optional[str] = None
    category: str = Field(default="general")
    is_sensitive: bool = False
    is_readonly: bool = False
    validation_rules: Optional[Dict[str, Any]] = None
    default_value: Optional[Union[str, int, float, bool, Dict[str, Any], List[Any]]] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    updated_by: Optional[str] = None

    @validator('key')
    def validate_key(cls, v):
        return v.lower().replace(' ', '_')


class AdminReport(BaseModel):
    """Admin report model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    report_type: AdminReportType
    parameters: Optional[Dict[str, Any]] = None
    generated_by: str
    generated_at: datetime = Field(default_factory=datetime.now)
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    file_format: str = Field(default="pdf")
    status: str = Field(default="generated")
    download_count: int = Field(default=0, ge=0)
    expires_at: Optional[datetime] = None
    is_public: bool = False
    tags: List[str] = Field(default_factory=list)


class AdminAlert(BaseModel):
    """Admin alert model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1, max_length=1000)
    level: AdminAlertLevel
    category: str = Field(..., min_length=1, max_length=50)
    source: str = Field(..., min_length=1, max_length=50)
    is_active: bool = True
    is_acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    resolution_notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AdminDashboard(BaseModel):
    """Admin dashboard model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    layout: Dict[str, Any] = Field(default_factory=dict)
    widgets: List[str] = Field(default_factory=list)
    is_default: bool = False
    is_public: bool = False
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    permissions: List[AdminPermissionType] = Field(default_factory=list)


class AdminWidget(BaseModel):
    """Admin widget model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    configuration: Dict[str, Any] = Field(default_factory=dict)
    data_source: Optional[str] = None
    refresh_interval: int = Field(default=300, ge=10)  # seconds
    size: Dict[str, int] = Field(default_factory=lambda: {"width": 4, "height": 3})
    position: Dict[str, int] = Field(default_factory=lambda: {"x": 0, "y": 0})
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class AdminChart(BaseModel):
    """Admin chart model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=1, max_length=50)  # line, bar, pie, etc.
    title: str = Field(..., min_length=1, max_length=200)
    data: List[Dict[str, Any]] = Field(default_factory=list)
    options: Dict[str, Any] = Field(default_factory=dict)
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    colors: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class AdminTable(BaseModel):
    """Admin table model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=200)
    columns: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[Dict[str, Any]] = Field(default_factory=list)
    pagination: bool = True
    page_size: int = Field(default=25, ge=1, le=1000)
    sorting: Optional[Dict[str, str]] = None
    filtering: Optional[Dict[str, Any]] = None
    searchable: bool = True
    exportable: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class AdminForm(BaseModel):
    """Admin form model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=200)
    fields: List[Dict[str, Any]] = Field(default_factory=list)
    validation_rules: Optional[Dict[str, Any]] = None
    submit_action: Optional[str] = None
    success_message: Optional[str] = None
    error_message: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class AdminAction(BaseModel):
    """Admin action model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    action_type: str = Field(..., min_length=1, max_length=50)
    parameters: Optional[Dict[str, Any]] = None
    is_destructive: bool = False
    requires_confirmation: bool = False
    confirmation_message: Optional[str] = None
    permissions_required: List[AdminPermissionType] = Field(default_factory=list)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class AdminEvent(BaseModel):
    """Admin event model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    event_type: str = Field(..., min_length=1, max_length=50)
    data: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    username: Optional[str] = None
    ip_address: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    severity: AdminAlertLevel = AdminAlertLevel.INFO
    is_processed: bool = False
    processed_at: Optional[datetime] = None


class AdminNotification(BaseModel):
    """Admin notification model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1, max_length=1000)
    type: str = Field(..., min_length=1, max_length=50)
    recipient_id: Optional[str] = None
    recipient_role: Optional[AdminRoleType] = None
    is_read: bool = False
    read_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    action_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AdminBackup(BaseModel):
    """Admin backup model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    backup_type: AdminBackupType
    file_path: str
    file_size: int = Field(ge=0)
    checksum: Optional[str] = None
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    is_encrypted: bool = False
    compression_type: Optional[str] = None
    status: str = Field(default="completed")
    metadata: Optional[Dict[str, Any]] = None


class AdminMaintenance(BaseModel):
    """Admin maintenance model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    maintenance_type: AdminMaintenanceType
    scheduled_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str = Field(default="scheduled")
    created_by: str
    executed_by: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    results: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    next_execution: Optional[datetime] = None
