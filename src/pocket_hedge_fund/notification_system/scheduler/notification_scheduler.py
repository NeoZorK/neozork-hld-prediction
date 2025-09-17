"""
Notification Scheduler

Scheduler for delayed and recurring notifications.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
import uuid

from ..models.notification_models import Notification, NotificationEvent

logger = logging.getLogger(__name__)


class NotificationScheduler:
    """
    Scheduler for delayed and recurring notifications.
    """
    
    def __init__(self):
        """Initialize notification scheduler."""
        self.scheduled_notifications = {}
        self.recurring_notifications = {}
        self.is_running = False
        self.scheduler_task = None
        self.cleanup_task = None
        self.notification_callback = None
    
    async def initialize(self):
        """Initialize notification scheduler."""
        try:
            # Start scheduler task
            self.scheduler_task = asyncio.create_task(self._scheduler_loop())
            
            # Start cleanup task
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())
            
            self.is_running = True
            logger.info("Notification scheduler initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize notification scheduler: {e}")
            raise
    
    async def schedule_notification(
        self,
        notification: Notification,
        scheduled_at: Optional[datetime] = None
    ) -> str:
        """
        Schedule a notification for future delivery.
        
        Args:
            notification: Notification to schedule
            scheduled_at: When to deliver (defaults to notification.scheduled_at)
            
        Returns:
            Schedule ID
        """
        try:
            # Determine scheduled time
            if scheduled_at:
                notification.scheduled_at = scheduled_at
            elif not notification.scheduled_at:
                raise ValueError("No scheduled time provided")
            
            # Generate schedule ID
            schedule_id = str(uuid.uuid4())
            
            # Store scheduled notification
            self.scheduled_notifications[schedule_id] = {
                'notification': notification,
                'scheduled_at': notification.scheduled_at,
                'created_at': datetime.now(),
                'status': 'scheduled'
            }
            
            logger.info(f"Scheduled notification {notification.id} for {notification.scheduled_at}")
            return schedule_id
            
        except Exception as e:
            logger.error(f"Failed to schedule notification: {e}")
            raise
    
    async def schedule_recurring_notification(
        self,
        notification: Notification,
        cron_expression: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> str:
        """
        Schedule a recurring notification.
        
        Args:
            notification: Base notification template
            cron_expression: Cron expression for recurrence
            start_date: When to start (defaults to now)
            end_date: When to end (optional)
            
        Returns:
            Schedule ID
        """
        try:
            # Generate schedule ID
            schedule_id = str(uuid.uuid4())
            
            # Store recurring notification
            self.recurring_notifications[schedule_id] = {
                'notification': notification,
                'cron_expression': cron_expression,
                'start_date': start_date or datetime.now(),
                'end_date': end_date,
                'created_at': datetime.now(),
                'status': 'active',
                'last_run': None,
                'next_run': self._calculate_next_run(cron_expression, datetime.now())
            }
            
            logger.info(f"Scheduled recurring notification {notification.id} with cron {cron_expression}")
            return schedule_id
            
        except Exception as e:
            logger.error(f"Failed to schedule recurring notification: {e}")
            raise
    
    async def cancel_notification(self, schedule_id: str) -> bool:
        """
        Cancel a scheduled notification.
        
        Args:
            schedule_id: Schedule ID to cancel
            
        Returns:
            True if cancelled successfully
        """
        try:
            # Check if it's a scheduled notification
            if schedule_id in self.scheduled_notifications:
                self.scheduled_notifications[schedule_id]['status'] = 'cancelled'
                logger.info(f"Cancelled scheduled notification {schedule_id}")
                return True
            
            # Check if it's a recurring notification
            if schedule_id in self.recurring_notifications:
                self.recurring_notifications[schedule_id]['status'] = 'cancelled'
                logger.info(f"Cancelled recurring notification {schedule_id}")
                return True
            
            logger.warning(f"Schedule ID {schedule_id} not found")
            return False
            
        except Exception as e:
            logger.error(f"Failed to cancel notification: {e}")
            return False
    
    async def get_scheduled_notifications(
        self,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get scheduled notifications.
        
        Args:
            status: Filter by status (optional)
            
        Returns:
            List of scheduled notifications
        """
        try:
            notifications = []
            
            # Add scheduled notifications
            for schedule_id, schedule_data in self.scheduled_notifications.items():
                if status is None or schedule_data['status'] == status:
                    notifications.append({
                        'schedule_id': schedule_id,
                        'notification_id': schedule_data['notification'].id,
                        'scheduled_at': schedule_data['scheduled_at'],
                        'created_at': schedule_data['created_at'],
                        'status': schedule_data['status'],
                        'type': 'scheduled'
                    })
            
            # Add recurring notifications
            for schedule_id, schedule_data in self.recurring_notifications.items():
                if status is None or schedule_data['status'] == status:
                    notifications.append({
                        'schedule_id': schedule_id,
                        'notification_id': schedule_data['notification'].id,
                        'cron_expression': schedule_data['cron_expression'],
                        'next_run': schedule_data['next_run'],
                        'created_at': schedule_data['created_at'],
                        'status': schedule_data['status'],
                        'type': 'recurring'
                    })
            
            return notifications
            
        except Exception as e:
            logger.error(f"Failed to get scheduled notifications: {e}")
            return []
    
    async def _scheduler_loop(self):
        """Main scheduler loop."""
        try:
            while self.is_running:
                current_time = datetime.now()
                
                # Process scheduled notifications
                await self._process_scheduled_notifications(current_time)
                
                # Process recurring notifications
                await self._process_recurring_notifications(current_time)
                
                # Wait before next iteration
                await asyncio.sleep(1)  # Check every second
                
        except Exception as e:
            logger.error(f"Scheduler loop error: {e}")
    
    async def _process_scheduled_notifications(self, current_time: datetime):
        """Process scheduled notifications that are due."""
        try:
            due_notifications = []
            
            for schedule_id, schedule_data in self.scheduled_notifications.items():
                if (schedule_data['status'] == 'scheduled' and 
                    schedule_data['scheduled_at'] <= current_time):
                    due_notifications.append((schedule_id, schedule_data))
            
            # Process due notifications
            for schedule_id, schedule_data in due_notifications:
                try:
                    notification = schedule_data['notification']
                    
                    # Mark as processing
                    schedule_data['status'] = 'processing'
                    
                    # Trigger notification delivery
                    if self.notification_callback:
                        await self.notification_callback(notification)
                    
                    # Mark as completed
                    schedule_data['status'] = 'completed'
                    schedule_data['completed_at'] = current_time
                    
                    logger.info(f"Processed scheduled notification {notification.id}")
                    
                except Exception as e:
                    logger.error(f"Failed to process scheduled notification {schedule_id}: {e}")
                    schedule_data['status'] = 'failed'
                    schedule_data['error'] = str(e)
                    
        except Exception as e:
            logger.error(f"Error processing scheduled notifications: {e}")
    
    async def _process_recurring_notifications(self, current_time: datetime):
        """Process recurring notifications that are due."""
        try:
            due_notifications = []
            
            for schedule_id, schedule_data in self.recurring_notifications.items():
                if (schedule_data['status'] == 'active' and 
                    schedule_data['next_run'] and 
                    schedule_data['next_run'] <= current_time):
                    due_notifications.append((schedule_id, schedule_data))
            
            # Process due notifications
            for schedule_id, schedule_data in due_notifications:
                try:
                    notification = schedule_data['notification']
                    
                    # Check if we're within the date range
                    if (schedule_data['end_date'] and 
                        current_time > schedule_data['end_date']):
                        schedule_data['status'] = 'expired'
                        continue
                    
                    # Trigger notification delivery
                    if self.notification_callback:
                        await self.notification_callback(notification)
                    
                    # Update last run and calculate next run
                    schedule_data['last_run'] = current_time
                    schedule_data['next_run'] = self._calculate_next_run(
                        schedule_data['cron_expression'], current_time
                    )
                    
                    logger.info(f"Processed recurring notification {notification.id}")
                    
                except Exception as e:
                    logger.error(f"Failed to process recurring notification {schedule_id}: {e}")
                    schedule_data['status'] = 'failed'
                    schedule_data['error'] = str(e)
                    
        except Exception as e:
            logger.error(f"Error processing recurring notifications: {e}")
    
    def _calculate_next_run(self, cron_expression: str, from_time: datetime) -> Optional[datetime]:
        """
        Calculate next run time from cron expression.
        
        Args:
            cron_expression: Cron expression
            from_time: Time to calculate from
            
        Returns:
            Next run time or None if invalid
        """
        try:
            # Simple cron parser for common patterns
            # In a real implementation, you would use a proper cron library
            
            parts = cron_expression.split()
            if len(parts) != 5:
                logger.error(f"Invalid cron expression: {cron_expression}")
                return None
            
            minute, hour, day, month, weekday = parts
            
            # For now, implement simple patterns
            if cron_expression == "0 * * * *":  # Every hour
                next_run = from_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            elif cron_expression == "0 0 * * *":  # Daily at midnight
                next_run = from_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            elif cron_expression == "0 0 * * 0":  # Weekly on Sunday
                days_until_sunday = (6 - from_time.weekday()) % 7
                if days_until_sunday == 0:
                    days_until_sunday = 7
                next_run = from_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=days_until_sunday)
            elif cron_expression == "0 0 1 * *":  # Monthly on 1st
                if from_time.month == 12:
                    next_run = from_time.replace(year=from_time.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                else:
                    next_run = from_time.replace(month=from_time.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
            else:
                # Default to daily
                next_run = from_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            
            return next_run
            
        except Exception as e:
            logger.error(f"Failed to calculate next run time: {e}")
            return None
    
    async def _cleanup_loop(self):
        """Cleanup loop for old notifications."""
        try:
            while self.is_running:
                # Wait 1 hour before cleanup
                await asyncio.sleep(3600)
                
                # Cleanup old completed notifications
                cutoff_time = datetime.now() - timedelta(days=7)
                
                # Cleanup scheduled notifications
                to_remove = []
                for schedule_id, schedule_data in self.scheduled_notifications.items():
                    if (schedule_data['status'] in ['completed', 'failed', 'cancelled'] and
                        schedule_data['created_at'] < cutoff_time):
                        to_remove.append(schedule_id)
                
                for schedule_id in to_remove:
                    del self.scheduled_notifications[schedule_id]
                
                # Cleanup recurring notifications
                to_remove = []
                for schedule_id, schedule_data in self.recurring_notifications.items():
                    if (schedule_data['status'] in ['cancelled', 'expired'] and
                        schedule_data['created_at'] < cutoff_time):
                        to_remove.append(schedule_id)
                
                for schedule_id in to_remove:
                    del self.recurring_notifications[schedule_id]
                
                if to_remove:
                    logger.info(f"Cleaned up {len(to_remove)} old notifications")
                    
        except Exception as e:
            logger.error(f"Cleanup loop error: {e}")
    
    def set_notification_callback(self, callback: Callable):
        """Set callback function for notification delivery."""
        self.notification_callback = callback
    
    async def get_scheduler_stats(self) -> Dict[str, Any]:
        """Get scheduler statistics."""
        try:
            stats = {
                'is_running': self.is_running,
                'scheduled_count': len(self.scheduled_notifications),
                'recurring_count': len(self.recurring_notifications),
                'status_counts': {
                    'scheduled': 0,
                    'processing': 0,
                    'completed': 0,
                    'failed': 0,
                    'cancelled': 0,
                    'active': 0,
                    'expired': 0
                }
            }
            
            # Count scheduled notification statuses
            for schedule_data in self.scheduled_notifications.values():
                status = schedule_data['status']
                if status in stats['status_counts']:
                    stats['status_counts'][status] += 1
            
            # Count recurring notification statuses
            for schedule_data in self.recurring_notifications.values():
                status = schedule_data['status']
                if status in stats['status_counts']:
                    stats['status_counts'][status] += 1
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get scheduler stats: {e}")
            return {}
    
    async def stop(self):
        """Stop the scheduler."""
        try:
            self.is_running = False
            
            # Cancel tasks
            if self.scheduler_task:
                self.scheduler_task.cancel()
            
            if self.cleanup_task:
                self.cleanup_task.cancel()
            
            # Wait for tasks to finish
            tasks = [self.scheduler_task, self.cleanup_task]
            await asyncio.gather(*[t for t in tasks if t], return_exceptions=True)
            
            logger.info("Notification scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")
    
    async def cleanup(self):
        """Cleanup scheduler resources."""
        try:
            await self.stop()
            
            # Clear all notifications
            self.scheduled_notifications.clear()
            self.recurring_notifications.clear()
            
            logger.info("Notification scheduler cleanup completed")
        except Exception as e:
            logger.error(f"Error during scheduler cleanup: {e}")
