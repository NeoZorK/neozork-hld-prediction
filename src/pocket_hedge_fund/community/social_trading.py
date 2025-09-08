"""Social Trading - Social trading and copy trading functionality"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class FollowStatus(Enum):
    """Follow status enumeration."""
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"


class CopyMode(Enum):
    """Copy mode enumeration."""
    FULL_COPY = "full_copy"
    PROPORTIONAL_COPY = "proportional_copy"
    SIGNAL_ONLY = "signal_only"


class SocialTrading:
    """Social trading and copy trading system."""
    
    def __init__(self):
        self.follow_relationships: Dict[str, Dict[str, Any]] = {}
        self.trade_signals: Dict[str, List[Dict[str, Any]]] = {}
        self.leader_metrics: Dict[str, Dict[str, Any]] = {}
        self.follower_metrics: Dict[str, Dict[str, Any]] = {}
        
    async def follow_trader(self, follower_id: str, leader_id: str,
                          copy_mode: CopyMode = CopyMode.PROPORTIONAL_COPY,
                          copy_percentage: float = 1.0,
                          max_copy_amount: float = 10000.0) -> Dict[str, Any]:
        """Follow a trader for copy trading."""
        try:
            # Validate parameters
            if copy_percentage <= 0 or copy_percentage > 1:
                return {'error': 'Copy percentage must be between 0 and 1'}
            
            if max_copy_amount <= 0:
                return {'error': 'Max copy amount must be positive'}
            
            # Create follow relationship
            follow_id = str(uuid.uuid4())
            follow_relationship = {
                'follow_id': follow_id,
                'follower_id': follower_id,
                'leader_id': leader_id,
                'status': FollowStatus.ACTIVE.value,
                'copy_mode': copy_mode.value,
                'copy_percentage': copy_percentage,
                'max_copy_amount': max_copy_amount,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            self.follow_relationships[follow_id] = follow_relationship
            
            # Initialize metrics
            if leader_id not in self.leader_metrics:
                self.leader_metrics[leader_id] = {
                    'total_followers': 0,
                    'total_copied_trades': 0,
                    'total_copied_volume': 0.0
                }
            
            if follower_id not in self.follower_metrics:
                self.follower_metrics[follower_id] = {
                    'total_following': 0,
                    'total_copied_trades': 0,
                    'total_copied_volume': 0.0
                }
            
            # Update metrics
            self.leader_metrics[leader_id]['total_followers'] += 1
            self.follower_metrics[follower_id]['total_following'] += 1
            
            logger.info(f"User {follower_id} started following {leader_id}")
            return {
                'status': 'success',
                'follow_id': follow_id,
                'follow_relationship': follow_relationship
            }
            
        except Exception as e:
            logger.error(f"Failed to follow trader: {e}")
            return {'error': str(e)}
    
    async def publish_trade_signal(self, leader_id: str, strategy_id: str,
                                 signal_type: str, asset: str,
                                 quantity: float, price: float,
                                 confidence: float = 1.0) -> Dict[str, Any]:
        """Publish a trade signal to followers."""
        try:
            # Create trade signal
            signal_id = str(uuid.uuid4())
            trade_signal = {
                'signal_id': signal_id,
                'leader_id': leader_id,
                'strategy_id': strategy_id,
                'signal_type': signal_type,
                'asset': asset,
                'quantity': quantity,
                'price': price,
                'timestamp': datetime.now(),
                'confidence': confidence
            }
            
            # Store signal
            if leader_id not in self.trade_signals:
                self.trade_signals[leader_id] = []
            self.trade_signals[leader_id].append(trade_signal)
            
            logger.info(f"Published trade signal {signal_id} by {leader_id}")
            return {
                'status': 'success',
                'signal_id': signal_id,
                'trade_signal': trade_signal
            }
            
        except Exception as e:
            logger.error(f"Failed to publish trade signal: {e}")
            return {'error': str(e)}
    
    async def get_followers(self, leader_id: str) -> Dict[str, Any]:
        """Get list of followers for a leader."""
        try:
            followers = []
            
            for follow in self.follow_relationships.values():
                if (follow['leader_id'] == leader_id and 
                    follow['status'] == FollowStatus.ACTIVE.value):
                    followers.append({
                        'follower_id': follow['follower_id'],
                        'follow_id': follow['follow_id'],
                        'copy_mode': follow['copy_mode'],
                        'copy_percentage': follow['copy_percentage'],
                        'max_copy_amount': follow['max_copy_amount'],
                        'followed_at': follow['created_at']
                    })
            
            return {
                'leader_id': leader_id,
                'followers': followers,
                'total_followers': len(followers)
            }
            
        except Exception as e:
            logger.error(f"Failed to get followers: {e}")
            return {'error': str(e)}
    
    def get_social_trading_summary(self) -> Dict[str, Any]:
        """Get social trading system summary."""
        total_follows = len(self.follow_relationships)
        active_follows = len([f for f in self.follow_relationships.values() if f['status'] == FollowStatus.ACTIVE.value])
        total_signals = sum(len(signals) for signals in self.trade_signals.values())
        
        return {
            'total_follow_relationships': total_follows,
            'active_follow_relationships': active_follows,
            'total_trade_signals': total_signals,
            'unique_leaders': len(self.trade_signals)
        }