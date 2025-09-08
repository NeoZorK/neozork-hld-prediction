"""Communication System - Investor communication and notifications"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Message type enumeration."""
    PERFORMANCE_UPDATE = "performance_update"
    RISK_ALERT = "risk_alert"
    MARKET_UPDATE = "market_update"
    FUND_ANNOUNCEMENT = "fund_announcement"
    SYSTEM_NOTIFICATION = "system_notification"


class DeliveryMethod(Enum):
    """Delivery method enumeration."""
    EMAIL = "email"
    SMS = "sms"
    PUSH_NOTIFICATION = "push_notification"
    IN_APP = "in_app"


@dataclass
class Message:
    """Message data class."""
    message_id: str
    investor_id: str
    message_type: MessageType
    subject: str
    content: str
    delivery_methods: List[DeliveryMethod]
    priority: int
    created_at: datetime
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None


class CommunicationSystem:
    """Investor communication and notification system."""
    
    def __init__(self):
        self.messages: Dict[str, List[Message]] = {}
        self.notification_preferences: Dict[str, Dict[str, Any]] = {}
        self.message_templates: Dict[str, str] = {}
        
        # Initialize default templates
        self._initialize_templates()
        
    async def send_message(self, investor_id: str, message_type: MessageType,
                          subject: str, content: str, 
                          delivery_methods: List[DeliveryMethod] = None,
                          priority: int = 1) -> Dict[str, Any]:
        """Send a message to an investor."""
        try:
            if delivery_methods is None:
                delivery_methods = [DeliveryMethod.IN_APP]
            
            message = Message(
                message_id=f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{investor_id}",
                investor_id=investor_id,
                message_type=message_type,
                subject=subject,
                content=content,
                delivery_methods=delivery_methods,
                priority=priority,
                created_at=datetime.now()
            )
            
            # Store message
            if investor_id not in self.messages:
                self.messages[investor_id] = []
            self.messages[investor_id].append(message)
            
            # Send via specified methods
            delivery_results = []
            for method in delivery_methods:
                result = await self._deliver_message(message, method)
                delivery_results.append(result)
            
            message.sent_at = datetime.now()
            
            logger.info(f"Sent message to investor {investor_id} via {len(delivery_methods)} methods")
            return {
                'status': 'success',
                'message_id': message.message_id,
                'delivery_results': delivery_results,
                'sent_at': message.sent_at
            }
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return {'error': str(e)}
    
    async def send_performance_update(self, investor_id: str, 
                                    performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send performance update to investor."""
        try:
            # Generate performance update content
            subject = f"Performance Update - {performance_data.get('period', 'Monthly')}"
            content = self._generate_performance_content(performance_data)
            
            # Get investor preferences
            preferences = self.notification_preferences.get(investor_id, {})
            delivery_methods = preferences.get('performance_updates', [DeliveryMethod.IN_APP])
            
            return await self.send_message(
                investor_id=investor_id,
                message_type=MessageType.PERFORMANCE_UPDATE,
                subject=subject,
                content=content,
                delivery_methods=delivery_methods,
                priority=2
            )
            
        except Exception as e:
            logger.error(f"Failed to send performance update: {e}")
            return {'error': str(e)}
    
    async def send_risk_alert(self, investor_id: str, 
                            risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send risk alert to investor."""
        try:
            # Generate risk alert content
            subject = f"Risk Alert - {risk_data.get('risk_type', 'Portfolio Risk')}"
            content = self._generate_risk_alert_content(risk_data)
            
            # Get investor preferences
            preferences = self.notification_preferences.get(investor_id, {})
            delivery_methods = preferences.get('risk_alerts', [DeliveryMethod.EMAIL, DeliveryMethod.IN_APP])
            
            return await self.send_message(
                investor_id=investor_id,
                message_type=MessageType.RISK_ALERT,
                subject=subject,
                content=content,
                delivery_methods=delivery_methods,
                priority=3  # High priority for risk alerts
            )
            
        except Exception as e:
            logger.error(f"Failed to send risk alert: {e}")
            return {'error': str(e)}
    
    async def get_investor_messages(self, investor_id: str, 
                                  message_type: Optional[MessageType] = None,
                                  unread_only: bool = False) -> Dict[str, Any]:
        """Get messages for a specific investor."""
        try:
            if investor_id not in self.messages:
                return {'messages': [], 'total_count': 0}
            
            messages = self.messages[investor_id]
            
            # Filter by message type
            if message_type:
                messages = [msg for msg in messages if msg.message_type == message_type]
            
            # Filter by read status
            if unread_only:
                messages = [msg for msg in messages if msg.read_at is None]
            
            # Sort by creation time (newest first)
            messages.sort(key=lambda x: x.created_at, reverse=True)
            
            return {
                'investor_id': investor_id,
                'messages': [msg.__dict__ for msg in messages],
                'total_count': len(messages),
                'unread_count': len([m for m in self.messages[investor_id] if m.read_at is None])
            }
            
        except Exception as e:
            logger.error(f"Failed to get investor messages: {e}")
            return {'error': str(e)}
    
    async def mark_message_read(self, investor_id: str, message_id: str) -> Dict[str, Any]:
        """Mark a message as read."""
        try:
            if investor_id not in self.messages:
                return {'error': 'Investor not found'}
            
            for message in self.messages[investor_id]:
                if message.message_id == message_id:
                    message.read_at = datetime.now()
                    logger.info(f"Marked message {message_id} as read for investor {investor_id}")
                    return {'status': 'success', 'message_id': message_id}
            
            return {'error': 'Message not found'}
            
        except Exception as e:
            logger.error(f"Failed to mark message as read: {e}")
            return {'error': str(e)}
    
    async def set_notification_preferences(self, investor_id: str, 
                                         preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Set notification preferences for an investor."""
        try:
            self.notification_preferences[investor_id] = preferences
            logger.info(f"Updated notification preferences for investor {investor_id}")
            return {'status': 'success', 'preferences': preferences}
            
        except Exception as e:
            logger.error(f"Failed to set notification preferences: {e}")
            return {'error': str(e)}
    
    async def _deliver_message(self, message: Message, method: DeliveryMethod) -> Dict[str, Any]:
        """Deliver message via specified method."""
        try:
            if method == DeliveryMethod.EMAIL:
                # TODO: Implement email delivery
                return {'method': 'email', 'status': 'sent', 'delivery_time': datetime.now()}
            elif method == DeliveryMethod.SMS:
                # TODO: Implement SMS delivery
                return {'method': 'sms', 'status': 'sent', 'delivery_time': datetime.now()}
            elif method == DeliveryMethod.PUSH_NOTIFICATION:
                # TODO: Implement push notification delivery
                return {'method': 'push', 'status': 'sent', 'delivery_time': datetime.now()}
            elif method == DeliveryMethod.IN_APP:
                # In-app messages are already stored
                return {'method': 'in_app', 'status': 'delivered', 'delivery_time': datetime.now()}
            else:
                return {'method': method.value, 'status': 'failed', 'error': 'Unknown delivery method'}
                
        except Exception as e:
            logger.error(f"Failed to deliver message via {method.value}: {e}")
            return {'method': method.value, 'status': 'failed', 'error': str(e)}
    
    def _generate_performance_content(self, performance_data: Dict[str, Any]) -> str:
        """Generate performance update content."""
        # TODO: Implement dynamic content generation
        return f"""
        Performance Update
        
        Total Return: {performance_data.get('total_return', 0):.2%}
        Daily Return: {performance_data.get('daily_return', 0):.2%}
        Sharpe Ratio: {performance_data.get('sharpe_ratio', 0):.2f}
        Max Drawdown: {performance_data.get('max_drawdown', 0):.2%}
        
        For more details, please log into your investor portal.
        """
    
    def _generate_risk_alert_content(self, risk_data: Dict[str, Any]) -> str:
        """Generate risk alert content."""
        # TODO: Implement dynamic content generation
        return f"""
        Risk Alert
        
        Risk Type: {risk_data.get('risk_type', 'Portfolio Risk')}
        Current Level: {risk_data.get('current_level', 'Unknown')}
        Threshold: {risk_data.get('threshold', 'Unknown')}
        
        Please review your portfolio and consider taking appropriate action.
        """
    
    def _initialize_templates(self):
        """Initialize message templates."""
        self.message_templates = {
            'performance_update': 'performance_update_template.html',
            'risk_alert': 'risk_alert_template.html',
            'market_update': 'market_update_template.html',
            'fund_announcement': 'fund_announcement_template.html',
            'system_notification': 'system_notification_template.html'
        }