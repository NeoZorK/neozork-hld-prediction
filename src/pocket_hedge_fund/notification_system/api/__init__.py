"""
Notification System API

This module provides REST API endpoints for notification system:
- Real-time notification endpoints
- Template management endpoints
- Preference management endpoints
- Analytics and reporting endpoints
"""

from .notification_api import router

__all__ = ["router"]
