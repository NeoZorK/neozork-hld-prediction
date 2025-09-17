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
try:
    from .models import (
        Tenant,
        Subscription,
        Billing,
        Customer,
        Usage,
        Plan,
        Feature
    )
except ImportError:
    # Models not available
    pass

try:
    from .services import (
        TenantService,
        SubscriptionService,
        PaymentService
    )
except ImportError:
    # Services not available
    pass

try:
    from .auth import (
        SaaSUserManager
    )
except ImportError:
    # Auth not available
    pass

try:
    from .middleware import (
        TenantMiddleware
    )
except ImportError:
    # Middleware not available
    pass

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
    "PaymentService",
    
    # Authentication
    "SaaSUserManager",
    
    # Middleware
    "TenantMiddleware"
]
