"""
NeoZork SaaS Platform Module

This module provides the core SaaS functionality for the NeoZork Trading Platform,
including multi-tenancy, subscription management, billing, and customer management.

Key Components:
- Multi-tenant architecture
- Subscription and billing management
- Customer onboarding and management
- Usage tracking and analytics
- API rate limiting and quotas
- Customer support and ticketing
"""

__version__ = "1.0.0"
__author__ = "NeoZork Team"

# Import core SaaS components
from .models import (
    Tenant,
    Subscription,
    Billing,
    Customer,
    Usage,
    Plan,
    Feature
)

from .services import (
    TenantService,
    SubscriptionService,
    BillingService,
    CustomerService,
    UsageService,
    PlanService
)

from .auth import (
    SaaSUserManager,
    TenantAuthentication,
    MultiTenantSessionManager
)

from .middleware import (
    TenantMiddleware,
    RateLimitMiddleware,
    UsageTrackingMiddleware
)

__all__ = [
    # Models
    "Tenant",
    "Subscription", 
    "Billing",
    "Customer",
    "Usage",
    "Plan",
    "Feature",
    
    # Services
    "TenantService",
    "SubscriptionService",
    "BillingService", 
    "CustomerService",
    "UsageService",
    "PlanService",
    
    # Authentication
    "SaaSUserManager",
    "TenantAuthentication",
    "MultiTenantSessionManager",
    
    # Middleware
    "TenantMiddleware",
    "RateLimitMiddleware", 
    "UsageTrackingMiddleware"
]
