"""
Notification System API

REST API endpoints for notification system operations.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from ..models.notification_models import (
    Notification, NotificationTemplate, NotificationPreference,
    NotificationType, ChannelType, NotificationPriority, DeliveryStatus
)
from ..core.notification_manager import NotificationManager
from ...auth.auth_manager import get_current_user

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])

# Global notification manager instance
notification_manager = None


async def get_notification_manager() -> NotificationManager:
    """Get notification manager instance."""
    global notification_manager
    if notification_manager is None:
        notification_manager = NotificationManager()
        await notification_manager.initialize()
    return notification_manager


# Request/Response Models
class NotificationRequest(BaseModel):
    """Request model for sending notifications."""
    user_id: str = Field(..., description="Target user ID")
    notification_type: NotificationType = Field(..., description="Notification type")
    title: str = Field(..., description="Notification title")
    message: str = Field(..., description="Notification message")
    priority: NotificationPriority = Field(default=NotificationPriority.NORMAL, description="Notification priority")
    channels: List[ChannelType] = Field(..., description="Delivery channels")
    template_id: Optional[str] = Field(None, description="Template ID")
    template_data: Optional[Dict[str, Any]] = Field(None, description="Template data")
    scheduled_at: Optional[datetime] = Field(None, description="Scheduled delivery time")
    expires_at: Optional[datetime] = Field(None, description="Expiration time")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class BulkNotificationRequest(BaseModel):
    """Request model for bulk notifications."""
    notifications: List[NotificationRequest] = Field(..., description="List of notifications to send")


class NotificationResponse(BaseModel):
    """Response model for notification operations."""
    success: bool = Field(..., description="Operation success status")
    notification_id: Optional[str] = Field(None, description="Notification ID")
    message: str = Field(..., description="Response message")
    delivery_results: Optional[List[Dict[str, Any]]] = Field(None, description="Delivery results")


class TemplateRequest(BaseModel):
    """Request model for notification templates."""
    name: str = Field(..., description="Template name")
    description: Optional[str] = Field(None, description="Template description")
    notification_type: NotificationType = Field(..., description="Notification type")
    template_type: str = Field(..., description="Template type")
    subject_template: Optional[str] = Field(None, description="Subject template")
    body_template: str = Field(..., description="Body template")
    channels: List[ChannelType] = Field(..., description="Supported channels")
    variables: List[str] = Field(default_factory=list, description="Template variables")


class PreferenceRequest(BaseModel):
    """Request model for notification preferences."""
    notification_type: NotificationType = Field(..., description="Notification type")
    channels: List[ChannelType] = Field(..., description="Preferred channels")
    is_enabled: bool = Field(default=True, description="Whether notifications are enabled")
    quiet_hours_start: Optional[str] = Field(None, description="Quiet hours start (HH:MM)")
    quiet_hours_end: Optional[str] = Field(None, description="Quiet hours end (HH:MM)")
    timezone: str = Field(default="UTC", description="User timezone")
    frequency_limit: Optional[int] = Field(None, description="Max notifications per hour")
    priority_threshold: NotificationPriority = Field(default=NotificationPriority.LOW, description="Priority threshold")


# API Endpoints

@router.post("/send", response_model=NotificationResponse)
async def send_notification(
    request: NotificationRequest,
    background_tasks: BackgroundTasks,
    manager: NotificationManager = Depends(get_notification_manager),
    current_user: dict = Depends(get_current_user)
):
    """Send a single notification."""
    try:
        # Create notification object
        notification = Notification(
            user_id=request.user_id,
            notification_type=request.notification_type,
            title=request.title,
            message=request.message,
            priority=request.priority,
            channels=request.channels,
            template_id=request.template_id,
            template_data=request.template_data,
            scheduled_at=request.scheduled_at,
            expires_at=request.expires_at,
            metadata=request.metadata
        )
        
        # Send notification
        delivery_results = await manager.send_notification(notification)
        
        return NotificationResponse(
            success=True,
            notification_id=notification.id,
            message="Notification sent successfully",
            delivery_results=[{
                'channel': result.channel.value,
                'status': result.status.value,
                'sent_at': result.sent_at.isoformat() if result.sent_at else None,
                'delivered_at': result.delivered_at.isoformat() if result.delivered_at else None,
                'error_message': result.error_message
            } for result in delivery_results]
        )
        
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send/bulk", response_model=Dict[str, NotificationResponse])
async def send_bulk_notifications(
    request: BulkNotificationRequest,
    background_tasks: BackgroundTasks,
    manager: NotificationManager = Depends(get_notification_manager),
    current_user: dict = Depends(get_current_user)
):
    """Send multiple notifications in bulk."""
    try:
        # Create notification objects
        notifications = []
        for req in request.notifications:
            notification = Notification(
                user_id=req.user_id,
                notification_type=req.notification_type,
                title=req.title,
                message=req.message,
                priority=req.priority,
                channels=req.channels,
                template_id=req.template_id,
                template_data=req.template_data,
                scheduled_at=req.scheduled_at,
                expires_at=req.expires_at,
                metadata=req.metadata
            )
            notifications.append(notification)
        
        # Send bulk notifications
        results = await manager.send_bulk_notifications(notifications)
        
        # Format response
        response = {}
        for notification_id, delivery_results in results.items():
            response[notification_id] = NotificationResponse(
                success=len(delivery_results) > 0,
                notification_id=notification_id,
                message="Bulk notification processed",
                delivery_results=[{
                    'channel': result.channel.value,
                    'status': result.status.value,
                    'sent_at': result.sent_at.isoformat() if result.sent_at else None,
                    'delivered_at': result.delivered_at.isoformat() if result.delivered_at else None,
                    'error_message': result.error_message
                } for result in delivery_results]
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to send bulk notifications: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send/template/{template_id}")
async def send_notification_from_template(
    template_id: str,
    user_id: str = Query(..., description="Target user ID"),
    template_data: Dict[str, Any] = Field(..., description="Template data"),
    channels: Optional[List[ChannelType]] = Query(None, description="Override channels"),
    priority: NotificationPriority = Query(NotificationPriority.NORMAL, description="Override priority"),
    manager: NotificationManager = Depends(get_notification_manager),
    current_user: dict = Depends(get_current_user)
):
    """Send notification from template."""
    try:
        # Create notification from template
        notification = await manager.create_notification_from_template(
            template_id=template_id,
            user_id=user_id,
            template_data=template_data,
            channels=channels,
            priority=priority
        )
        
        # Send notification
        delivery_results = await manager.send_notification(notification)
        
        return NotificationResponse(
            success=True,
            notification_id=notification.id,
            message="Template notification sent successfully",
            delivery_results=[{
                'channel': result.channel.value,
                'status': result.status.value,
                'sent_at': result.sent_at.isoformat() if result.sent_at else None,
                'delivered_at': result.delivered_at.isoformat() if result.delivered_at else None,
                'error_message': result.error_message
            } for result in delivery_results]
        )
        
    except Exception as e:
        logger.error(f"Failed to send template notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{notification_id}")
async def get_notification_status(
    notification_id: str,
    manager: NotificationManager = Depends(get_notification_manager),
    current_user: dict = Depends(get_current_user)
):
    """Get notification delivery status."""
    try:
        status = await manager.get_notification_status(notification_id)
        return status
        
    except Exception as e:
        logger.error(f"Failed to get notification status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/schedule")
async def schedule_notification(
    request: NotificationRequest,
    scheduled_at: datetime = Query(..., description="Scheduled delivery time"),
    manager: NotificationManager = Depends(get_notification_manager),
    current_user: dict = Depends(get_current_user)
):
    """Schedule a notification for future delivery."""
    try:
        # Create notification object
        notification = Notification(
            user_id=request.user_id,
            notification_type=request.notification_type,
            title=request.title,
            message=request.message,
            priority=request.priority,
            channels=request.channels,
            template_id=request.template_id,
            template_data=request.template_data,
            scheduled_at=scheduled_at,
            expires_at=request.expires_at,
            metadata=request.metadata
        )
        
        # Schedule notification
        schedule_id = await manager.schedule_notification(notification, scheduled_at)
        
        return {
            "success": True,
            "schedule_id": schedule_id,
            "notification_id": notification.id,
            "scheduled_at": scheduled_at.isoformat(),
            "message": "Notification scheduled successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to schedule notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/schedule/{schedule_id}")
async def cancel_scheduled_notification(
    schedule_id: str,
    manager: NotificationManager = Depends(get_notification_manager),
    current_user: dict = Depends(get_current_user)
):
    """Cancel a scheduled notification."""
    try:
        success = await manager.cancel_notification(schedule_id)
        
        if success:
            return {"success": True, "message": "Notification cancelled successfully"}
        else:
            raise HTTPException(status_code=404, detail="Schedule ID not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to cancel notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/retry/{notification_id}")
async def retry_notification(
    notification_id: str,
    manager: NotificationManager = Depends(get_notification_manager),
    current_user: dict = Depends(get_current_user)
):
    """Retry a failed notification."""
    try:
        retry_count = await manager.retry_failed_notifications(notification_id)
        
        return {
            "success": True,
            "retry_count": retry_count,
            "message": f"Retried {retry_count} notifications"
        }
        
    except Exception as e:
        logger.error(f"Failed to retry notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/retry/failed")
async def retry_all_failed_notifications(
    hours_back: int = Query(24, description="Hours back to look for failed notifications"),
    manager: NotificationManager = Depends(get_notification_manager),
    current_user: dict = Depends(get_current_user)
):
    """Retry all failed notifications."""
    try:
        retry_count = await manager.retry_failed_notifications(hours_back=hours_back)
        
        return {
            "success": True,
            "retry_count": retry_count,
            "message": f"Retried {retry_count} failed notifications"
        }
        
    except Exception as e:
        logger.error(f"Failed to retry failed notifications: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Template Management Endpoints

@router.post("/templates")
async def create_template(
    request: TemplateRequest,
    manager: NotificationManager = Depends(get_notification_manager),
    current_user: dict = Depends(get_current_user)
):
    """Create a new notification template."""
    try:
        # This would create a template in the database
        # For now, return success
        return {
            "success": True,
            "template_id": "template_123",
            "message": "Template created successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to create template: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates")
async def get_templates(
    notification_type: Optional[NotificationType] = Query(None, description="Filter by notification type"),
    manager: NotificationManager = Depends(get_notification_manager),
    current_user: dict = Depends(get_current_user)
):
    """Get notification templates."""
    try:
        # This would query templates from database
        # For now, return mock data
        templates = [
            {
                "id": "template_1",
                "name": "Trading Alert Template",
                "notification_type": "trading_alert",
                "template_type": "html",
                "channels": ["email", "push"]
            }
        ]
        
        if notification_type:
            templates = [t for t in templates if t["notification_type"] == notification_type.value]
        
        return {"templates": templates}
        
    except Exception as e:
        logger.error(f"Failed to get templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Preference Management Endpoints

@router.post("/preferences")
async def set_preference(
    request: PreferenceRequest,
    manager: NotificationManager = Depends(get_notification_manager),
    current_user: dict = Depends(get_current_user)
):
    """Set user notification preference."""
    try:
        # This would save preference to database
        # For now, return success
        return {
            "success": True,
            "message": "Preference set successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to set preference: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/preferences/{user_id}")
async def get_preferences(
    user_id: str,
    manager: NotificationManager = Depends(get_notification_manager),
    current_user: dict = Depends(get_current_user)
):
    """Get user notification preferences."""
    try:
        # This would query preferences from database
        # For now, return mock data
        preferences = {
            "user_id": user_id,
            "preferences": [
                {
                    "notification_type": "trading_alert",
                    "channels": ["email", "push"],
                    "is_enabled": True,
                    "priority_threshold": "normal"
                }
            ]
        }
        
        return preferences
        
    except Exception as e:
        logger.error(f"Failed to get preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Analytics Endpoints

@router.get("/analytics/stats")
async def get_notification_stats(
    start_date: Optional[datetime] = Query(None, description="Start date"),
    end_date: Optional[datetime] = Query(None, description="End date"),
    manager: NotificationManager = Depends(get_notification_manager),
    current_user: dict = Depends(get_current_user)
):
    """Get notification statistics."""
    try:
        # Use default date range if not provided
        if not start_date:
            start_date = datetime.now() - timedelta(days=7)
        if not end_date:
            end_date = datetime.now()
        
        # Get metrics from analytics tracker
        metrics = await manager.analytics_tracker.get_delivery_metrics(
            start_date, end_date
        )
        
        return {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "metrics": {
                "total_sent": metrics.total_sent,
                "total_delivered": metrics.total_delivered,
                "total_failed": metrics.total_failed,
                "delivery_rate": metrics.delivery_rate,
                "average_delivery_time": metrics.average_delivery_time,
                "channel_metrics": metrics.channel_metrics,
                "type_metrics": metrics.type_metrics
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get notification stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/real-time")
async def get_real_time_stats(
    manager: NotificationManager = Depends(get_notification_manager),
    current_user: dict = Depends(get_current_user)
):
    """Get real-time notification statistics."""
    try:
        stats = await manager.analytics_tracker.get_real_time_stats()
        return stats
        
    except Exception as e:
        logger.error(f"Failed to get real-time stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Health Check Endpoint

@router.get("/health")
async def health_check(
    manager: NotificationManager = Depends(get_notification_manager)
):
    """Health check endpoint."""
    try:
        # Get engine stats
        engine_stats = await manager.notification_engine.get_engine_stats()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "engine_stats": engine_stats
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
        )
