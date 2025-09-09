"""
Analytics Tracker

Tracks notification analytics and metrics.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from decimal import Decimal
import json

from ..models.notification_models import (
    Notification, NotificationHistory, NotificationMetrics,
    DeliveryStatus, NotificationType, ChannelType, NotificationPriority
)

logger = logging.getLogger(__name__)


class AnalyticsTracker:
    """
    Tracks notification analytics and metrics.
    """
    
    def __init__(self, db_manager=None):
        """Initialize analytics tracker."""
        self.db_manager = db_manager
        self.metrics_cache = {}
        self.real_time_stats = {
            'total_sent': 0,
            'total_delivered': 0,
            'total_failed': 0,
            'channel_stats': {},
            'type_stats': {},
            'hourly_stats': {}
        }
        self.aggregation_interval = 60  # seconds
        self.last_aggregation = datetime.now()
    
    async def initialize(self):
        """Initialize analytics tracker."""
        try:
            # Load historical metrics
            await self._load_historical_metrics()
            
            # Start background aggregation task
            asyncio.create_task(self._aggregation_worker())
            
            logger.info("Analytics tracker initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize analytics tracker: {e}")
            raise
    
    async def _aggregation_worker(self):
        """Background worker for aggregating metrics."""
        try:
            while True:
                await asyncio.sleep(self.aggregation_interval)
                await self._aggregate_metrics()
        except Exception as e:
            logger.error(f"Aggregation worker failed: {e}")
    
    async def _aggregate_metrics(self):
        """Aggregate real-time metrics."""
        try:
            current_time = datetime.now()
            hour_key = current_time.strftime('%Y-%m-%d-%H')
            
            # Update hourly stats
            if hour_key not in self.real_time_stats['hourly_stats']:
                self.real_time_stats['hourly_stats'][hour_key] = {
                    'sent': 0,
                    'delivered': 0,
                    'failed': 0
                }
            
            # Store current hour's stats
            self.real_time_stats['hourly_stats'][hour_key] = {
                'sent': self.real_time_stats['total_sent'],
                'delivered': self.real_time_stats['total_delivered'],
                'failed': self.real_time_stats['total_failed']
            }
            
            # Clean up old hourly stats (keep last 24 hours)
            cutoff_time = current_time - timedelta(hours=24)
            cutoff_key = cutoff_time.strftime('%Y-%m-%d-%H')
            
            keys_to_remove = [
                key for key in self.real_time_stats['hourly_stats'].keys()
                if key < cutoff_key
            ]
            
            for key in keys_to_remove:
                del self.real_time_stats['hourly_stats'][key]
            
            self.last_aggregation = current_time
            
        except Exception as e:
            logger.error(f"Failed to aggregate metrics: {e}")
    
    async def track_notification_sent(
        self,
        notification: Notification,
        delivery_results: List[NotificationHistory]
    ):
        """
        Track notification sent event.
        
        Args:
            notification: Notification that was sent
            delivery_results: Delivery results for each channel
        """
        try:
            # Update real-time stats
            self.real_time_stats['total_sent'] += 1
            
            # Update channel stats
            for result in delivery_results:
                channel = result.channel
                if channel not in self.real_time_stats['channel_stats']:
                    self.real_time_stats['channel_stats'][channel] = {
                        'sent': 0,
                        'delivered': 0,
                        'failed': 0
                    }
                
                self.real_time_stats['channel_stats'][channel]['sent'] += 1
                
                if result.status == DeliveryStatus.DELIVERED:
                    self.real_time_stats['total_delivered'] += 1
                    self.real_time_stats['channel_stats'][channel]['delivered'] += 1
                elif result.status == DeliveryStatus.FAILED:
                    self.real_time_stats['total_failed'] += 1
                    self.real_time_stats['channel_stats'][channel]['failed'] += 1
            
            # Update type stats
            notification_type = notification.notification_type
            if notification_type not in self.real_time_stats['type_stats']:
                self.real_time_stats['type_stats'][notification_type] = {
                    'sent': 0,
                    'delivered': 0,
                    'failed': 0
                }
            
            self.real_time_stats['type_stats'][notification_type]['sent'] += 1
            
            # Save delivery history
            await self._save_delivery_history(delivery_results)
            
            logger.debug(f"Tracked notification {notification.id} sent event")
            
        except Exception as e:
            logger.error(f"Failed to track notification sent: {e}")
    
    async def track_notification_delivered(
        self,
        notification_id: str,
        channel: ChannelType,
        delivered_at: datetime
    ):
        """
        Track notification delivered event.
        
        Args:
            notification_id: Notification ID
            channel: Delivery channel
            delivered_at: When it was delivered
        """
        try:
            # Update real-time stats
            if channel in self.real_time_stats['channel_stats']:
                self.real_time_stats['channel_stats'][channel]['delivered'] += 1
            
            # Update delivery history
            await self._update_delivery_status(
                notification_id, channel, DeliveryStatus.DELIVERED, delivered_at
            )
            
            logger.debug(f"Tracked notification {notification_id} delivered via {channel}")
            
        except Exception as e:
            logger.error(f"Failed to track notification delivered: {e}")
    
    async def track_notification_failed(
        self,
        notification_id: str,
        channel: ChannelType,
        error_message: str,
        failed_at: datetime
    ):
        """
        Track notification failed event.
        
        Args:
            notification_id: Notification ID
            channel: Delivery channel
            error_message: Error message
            failed_at: When it failed
        """
        try:
            # Update real-time stats
            if channel in self.real_time_stats['channel_stats']:
                self.real_time_stats['channel_stats'][channel]['failed'] += 1
            
            # Update delivery history
            await self._update_delivery_status(
                notification_id, channel, DeliveryStatus.FAILED, failed_at, error_message
            )
            
            logger.debug(f"Tracked notification {notification_id} failed via {channel}: {error_message}")
            
        except Exception as e:
            logger.error(f"Failed to track notification failed: {e}")
    
    async def get_notification_history(
        self,
        notification_id: str
    ) -> List[NotificationHistory]:
        """
        Get delivery history for a notification.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            List of delivery history records
        """
        try:
            if self.db_manager:
                # This would query the database
                # For now, return mock data
                return []
            else:
                # Mock implementation
                return []
                
        except Exception as e:
            logger.error(f"Failed to get notification history: {e}")
            return []
    
    async def get_failed_notifications(
        self,
        notification_id: Optional[str] = None,
        hours_back: int = 24
    ) -> List[Notification]:
        """
        Get failed notifications for retry.
        
        Args:
            notification_id: Specific notification ID (optional)
            hours_back: How many hours back to look
            
        Returns:
            List of failed notifications
        """
        try:
            if self.db_manager:
                # This would query the database for failed notifications
                # For now, return empty list
                return []
            else:
                # Mock implementation
                return []
                
        except Exception as e:
            logger.error(f"Failed to get failed notifications: {e}")
            return []
    
    async def get_delivery_metrics(
        self,
        start_date: datetime,
        end_date: datetime,
        notification_type: Optional[NotificationType] = None,
        channel: Optional[ChannelType] = None
    ) -> NotificationMetrics:
        """
        Get delivery metrics for a time period.
        
        Args:
            start_date: Start date for metrics
            end_date: End date for metrics
            notification_type: Filter by notification type (optional)
            channel: Filter by channel (optional)
            
        Returns:
            Notification metrics
        """
        try:
            # Calculate metrics from real-time stats
            total_sent = self.real_time_stats['total_sent']
            total_delivered = self.real_time_stats['total_delivered']
            total_failed = self.real_time_stats['total_failed']
            
            delivery_rate = total_delivered / total_sent if total_sent > 0 else 0.0
            
            # Calculate average delivery time (mock)
            average_delivery_time = 2.5  # seconds
            
            # Build channel metrics
            channel_metrics = {}
            for ch, stats in self.real_time_stats['channel_stats'].items():
                if not channel or ch == channel:
                    channel_metrics[ch] = {
                        'sent': stats['sent'],
                        'delivered': stats['delivered'],
                        'failed': stats['failed']
                    }
            
            # Build type metrics
            type_metrics = {}
            for nt, stats in self.real_time_stats['type_stats'].items():
                if not notification_type or nt == notification_type:
                    type_metrics[nt] = {
                        'sent': stats['sent'],
                        'delivered': stats['delivered'],
                        'failed': stats['failed']
                    }
            
            metrics = NotificationMetrics(
                total_sent=total_sent,
                total_delivered=total_delivered,
                total_failed=total_failed,
                delivery_rate=delivery_rate,
                average_delivery_time=average_delivery_time,
                channel_metrics=channel_metrics,
                type_metrics=type_metrics,
                period_start=start_date,
                period_end=end_date
            )
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to get delivery metrics: {e}")
            raise
    
    async def get_real_time_stats(self) -> Dict[str, Any]:
        """
        Get real-time statistics.
        
        Returns:
            Real-time statistics dictionary
        """
        try:
            # Calculate delivery rate
            total_sent = self.real_time_stats['total_sent']
            delivery_rate = (
                self.real_time_stats['total_delivered'] / total_sent
                if total_sent > 0 else 0.0
            )
            
            stats = {
                'total_sent': self.real_time_stats['total_sent'],
                'total_delivered': self.real_time_stats['total_delivered'],
                'total_failed': self.real_time_stats['total_failed'],
                'delivery_rate': delivery_rate,
                'channel_stats': self.real_time_stats['channel_stats'],
                'type_stats': self.real_time_stats['type_stats'],
                'last_updated': self.last_aggregation.isoformat()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get real-time stats: {e}")
            return {}
    
    async def get_hourly_stats(
        self,
        hours: int = 24
    ) -> Dict[str, Dict[str, int]]:
        """
        Get hourly statistics.
        
        Args:
            hours: Number of hours to include
            
        Returns:
            Hourly statistics dictionary
        """
        try:
            current_time = datetime.now()
            hourly_stats = {}
            
            for i in range(hours):
                hour_time = current_time - timedelta(hours=i)
                hour_key = hour_time.strftime('%Y-%m-%d-%H')
                
                if hour_key in self.real_time_stats['hourly_stats']:
                    hourly_stats[hour_key] = self.real_time_stats['hourly_stats'][hour_key]
                else:
                    hourly_stats[hour_key] = {'sent': 0, 'delivered': 0, 'failed': 0}
            
            return hourly_stats
            
        except Exception as e:
            logger.error(f"Failed to get hourly stats: {e}")
            return {}
    
    async def get_top_failing_channels(
        self,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get channels with highest failure rates.
        
        Args:
            limit: Maximum number of channels to return
            
        Returns:
            List of channel failure statistics
        """
        try:
            failing_channels = []
            
            for channel, stats in self.real_time_stats['channel_stats'].items():
                total = stats['sent']
                failed = stats['failed']
                
                if total > 0:
                    failure_rate = failed / total
                    failing_channels.append({
                        'channel': channel,
                        'total_sent': total,
                        'failed': failed,
                        'failure_rate': failure_rate
                    })
            
            # Sort by failure rate descending
            failing_channels.sort(key=lambda x: x['failure_rate'], reverse=True)
            
            return failing_channels[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get top failing channels: {e}")
            return []
    
    async def _load_historical_metrics(self):
        """Load historical metrics from database."""
        try:
            if self.db_manager:
                # This would load historical metrics from database
                # For now, initialize with zeros
                pass
            
            logger.info("Loaded historical metrics")
            
        except Exception as e:
            logger.error(f"Failed to load historical metrics: {e}")
    
    async def _save_delivery_history(self, delivery_results: List[NotificationHistory]):
        """Save delivery history to database."""
        try:
            if self.db_manager:
                # This would save to database
                # For now, just log
                logger.debug(f"Saved {len(delivery_results)} delivery history records")
            else:
                logger.debug(f"Mock saved {len(delivery_results)} delivery history records")
                
        except Exception as e:
            logger.error(f"Failed to save delivery history: {e}")
    
    async def _update_delivery_status(
        self,
        notification_id: str,
        channel: ChannelType,
        status: DeliveryStatus,
        timestamp: datetime,
        error_message: Optional[str] = None
    ):
        """Update delivery status in database."""
        try:
            if self.db_manager:
                # This would update the database
                # For now, just log
                logger.debug(f"Updated delivery status for {notification_id} via {channel}: {status}")
            else:
                logger.debug(f"Mock updated delivery status for {notification_id} via {channel}: {status}")
                
        except Exception as e:
            logger.error(f"Failed to update delivery status: {e}")
    
    async def reset_stats(self):
        """Reset all statistics."""
        try:
            self.real_time_stats = {
                'total_sent': 0,
                'total_delivered': 0,
                'total_failed': 0,
                'channel_stats': {},
                'type_stats': {},
                'hourly_stats': {}
            }
            
            self.last_aggregation = datetime.now()
            
            logger.info("Reset all analytics statistics")
            
        except Exception as e:
            logger.error(f"Failed to reset stats: {e}")
    
    async def cleanup(self):
        """Cleanup resources."""
        try:
            self.metrics_cache.clear()
            self.real_time_stats.clear()
            logger.info("Analytics tracker cleanup completed")
        except Exception as e:
            logger.error(f"Error during analytics tracker cleanup: {e}")
