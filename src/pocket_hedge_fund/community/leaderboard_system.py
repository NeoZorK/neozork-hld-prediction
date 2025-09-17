"""Leaderboard System - Performance rankings and competitions"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class LeaderboardType(Enum):
    """Leaderboard type enumeration."""
    PERFORMANCE = "performance"
    PROFIT = "profit"
    SHARPE_RATIO = "sharpe_ratio"
    WIN_RATE = "win_rate"
    FOLLOWERS = "followers"
    STRATEGIES = "strategies"


class CompetitionStatus(Enum):
    """Competition status enumeration."""
    UPCOMING = "upcoming"
    ACTIVE = "active"
    ENDED = "ended"
    CANCELLED = "cancelled"


class LeaderboardSystem:
    """Performance rankings and competitions system."""
    
    def __init__(self):
        self.leaderboards: Dict[str, Dict[str, Any]] = {}
        self.competitions: Dict[str, Dict[str, Any]] = {}
        self.user_rankings: Dict[str, Dict[str, Any]] = {}
        self.ranking_history: Dict[str, List[Dict[str, Any]]] = {}
        
    async def create_leaderboard(self, name: str, leaderboard_type: LeaderboardType,
                               period_days: int = 30, max_entries: int = 100) -> Dict[str, Any]:
        """Create a new leaderboard."""
        try:
            leaderboard_id = str(uuid.uuid4())
            
            leaderboard = {
                'leaderboard_id': leaderboard_id,
                'name': name,
                'type': leaderboard_type.value,
                'period_days': period_days,
                'max_entries': max_entries,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'entries': []
            }
            
            self.leaderboards[leaderboard_id] = leaderboard
            
            logger.info(f"Created leaderboard: {name} ({leaderboard_id})")
            return {
                'status': 'success',
                'leaderboard_id': leaderboard_id,
                'leaderboard': leaderboard
            }
            
        except Exception as e:
            logger.error(f"Failed to create leaderboard: {e}")
            return {'error': str(e)}
    
    async def update_leaderboard(self, leaderboard_id: str, 
                               user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update leaderboard with user performance data."""
        try:
            if leaderboard_id not in self.leaderboards:
                return {'error': 'Leaderboard not found'}
            
            leaderboard = self.leaderboards[leaderboard_id]
            
            # Calculate ranking score based on type
            score = await self._calculate_ranking_score(leaderboard['type'], user_data)
            
            # Add or update entry
            entry = {
                'user_id': user_data['user_id'],
                'username': user_data.get('username', ''),
                'score': score,
                'metadata': user_data,
                'updated_at': datetime.now()
            }
            
            # Update entries
            existing_entry = None
            for i, existing in enumerate(leaderboard['entries']):
                if existing['user_id'] == user_data['user_id']:
                    existing_entry = i
                    break
            
            if existing_entry is not None:
                leaderboard['entries'][existing_entry] = entry
            else:
                leaderboard['entries'].append(entry)
            
            # Sort by score (descending)
            leaderboard['entries'].sort(key=lambda x: x['score'], reverse=True)
            
            # Limit entries
            if len(leaderboard['entries']) > leaderboard['max_entries']:
                leaderboard['entries'] = leaderboard['entries'][:leaderboard['max_entries']]
            
            leaderboard['updated_at'] = datetime.now()
            
            logger.info(f"Updated leaderboard {leaderboard_id} with {len(leaderboard['entries'])} entries")
            return {
                'status': 'success',
                'leaderboard_id': leaderboard_id,
                'total_entries': len(leaderboard['entries'])
            }
            
        except Exception as e:
            logger.error(f"Failed to update leaderboard: {e}")
            return {'error': str(e)}
    
    async def get_leaderboard(self, leaderboard_id: str, 
                            limit: int = 50) -> Dict[str, Any]:
        """Get leaderboard entries."""
        try:
            if leaderboard_id not in self.leaderboards:
                return {'error': 'Leaderboard not found'}
            
            leaderboard = self.leaderboards[leaderboard_id]
            
            # Get top entries
            top_entries = leaderboard['entries'][:limit]
            
            # Add ranking positions
            for i, entry in enumerate(top_entries):
                entry['rank'] = i + 1
            
            return {
                'leaderboard_id': leaderboard_id,
                'name': leaderboard['name'],
                'type': leaderboard['type'],
                'period_days': leaderboard['period_days'],
                'total_entries': len(leaderboard['entries']),
                'entries': top_entries,
                'last_updated': leaderboard['updated_at']
            }
            
        except Exception as e:
            logger.error(f"Failed to get leaderboard: {e}")
            return {'error': str(e)}
    
    async def get_user_ranking(self, user_id: str, leaderboard_id: str) -> Dict[str, Any]:
        """Get user's ranking in a specific leaderboard."""
        try:
            if leaderboard_id not in self.leaderboards:
                return {'error': 'Leaderboard not found'}
            
            leaderboard = self.leaderboards[leaderboard_id]
            
            # Find user's position
            user_rank = None
            user_entry = None
            
            for i, entry in enumerate(leaderboard['entries']):
                if entry['user_id'] == user_id:
                    user_rank = i + 1
                    user_entry = entry
                    break
            
            if user_rank is None:
                return {
                    'user_id': user_id,
                    'leaderboard_id': leaderboard_id,
                    'rank': None,
                    'message': 'User not found in leaderboard'
                }
            
            return {
                'user_id': user_id,
                'leaderboard_id': leaderboard_id,
                'rank': user_rank,
                'score': user_entry['score'],
                'total_entries': len(leaderboard['entries']),
                'percentile': (len(leaderboard['entries']) - user_rank + 1) / len(leaderboard['entries']) * 100
            }
            
        except Exception as e:
            logger.error(f"Failed to get user ranking: {e}")
            return {'error': str(e)}
    
    async def create_competition(self, name: str, description: str,
                               start_date: datetime, end_date: datetime,
                               prize_pool: float = 0.0,
                               entry_fee: float = 0.0) -> Dict[str, Any]:
        """Create a trading competition."""
        try:
            competition_id = str(uuid.uuid4())
            
            competition = {
                'competition_id': competition_id,
                'name': name,
                'description': description,
                'start_date': start_date,
                'end_date': end_date,
                'prize_pool': prize_pool,
                'entry_fee': entry_fee,
                'status': CompetitionStatus.UPCOMING.value,
                'participants': [],
                'leaderboard_id': None,  # Will be created when competition starts
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            self.competitions[competition_id] = competition
            
            logger.info(f"Created competition: {name} ({competition_id})")
            return {
                'status': 'success',
                'competition_id': competition_id,
                'competition': competition
            }
            
        except Exception as e:
            logger.error(f"Failed to create competition: {e}")
            return {'error': str(e)}
    
    async def join_competition(self, competition_id: str, user_id: str) -> Dict[str, Any]:
        """Join a competition."""
        try:
            if competition_id not in self.competitions:
                return {'error': 'Competition not found'}
            
            competition = self.competitions[competition_id]
            
            # Check if competition is open for registration
            if competition['status'] != CompetitionStatus.UPCOMING.value:
                return {'error': 'Competition is not open for registration'}
            
            # Check if user is already participating
            if any(p['user_id'] == user_id for p in competition['participants']):
                return {'error': 'Already participating in this competition'}
            
            # Add participant
            participant = {
                'user_id': user_id,
                'joined_at': datetime.now(),
                'entry_fee_paid': competition['entry_fee'] > 0,
                'starting_balance': 10000.0,  # Default starting balance
                'current_balance': 10000.0,
                'total_return': 0.0
            }
            
            competition['participants'].append(participant)
            competition['updated_at'] = datetime.now()
            
            logger.info(f"User {user_id} joined competition {competition_id}")
            return {
                'status': 'success',
                'competition_id': competition_id,
                'user_id': user_id,
                'participant': participant
            }
            
        except Exception as e:
            logger.error(f"Failed to join competition: {e}")
            return {'error': str(e)}
    
    async def _calculate_ranking_score(self, leaderboard_type: str, 
                                     user_data: Dict[str, Any]) -> float:
        """Calculate ranking score based on leaderboard type."""
        if leaderboard_type == LeaderboardType.PERFORMANCE.value:
            return user_data.get('total_return', 0.0)
        elif leaderboard_type == LeaderboardType.PROFIT.value:
            return user_data.get('total_profit', 0.0)
        elif leaderboard_type == LeaderboardType.SHARPE_RATIO.value:
            return user_data.get('sharpe_ratio', 0.0)
        elif leaderboard_type == LeaderboardType.WIN_RATE.value:
            return user_data.get('win_rate', 0.0)
        elif leaderboard_type == LeaderboardType.FOLLOWERS.value:
            return user_data.get('follower_count', 0.0)
        elif leaderboard_type == LeaderboardType.STRATEGIES.value:
            return user_data.get('strategy_count', 0.0)
        else:
            return 0.0
    
    def get_leaderboard_summary(self) -> Dict[str, Any]:
        """Get leaderboard system summary."""
        total_leaderboards = len(self.leaderboards)
        total_competitions = len(self.competitions)
        active_competitions = len([c for c in self.competitions.values() 
                                 if c['status'] == CompetitionStatus.ACTIVE.value])
        
        return {
            'total_leaderboards': total_leaderboards,
            'total_competitions': total_competitions,
            'active_competitions': active_competitions,
            'total_participants': sum(len(c['participants']) for c in self.competitions.values())
        }