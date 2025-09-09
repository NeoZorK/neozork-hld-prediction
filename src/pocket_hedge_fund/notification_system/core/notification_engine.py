"""
Notification Engine

Core engine for processing and delivering notifications.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from decimal import Decimal

from ..models.notification_models import (
    Notification, NotificationHistory, DeliveryStatus,
    NotificationPriority, ChannelType, RetryPolicy
)

logger = logging.getLogger(__name__)


class NotificationEngine:
    """
    Core notification engine for processing and delivering notifications.
    """
    
    def __init__(self, db_manager=None):
        """Initialize notification engine."""
        self.db_manager = db_manager
        self.processing_queue = asyncio.Queue()
        self.retry_queue = asyncio.Queue()
        self.is_running = False
        self.workers = []
        self.max_workers = 5
        self.rate_limits = {}
        self.delivery_stats = {}
    
    async def initialize(self):
        """Initialize notification engine."""
        try:
            # Start background workers
            await self._start_workers()
            
            # Load rate limits and stats
            await self._load_configuration()
            
            self.is_running = True
            logger.info("Notification engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize notification engine: {e}")
            raise
    
    async def _start_workers(self):
        """Start background worker processes."""
        try:
            # Start main processing workers
            for i in range(self.max_workers):
                worker = asyncio.create_task(self._processing_worker(f"worker-{i}"))
                self.workers.append(worker)
            
            # Start retry worker
            retry_worker = asyncio.create_task(self._retry_worker())
            self.workers.append(retry_worker)
            
            logger.info(f"Started {self.max_workers} processing workers and 1 retry worker")
        except Exception as e:
            logger.error(f"Failed to start workers: {e}")
            raise
    
    async def _processing_worker(self, worker_name: str):
        """Background worker for processing notifications."""
        try:
            while self.is_running:
                try:
                    # Get notification from queue with timeout
                    notification = await asyncio.wait_for(
                        self.processing_queue.get(), timeout=1.0
                    )
                    
                    # Process notification
                    await self._process_notification(notification, worker_name)
                    
                    # Mark task as done
                    self.processing_queue.task_done()
                    
                except asyncio.TimeoutError:
                    # No notifications to process, continue
                    continue
                except Exception as e:
                    logger.error(f"Worker {worker_name} error: {e}")
                    await asyncio.sleep(1)
                    
        except Exception as e:
            logger.error(f"Worker {worker_name} failed: {e}")
    
    async def _retry_worker(self):
        """Background worker for retrying failed notifications."""
        try:
            while self.is_running:
                try:
                    # Get retry item from queue with timeout
                    retry_item = await asyncio.wait_for(
                        self.retry_queue.get(), timeout=5.0
                    )
                    
                    # Process retry
                    await self._process_retry(retry_item)
                    
                    # Mark task as done
                    self.retry_queue.task_done()
                    
                except asyncio.TimeoutError:
                    # No retries to process, continue
                    continue
                except Exception as e:
                    logger.error(f"Retry worker error: {e}")
                    await asyncio.sleep(1)
                    
        except Exception as e:
            logger.error(f"Retry worker failed: {e}")
    
    async def _process_notification(
        self,
        notification: Notification,
        worker_name: str
    ):
        """Process a single notification."""
        try:
            logger.info(f"Processing notification {notification.id} with {worker_name}")
            
            # Check rate limits
            if not await self._check_rate_limits(notification):
                logger.warning(f"Rate limit exceeded for notification {notification.id}")
                return
            
            # Validate notification
            if not await self._validate_notification(notification):
                logger.error(f"Invalid notification {notification.id}")
                return
            
            # Process each channel
            for channel in notification.channels:
                try:
                    await self._process_channel(notification, channel)
                except Exception as e:
                    logger.error(f"Failed to process channel {channel} for notification {notification.id}: {e}")
            
            # Update delivery stats
            await self._update_delivery_stats(notification)
            
        except Exception as e:
            logger.error(f"Failed to process notification {notification.id}: {e}")
    
    async def _process_channel(
        self,
        notification: Notification,
        channel: ChannelType
    ):
        """Process notification for a specific channel."""
        try:
            # Check channel-specific rate limits
            if not await self._check_channel_rate_limit(channel):
                logger.warning(f"Rate limit exceeded for channel {channel}")
                return
            
            # Create delivery history record
            history = NotificationHistory(
                notification_id=notification.id,
                user_id=notification.user_id,
                channel=channel,
                status=DeliveryStatus.PENDING
            )
            
            # Attempt delivery
            success = await self._attempt_delivery(notification, channel, history)
            
            if success:
                history.status = DeliveryStatus.DELIVERED
                history.delivered_at = datetime.now()
                logger.info(f"Successfully delivered notification {notification.id} via {channel}")
            else:
                history.status = DeliveryStatus.FAILED
                history.failed_at = datetime.now()
                
                # Check if retry is needed
                if await self._should_retry(notification, history):
                    await self._schedule_retry(notification, channel, history)
                
                logger.warning(f"Failed to deliver notification {notification.id} via {channel}")
            
            # Save delivery history
            await self._save_delivery_history(history)
            
        except Exception as e:
            logger.error(f"Error processing channel {channel} for notification {notification.id}: {e}")
    
    async def _attempt_delivery(
        self,
        notification: Notification,
        channel: ChannelType,
        history: NotificationHistory
    ) -> bool:
        """Attempt to deliver notification via channel."""
        try:
            # This would integrate with actual channel implementations
            # For now, simulate delivery with some failures
            
            # Simulate delivery time
            await asyncio.sleep(0.1)
            
            # Simulate occasional failures (10% failure rate)
            import random
            if random.random() < 0.1:
                history.error_message = "Simulated delivery failure"
                return False
            
            return True
            
        except Exception as e:
            history.error_message = str(e)
            return False
    
    async def _should_retry(
        self,
        notification: Notification,
        history: NotificationHistory
    ) -> bool:
        """Check if notification should be retried."""
        try:
            if not notification.retry_policy:
                return False
            
            if history.retry_count >= notification.retry_policy.max_retries:
                return False
            
            # Check if enough time has passed since last attempt
            if history.delivery_attempts:
                last_attempt = max(history.delivery_attempts)
                delay = notification.retry_policy.retry_delay
                if datetime.now() - last_attempt < timedelta(seconds=delay):
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking retry eligibility: {e}")
            return False
    
    async def _schedule_retry(
        self,
        notification: Notification,
        channel: ChannelType,
        history: NotificationHistory
    ):
        """Schedule notification for retry."""
        try:
            retry_item = {
                'notification': notification,
                'channel': channel,
                'history': history,
                'scheduled_at': datetime.now() + timedelta(
                    seconds=notification.retry_policy.retry_delay
                )
            }
            
            await self.retry_queue.put(retry_item)
            logger.info(f"Scheduled retry for notification {notification.id} via {channel}")
            
        except Exception as e:
            logger.error(f"Failed to schedule retry: {e}")
    
    async def _process_retry(self, retry_item: Dict[str, Any]):
        """Process a retry item."""
        try:
            notification = retry_item['notification']
            channel = retry_item['channel']
            history = retry_item['history']
            
            # Check if retry is still needed
            if not await self._should_retry(notification, history):
                return
            
            # Increment retry count
            history.retry_count += 1
            history.delivery_attempts.append(datetime.now())
            
            # Attempt delivery again
            success = await self._attempt_delivery(notification, channel, history)
            
            if success:
                history.status = DeliveryStatus.DELIVERED
                history.delivered_at = datetime.now()
                logger.info(f"Retry successful for notification {notification.id} via {channel}")
            else:
                history.status = DeliveryStatus.FAILED
                history.failed_at = datetime.now()
                
                # Schedule another retry if needed
                if await self._should_retry(notification, history):
                    await self._schedule_retry(notification, channel, history)
                else:
                    logger.error(f"Max retries exceeded for notification {notification.id} via {channel}")
            
            # Save updated history
            await self._save_delivery_history(history)
            
        except Exception as e:
            logger.error(f"Failed to process retry: {e}")
    
    async def _check_rate_limits(self, notification: Notification) -> bool:
        """Check if notification is within rate limits."""
        try:
            # Check global rate limits
            user_key = f"user:{notification.user_id}"
            if user_key in self.rate_limits:
                limit = self.rate_limits[user_key]
                if limit['count'] >= limit['max_per_hour']:
                    return False
            
            # Check notification type rate limits
            type_key = f"type:{notification.notification_type}"
            if type_key in self.rate_limits:
                limit = self.rate_limits[type_key]
                if limit['count'] >= limit['max_per_hour']:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking rate limits: {e}")
            return True  # Allow on error
    
    async def _check_channel_rate_limit(self, channel: ChannelType) -> bool:
        """Check channel-specific rate limits."""
        try:
            channel_key = f"channel:{channel}"
            if channel_key in self.rate_limits:
                limit = self.rate_limits[channel_key]
                if limit['count'] >= limit['max_per_minute']:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking channel rate limit: {e}")
            return True  # Allow on error
    
    async def _validate_notification(self, notification: Notification) -> bool:
        """Validate notification before processing."""
        try:
            # Check required fields
            if not notification.user_id:
                logger.error("Notification missing user_id")
                return False
            
            if not notification.title and not notification.message:
                logger.error("Notification missing title and message")
                return False
            
            if not notification.channels:
                logger.error("Notification missing channels")
                return False
            
            # Check expiration
            if notification.expires_at and notification.expires_at < datetime.now():
                logger.warning(f"Notification {notification.id} has expired")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating notification: {e}")
            return False
    
    async def _update_delivery_stats(self, notification: Notification):
        """Update delivery statistics."""
        try:
            stats_key = f"stats:{notification.notification_type}"
            if stats_key not in self.delivery_stats:
                self.delivery_stats[stats_key] = {
                    'total': 0,
                    'delivered': 0,
                    'failed': 0
                }
            
            self.delivery_stats[stats_key]['total'] += 1
            
        except Exception as e:
            logger.error(f"Error updating delivery stats: {e}")
    
    async def _save_delivery_history(self, history: NotificationHistory):
        """Save delivery history to database."""
        try:
            if self.db_manager:
                # This would save to database
                # For now, just log
                logger.debug(f"Saved delivery history for notification {history.notification_id}")
            else:
                logger.debug(f"Mock saved delivery history for notification {history.notification_id}")
                
        except Exception as e:
            logger.error(f"Error saving delivery history: {e}")
    
    async def _load_configuration(self):
        """Load engine configuration."""
        try:
            # Load rate limits
            self.rate_limits = {
                'user:default': {'count': 0, 'max_per_hour': 100},
                'type:trading_alert': {'count': 0, 'max_per_hour': 50},
                'channel:email': {'count': 0, 'max_per_minute': 10},
                'channel:sms': {'count': 0, 'max_per_minute': 5}
            }
            
            logger.info("Loaded notification engine configuration")
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
    
    async def queue_notification(self, notification: Notification):
        """Queue notification for processing."""
        try:
            await self.processing_queue.put(notification)
            logger.info(f"Queued notification {notification.id} for processing")
        except Exception as e:
            logger.error(f"Failed to queue notification: {e}")
            raise
    
    async def get_engine_stats(self) -> Dict[str, Any]:
        """Get engine statistics."""
        try:
            return {
                'is_running': self.is_running,
                'queue_size': self.processing_queue.qsize(),
                'retry_queue_size': self.retry_queue.qsize(),
                'active_workers': len([w for w in self.workers if not w.done()]),
                'delivery_stats': self.delivery_stats,
                'rate_limits': self.rate_limits
            }
        except Exception as e:
            logger.error(f"Error getting engine stats: {e}")
            return {}
    
    async def stop(self):
        """Stop the notification engine."""
        try:
            self.is_running = False
            
            # Cancel all workers
            for worker in self.workers:
                worker.cancel()
            
            # Wait for workers to finish
            await asyncio.gather(*self.workers, return_exceptions=True)
            
            logger.info("Notification engine stopped")
        except Exception as e:
            logger.error(f"Error stopping notification engine: {e}")
    
    async def cleanup(self):
        """Cleanup resources."""
        try:
            await self.stop()
            
            # Clear queues
            while not self.processing_queue.empty():
                self.processing_queue.get_nowait()
            
            while not self.retry_queue.empty():
                self.retry_queue.get_nowait()
            
            # Clear stats
            self.delivery_stats.clear()
            self.rate_limits.clear()
            
            logger.info("Notification engine cleanup completed")
        except Exception as e:
            logger.error(f"Error during notification engine cleanup: {e}")
