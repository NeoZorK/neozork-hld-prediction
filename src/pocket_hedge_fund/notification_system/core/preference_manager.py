"""
Preference Manager

Manages user notification preferences and settings.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import json

from ..models.notification_models import (
    NotificationPreference, NotificationType, ChannelType,
    NotificationPriority
)

logger = logging.getLogger(__name__)


class PreferenceManager:
    """
    Manages user notification preferences and settings.
    """
    
    def __init__(self, db_manager=None):
        """Initialize preference manager."""
        self.db_manager = db_manager
        self.preference_cache = {}
        self.default_preferences = self._setup_default_preferences()
        self.cache_ttl = 300  # 5 minutes
        self.cache_timestamps = {}
    
    def _setup_default_preferences(self) -> Dict[NotificationType, NotificationPreference]:
        """Setup default notification preferences."""
        default_prefs = {}
        
        for notification_type in NotificationType:
            default_prefs[notification_type] = NotificationPreference(
                user_id="default",
                notification_type=notification_type,
                channels=[ChannelType.EMAIL],  # Default to email only
                is_enabled=True,
                priority_threshold=NotificationPriority.LOW,
                timezone="UTC"
            )
        
        # Override specific types with more appropriate defaults
        default_prefs[NotificationType.TRADING_ALERT] = NotificationPreference(
            user_id="default",
            notification_type=NotificationType.TRADING_ALERT,
            channels=[ChannelType.EMAIL, ChannelType.PUSH],
            is_enabled=True,
            priority_threshold=NotificationPriority.NORMAL,
            frequency_limit=10,  # Max 10 per hour
            timezone="UTC"
        )
        
        default_prefs[NotificationType.RISK_WARNING] = NotificationPreference(
            user_id="default",
            notification_type=NotificationType.RISK_WARNING,
            channels=[ChannelType.EMAIL, ChannelType.SMS, ChannelType.PUSH],
            is_enabled=True,
            priority_threshold=NotificationPriority.HIGH,
            frequency_limit=5,  # Max 5 per hour
            timezone="UTC"
        )
        
        default_prefs[NotificationType.SECURITY_ALERT] = NotificationPreference(
            user_id="default",
            notification_type=NotificationType.SECURITY_ALERT,
            channels=[ChannelType.EMAIL, ChannelType.SMS, ChannelType.PUSH],
            is_enabled=True,
            priority_threshold=NotificationPriority.CRITICAL,
            frequency_limit=20,  # Max 20 per hour
            timezone="UTC"
        )
        
        return default_prefs
    
    async def initialize(self):
        """Initialize preference manager."""
        try:
            # Load user preferences from database
            await self._load_user_preferences()
            
            logger.info("Preference manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize preference manager: {e}")
            raise
    
    async def _load_user_preferences(self):
        """Load user preferences from database."""
        try:
            if self.db_manager:
                # This would query the database for user preferences
                # For now, we'll use mock data
                pass
            
            logger.info("Loaded user preferences from database")
        except Exception as e:
            logger.error(f"Failed to load user preferences: {e}")
            raise
    
    async def get_user_preferences(
        self,
        user_id: str,
        notification_type: Optional[NotificationType] = None
    ) -> Optional[NotificationPreference]:
        """
        Get user preferences for a specific notification type.
        
        Args:
            user_id: User identifier
            notification_type: Specific notification type (optional)
            
        Returns:
            User preferences or None if not found
        """
        try:
            cache_key = f"{user_id}:{notification_type}" if notification_type else f"{user_id}:all"
            
            # Check cache first
            if await self._is_cache_valid(cache_key):
                return self.preference_cache.get(cache_key)
            
            # Load from database
            preference = await self._load_user_preference(user_id, notification_type)
            
            # Cache the result
            if preference:
                self.preference_cache[cache_key] = preference
                self.cache_timestamps[cache_key] = datetime.now()
            
            return preference
            
        except Exception as e:
            logger.error(f"Failed to get user preferences: {e}")
            return None
    
    async def get_all_user_preferences(
        self,
        user_id: str
    ) -> Dict[NotificationType, NotificationPreference]:
        """
        Get all user preferences.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary of notification type to preferences
        """
        try:
            preferences = {}
            
            for notification_type in NotificationType:
                preference = await self.get_user_preferences(user_id, notification_type)
                if preference:
                    preferences[notification_type] = preference
                else:
                    # Use default preference
                    default_pref = self.default_preferences[notification_type]
                    default_pref.user_id = user_id
                    preferences[notification_type] = default_pref
            
            return preferences
            
        except Exception as e:
            logger.error(f"Failed to get all user preferences: {e}")
            return {}
    
    async def set_user_preference(
        self,
        preference: NotificationPreference
    ) -> bool:
        """
        Set user preference.
        
        Args:
            preference: Preference to set
            
        Returns:
            True if successful
        """
        try:
            # Validate preference
            if not await self._validate_preference(preference):
                return False
            
            # Save to database
            success = await self._save_user_preference(preference)
            
            if success:
                # Update cache
                cache_key = f"{preference.user_id}:{preference.notification_type}"
                self.preference_cache[cache_key] = preference
                self.cache_timestamps[cache_key] = datetime.now()
                
                logger.info(f"Updated preference for user {preference.user_id}, type {preference.notification_type}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to set user preference: {e}")
            return False
    
    async def update_user_preference(
        self,
        user_id: str,
        notification_type: NotificationType,
        updates: Dict[str, Any]
    ) -> bool:
        """
        Update specific fields of user preference.
        
        Args:
            user_id: User identifier
            notification_type: Notification type
            updates: Fields to update
            
        Returns:
            True if successful
        """
        try:
            # Get existing preference
            preference = await self.get_user_preferences(user_id, notification_type)
            
            if not preference:
                # Create new preference with defaults
                preference = self.default_preferences[notification_type]
                preference.user_id = user_id
                preference.notification_type = notification_type
            
            # Update fields
            for field, value in updates.items():
                if hasattr(preference, field):
                    setattr(preference, field, value)
            
            # Save updated preference
            return await self.set_user_preference(preference)
            
        except Exception as e:
            logger.error(f"Failed to update user preference: {e}")
            return False
    
    async def delete_user_preference(
        self,
        user_id: str,
        notification_type: NotificationType
    ) -> bool:
        """
        Delete user preference.
        
        Args:
            user_id: User identifier
            notification_type: Notification type
            
        Returns:
            True if successful
        """
        try:
            # Delete from database
            success = await self._delete_user_preference(user_id, notification_type)
            
            if success:
                # Remove from cache
                cache_key = f"{user_id}:{notification_type}"
                self.preference_cache.pop(cache_key, None)
                self.cache_timestamps.pop(cache_key, None)
                
                logger.info(f"Deleted preference for user {user_id}, type {notification_type}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to delete user preference: {e}")
            return False
    
    async def reset_user_preferences(
        self,
        user_id: str
    ) -> bool:
        """
        Reset user preferences to defaults.
        
        Args:
            user_id: User identifier
            
        Returns:
            True if successful
        """
        try:
            # Delete all existing preferences
            for notification_type in NotificationType:
                await self.delete_user_preference(user_id, notification_type)
            
            # Clear cache
            keys_to_remove = [key for key in self.preference_cache.keys() if key.startswith(f"{user_id}:")]
            for key in keys_to_remove:
                self.preference_cache.pop(key, None)
                self.cache_timestamps.pop(key, None)
            
            logger.info(f"Reset preferences for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to reset user preferences: {e}")
            return False
    
    async def get_preference_statistics(
        self,
        notification_type: Optional[NotificationType] = None
    ) -> Dict[str, Any]:
        """
        Get preference statistics.
        
        Args:
            notification_type: Specific notification type (optional)
            
        Returns:
            Statistics dictionary
        """
        try:
            stats = {
                'total_users': 0,
                'enabled_preferences': 0,
                'disabled_preferences': 0,
                'channel_usage': {},
                'priority_distribution': {}
            }
            
            # This would query the database for actual statistics
            # For now, return mock data
            stats['total_users'] = 100
            stats['enabled_preferences'] = 85
            stats['disabled_preferences'] = 15
            stats['channel_usage'] = {
                'email': 90,
                'push': 60,
                'sms': 30,
                'webhook': 10
            }
            stats['priority_distribution'] = {
                'low': 20,
                'normal': 50,
                'high': 25,
                'urgent': 4,
                'critical': 1
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get preference statistics: {e}")
            return {}
    
    async def _load_user_preference(
        self,
        user_id: str,
        notification_type: Optional[NotificationType]
    ) -> Optional[NotificationPreference]:
        """Load user preference from database."""
        try:
            if self.db_manager:
                # This would query the database
                # For now, return None to use defaults
                return None
            else:
                # Mock implementation
                return None
                
        except Exception as e:
            logger.error(f"Failed to load user preference: {e}")
            return None
    
    async def _save_user_preference(
        self,
        preference: NotificationPreference
    ) -> bool:
        """Save user preference to database."""
        try:
            if self.db_manager:
                # This would save to database
                # For now, return True
                return True
            else:
                # Mock implementation
                return True
                
        except Exception as e:
            logger.error(f"Failed to save user preference: {e}")
            return False
    
    async def _delete_user_preference(
        self,
        user_id: str,
        notification_type: NotificationType
    ) -> bool:
        """Delete user preference from database."""
        try:
            if self.db_manager:
                # This would delete from database
                # For now, return True
                return True
            else:
                # Mock implementation
                return True
                
        except Exception as e:
            logger.error(f"Failed to delete user preference: {e}")
            return False
    
    async def _validate_preference(self, preference: NotificationPreference) -> bool:
        """Validate preference data."""
        try:
            # Check required fields
            if not preference.user_id:
                logger.error("Preference missing user_id")
                return False
            
            if not preference.notification_type:
                logger.error("Preference missing notification_type")
                return False
            
            # Check channels
            if not preference.channels:
                logger.error("Preference must have at least one channel")
                return False
            
            # Check quiet hours format
            if preference.quiet_hours_start and preference.quiet_hours_end:
                try:
                    datetime.strptime(preference.quiet_hours_start, '%H:%M')
                    datetime.strptime(preference.quiet_hours_end, '%H:%M')
                except ValueError:
                    logger.error("Invalid quiet hours format")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating preference: {e}")
            return False
    
    async def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cache entry is still valid."""
        try:
            if cache_key not in self.cache_timestamps:
                return False
            
            timestamp = self.cache_timestamps[cache_key]
            return datetime.now() - timestamp < timedelta(seconds=self.cache_ttl)
            
        except Exception as e:
            logger.error(f"Error checking cache validity: {e}")
            return False
    
    async def clear_cache(self, user_id: Optional[str] = None):
        """Clear preference cache."""
        try:
            if user_id:
                # Clear cache for specific user
                keys_to_remove = [key for key in self.preference_cache.keys() if key.startswith(f"{user_id}:")]
                for key in keys_to_remove:
                    self.preference_cache.pop(key, None)
                    self.cache_timestamps.pop(key, None)
            else:
                # Clear all cache
                self.preference_cache.clear()
                self.cache_timestamps.clear()
            
            logger.info(f"Cleared preference cache for user: {user_id or 'all'}")
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
    
    async def cleanup(self):
        """Cleanup resources."""
        try:
            self.preference_cache.clear()
            self.cache_timestamps.clear()
            logger.info("Preference manager cleanup completed")
        except Exception as e:
            logger.error(f"Error during preference manager cleanup: {e}")
