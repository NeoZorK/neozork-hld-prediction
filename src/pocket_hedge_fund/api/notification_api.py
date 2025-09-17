"""
NeoZork Pocket Hedge Fund - Notification API

This module provides RESTful API endpoints for notification management including:
- Send notifications
- Get user notifications
- Mark notifications as read
- Manage notification preferences
- Create notification templates
- Get notification statistics
- Batch notification operations
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import logging

from ..notifications.notification_manager import (
    NotificationManager, NotificationType, NotificationChannel, 
    NotificationPriority, NotificationStatus, NotificationPreferences
)
from ..auth.jwt_manager import JWTManager
from ..config.database_manager import DatabaseManager
from ..config.config_manager import ConfigManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])

# Security
security = HTTPBearer()

# Global instances
notification_manager = None
jwt_manager = None

async def get_notification_manager() -> NotificationManager:
    """Get notification manager instance"""
    global notification_manager
    if not notification_manager:
        db_manager = DatabaseManager()
        config_manager = ConfigManager()
        await db_manager.initialize()
        await config_manager.initialize()
        
        notification_manager = NotificationManager(db_manager, config_manager)
        await notification_manager.initialize()
    
    return notification_manager

async def get_jwt_manager() -> JWTManager:
    """Get JWT manager instance"""
    global jwt_manager
    if not jwt_manager:
        jwt_manager = JWTManager()
    
    return jwt_manager

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    jwt_mgr = await get_jwt_manager()
    
    try:
        payload = jwt_mgr.validate_token(credentials.credentials)
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Pydantic models

class NotificationCreateRequest(BaseModel):
    """Request model for creating notification"""
    user_id: str = Field(..., description="User ID to send notification to")
    title: str = Field(..., description="Notification title")
    message: str = Field(..., description="Notification message")
    notification_type: str = Field(..., description="Notification type")
    channel: str = Field(..., description="Notification channel")
    priority: str = Field(default="medium", description="Notification priority")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Additional data")
    template_id: Optional[str] = Field(default=None, description="Template ID")
    scheduled_at: Optional[datetime] = Field(default=None, description="Scheduled send time")

class NotificationResponse(BaseModel):
    """Response model for notification"""
    notification_id: str
    user_id: str
    title: str
    message: str
    notification_type: str
    channel: str
    priority: str
    status: str
    data: Dict[str, Any]
    template_id: Optional[str]
    scheduled_at: Optional[datetime]
    sent_at: Optional[datetime]
    read_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class NotificationListResponse(BaseModel):
    """Response model for notification list"""
    notifications: List[NotificationResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int

class NotificationPreferencesRequest(BaseModel):
    """Request model for notification preferences"""
    email_enabled: bool = Field(default=True, description="Enable email notifications")
    sms_enabled: bool = Field(default=False, description="Enable SMS notifications")
    push_enabled: bool = Field(default=True, description="Enable push notifications")
    in_app_enabled: bool = Field(default=True, description="Enable in-app notifications")
    webhook_enabled: bool = Field(default=False, description="Enable webhook notifications")
    webhook_url: Optional[str] = Field(default=None, description="Webhook URL")
    email_frequency: str = Field(default="immediate", description="Email frequency")
    sms_frequency: str = Field(default="immediate", description="SMS frequency")
    push_frequency: str = Field(default="immediate", description="Push frequency")
    notification_types: Dict[str, bool] = Field(default_factory=dict, description="Notification type preferences")
    quiet_hours_start: Optional[str] = Field(default=None, description="Quiet hours start time")
    quiet_hours_end: Optional[str] = Field(default=None, description="Quiet hours end time")
    timezone: str = Field(default="UTC", description="User timezone")

class NotificationPreferencesResponse(BaseModel):
    """Response model for notification preferences"""
    user_id: str
    email_enabled: bool
    sms_enabled: bool
    push_enabled: bool
    in_app_enabled: bool
    webhook_enabled: bool
    webhook_url: Optional[str]
    email_frequency: str
    sms_frequency: str
    push_frequency: str
    notification_types: Dict[str, bool]
    quiet_hours_start: Optional[str]
    quiet_hours_end: Optional[str]
    timezone: str
    created_at: datetime
    updated_at: datetime

class NotificationTemplateRequest(BaseModel):
    """Request model for notification template"""
    name: str = Field(..., description="Template name")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Template body")
    channel: str = Field(..., description="Notification channel")
    notification_type: str = Field(..., description="Notification type")
    variables: List[str] = Field(default_factory=list, description="Template variables")

class NotificationTemplateResponse(BaseModel):
    """Response model for notification template"""
    template_id: str
    name: str
    subject: str
    body: str
    channel: str
    notification_type: str
    variables: List[str]
    created_at: datetime
    updated_at: datetime

class BatchNotificationRequest(BaseModel):
    """Request model for batch notifications"""
    notifications: List[NotificationCreateRequest] = Field(..., description="List of notifications to send")

class BatchNotificationResponse(BaseModel):
    """Response model for batch notifications"""
    total: int
    sent: int
    failed: int
    errors: List[Dict[str, Any]]

class NotificationStatisticsResponse(BaseModel):
    """Response model for notification statistics"""
    total_notifications: int
    by_status: Dict[str, int]
    by_type: Dict[str, int]
    by_channel: Dict[str, int]
    by_priority: Dict[str, int]
    sent_rate: float
    read_rate: float

# API Endpoints

@router.post("/", response_model=Dict[str, str])
async def create_notification(
    request: NotificationCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a new notification"""
    try:
        # Check permissions
        if current_user.get("role") not in ["ADMIN", "MANAGER"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        # Validate notification type
        try:
            notification_type = NotificationType(request.notification_type)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid notification type")
        
        # Validate channel
        try:
            channel = NotificationChannel(request.channel)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid notification channel")
        
        # Validate priority
        try:
            priority = NotificationPriority(request.priority)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid notification priority")
        
        # Create notification
        notification_mgr = await get_notification_manager()
        notification_id = await notification_mgr.create_notification(
            user_id=request.user_id,
            title=request.title,
            message=request.message,
            notification_type=notification_type,
            channel=channel,
            priority=priority,
            data=request.data,
            template_id=request.template_id,
            scheduled_at=request.scheduled_at
        )
        
        return {
            "status": "success",
            "message": "Notification created successfully",
            "notification_id": notification_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create notification: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=NotificationListResponse)
async def get_notifications(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size"),
    status: Optional[str] = Query(None, description="Filter by status"),
    notification_type: Optional[str] = Query(None, description="Filter by notification type"),
    unread_only: bool = Query(False, description="Show only unread notifications"),
    current_user: dict = Depends(get_current_user)
):
    """Get user notifications with pagination and filtering"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        # Validate status if provided
        notification_status = None
        if status:
            try:
                notification_status = NotificationStatus(status)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid status")
        
        # Validate notification type if provided
        notification_type_enum = None
        if notification_type:
            try:
                notification_type_enum = NotificationType(notification_type)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid notification type")
        
        # Get notifications
        notification_mgr = await get_notification_manager()
        notifications = await notification_mgr.get_user_notifications(
            user_id=user_id,
            limit=page_size,
            offset=(page - 1) * page_size,
            status=notification_status,
            notification_type=notification_type_enum,
            unread_only=unread_only
        )
        
        # Convert to response format
        notification_responses = []
        for notification in notifications:
            notification_responses.append(NotificationResponse(
                notification_id=notification.notification_id,
                user_id=notification.user_id,
                title=notification.title,
                message=notification.message,
                notification_type=notification.notification_type.value,
                channel=notification.channel.value,
                priority=notification.priority.value,
                status=notification.status.value,
                data=notification.data,
                template_id=notification.template_id,
                scheduled_at=notification.scheduled_at,
                sent_at=notification.sent_at,
                read_at=notification.read_at,
                created_at=notification.created_at,
                updated_at=notification.updated_at
            ))
        
        # Calculate pagination
        total_count = len(notifications)
        total_pages = (total_count + page_size - 1) // page_size
        
        return NotificationListResponse(
            notifications=notification_responses,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get notifications: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Mark notification as read"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        notification_mgr = await get_notification_manager()
        success = await notification_mgr.mark_notification_read(notification_id, user_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        return {
            "status": "success",
            "message": "Notification marked as read"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to mark notification as read: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/preferences", response_model=NotificationPreferencesResponse)
async def get_notification_preferences(
    current_user: dict = Depends(get_current_user)
):
    """Get user notification preferences"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        notification_mgr = await get_notification_manager()
        preferences = await notification_mgr.get_user_preferences(user_id)
        
        if not preferences:
            raise HTTPException(status_code=404, detail="Preferences not found")
        
        # Convert notification types to string keys
        notification_types = {}
        for ntype, enabled in preferences.notification_types.items():
            notification_types[ntype.value] = enabled
        
        return NotificationPreferencesResponse(
            user_id=preferences.user_id,
            email_enabled=preferences.email_enabled,
            sms_enabled=preferences.sms_enabled,
            push_enabled=preferences.push_enabled,
            in_app_enabled=preferences.in_app_enabled,
            webhook_enabled=preferences.webhook_enabled,
            webhook_url=preferences.webhook_url,
            email_frequency=preferences.email_frequency,
            sms_frequency=preferences.sms_frequency,
            push_frequency=preferences.push_frequency,
            notification_types=notification_types,
            quiet_hours_start=preferences.quiet_hours_start,
            quiet_hours_end=preferences.quiet_hours_end,
            timezone=preferences.timezone,
            created_at=preferences.created_at,
            updated_at=preferences.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get notification preferences: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/preferences", response_model=Dict[str, str])
async def update_notification_preferences(
    request: NotificationPreferencesRequest,
    current_user: dict = Depends(get_current_user)
):
    """Update user notification preferences"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        # Convert string keys back to enum keys
        notification_types = {}
        for ntype_str, enabled in request.notification_types.items():
            try:
                ntype = NotificationType(ntype_str)
                notification_types[ntype] = enabled
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid notification type: {ntype_str}")
        
        # Create preferences object
        preferences = NotificationPreferences(
            user_id=user_id,
            email_enabled=request.email_enabled,
            sms_enabled=request.sms_enabled,
            push_enabled=request.push_enabled,
            in_app_enabled=request.in_app_enabled,
            webhook_enabled=request.webhook_enabled,
            webhook_url=request.webhook_url,
            email_frequency=request.email_frequency,
            sms_frequency=request.sms_frequency,
            push_frequency=request.push_frequency,
            notification_types=notification_types,
            quiet_hours_start=request.quiet_hours_start,
            quiet_hours_end=request.quiet_hours_end,
            timezone=request.timezone,
            created_at=datetime.now(datetime.UTC),
            updated_at=datetime.now(datetime.UTC)
        )
        
        notification_mgr = await get_notification_manager()
        success = await notification_mgr.update_user_preferences(user_id, preferences)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update preferences")
        
        return {
            "status": "success",
            "message": "Notification preferences updated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update notification preferences: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/templates", response_model=Dict[str, str])
async def create_notification_template(
    request: NotificationTemplateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create notification template"""
    try:
        # Check permissions
        if current_user.get("role") not in ["ADMIN", "MANAGER"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        # Validate channel
        try:
            channel = NotificationChannel(request.channel)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid notification channel")
        
        # Validate notification type
        try:
            notification_type = NotificationType(request.notification_type)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid notification type")
        
        notification_mgr = await get_notification_manager()
        template_id = await notification_mgr.create_notification_template(
            name=request.name,
            subject=request.subject,
            body=request.body,
            channel=channel,
            notification_type=notification_type,
            variables=request.variables
        )
        
        return {
            "status": "success",
            "message": "Notification template created successfully",
            "template_id": template_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create notification template: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/batch", response_model=BatchNotificationResponse)
async def send_batch_notifications(
    request: BatchNotificationRequest,
    current_user: dict = Depends(get_current_user)
):
    """Send batch notifications"""
    try:
        # Check permissions
        if current_user.get("role") not in ["ADMIN", "MANAGER"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        # Convert requests to notification data
        notifications_data = []
        for notification_req in request.notifications:
            # Validate notification type
            try:
                notification_type = NotificationType(notification_req.notification_type)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid notification type")
            
            # Validate channel
            try:
                channel = NotificationChannel(notification_req.channel)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid notification channel")
            
            # Validate priority
            try:
                priority = NotificationPriority(notification_req.priority)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid notification priority")
            
            notifications_data.append({
                "user_id": notification_req.user_id,
                "title": notification_req.title,
                "message": notification_req.message,
                "notification_type": notification_type,
                "channel": channel,
                "priority": priority,
                "data": notification_req.data,
                "template_id": notification_req.template_id,
                "scheduled_at": notification_req.scheduled_at
            })
        
        notification_mgr = await get_notification_manager()
        results = await notification_mgr.send_batch_notifications(notifications_data)
        
        return BatchNotificationResponse(
            total=results["total"],
            sent=results["sent"],
            failed=results["failed"],
            errors=results["errors"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to send batch notifications: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/statistics", response_model=NotificationStatisticsResponse)
async def get_notification_statistics(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter"),
    current_user: dict = Depends(get_current_user)
):
    """Get notification statistics"""
    try:
        # Check permissions for user_id filter
        if user_id and current_user.get("role") not in ["ADMIN", "MANAGER"]:
            # Users can only see their own statistics
            if user_id != current_user.get("user_id"):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        notification_mgr = await get_notification_manager()
        stats = await notification_mgr.get_notification_statistics(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return NotificationStatisticsResponse(
            total_notifications=stats["total_notifications"],
            by_status=stats["by_status"],
            by_type=stats["by_type"],
            by_channel=stats["by_channel"],
            by_priority=stats["by_priority"],
            sent_rate=stats["sent_rate"],
            read_rate=stats["read_rate"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get notification statistics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/cleanup")
async def cleanup_expired_notifications(
    days: int = Query(30, ge=1, le=365, description="Days to keep notifications"),
    current_user: dict = Depends(get_current_user)
):
    """Clean up expired notifications"""
    try:
        # Check permissions
        if current_user.get("role") not in ["ADMIN"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        notification_mgr = await get_notification_manager()
        await notification_mgr.cleanup_expired_notifications(days)
        
        return {
            "status": "success",
            "message": f"Expired notifications cleaned up (older than {days} days)"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to cleanup expired notifications: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# WebSocket endpoint for real-time notifications
@router.websocket("/ws/{user_id}")
async def websocket_notifications(websocket, user_id: str):
    """WebSocket endpoint for real-time notifications"""
    try:
        await websocket.accept()
        
        # Subscribe to user notifications
        notification_mgr = await get_notification_manager()
        
        # Keep connection alive and send notifications
        while True:
            try:
                # Check for new notifications
                notifications = await notification_mgr.get_user_notifications(
                    user_id=user_id,
                    limit=10,
                    unread_only=True
                )
                
                if notifications:
                    for notification in notifications:
                        await websocket.send_json({
                            "type": "notification",
                            "data": {
                                "notification_id": notification.notification_id,
                                "title": notification.title,
                                "message": notification.message,
                                "notification_type": notification.notification_type.value,
                                "priority": notification.priority.value,
                                "created_at": notification.created_at.isoformat()
                            }
                        })
                
                # Wait before checking again
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                break
        
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    finally:
        await websocket.close()
