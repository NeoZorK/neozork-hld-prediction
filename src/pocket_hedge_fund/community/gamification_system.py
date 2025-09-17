"""Gamification System - User engagement and rewards"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class AchievementType(Enum):
    """Achievement type enumeration."""
    TRADING = "trading"
    SOCIAL = "social"
    LEARNING = "learning"
    COMMUNITY = "community"
    PERFORMANCE = "performance"


class BadgeType(Enum):
    """Badge type enumeration."""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"


class GamificationSystem:
    """User engagement and rewards system."""
    
    def __init__(self):
        self.achievements: Dict[str, Dict[str, Any]] = {}
        self.user_achievements: Dict[str, List[Dict[str, Any]]] = {}
        self.badges: Dict[str, Dict[str, Any]] = {}
        self.user_badges: Dict[str, List[Dict[str, Any]]] = {}
        self.user_points: Dict[str, int] = {}
        self.user_levels: Dict[str, Dict[str, Any]] = {}
        self.quests: Dict[str, Dict[str, Any]] = {}
        self.user_quests: Dict[str, List[Dict[str, Any]]] = {}
        
        # Initialize default achievements and badges
        self._initialize_default_content()
        
    async def award_achievement(self, user_id: str, achievement_id: str) -> Dict[str, Any]:
        """Award an achievement to a user."""
        try:
            if achievement_id not in self.achievements:
                return {'error': 'Achievement not found'}
            
            achievement = self.achievements[achievement_id]
            
            # Check if user already has this achievement
            if user_id in self.user_achievements:
                existing_achievements = [a['achievement_id'] for a in self.user_achievements[user_id]]
                if achievement_id in existing_achievements:
                    return {'error': 'User already has this achievement'}
            
            # Award achievement
            user_achievement = {
                'achievement_id': achievement_id,
                'user_id': user_id,
                'awarded_at': datetime.now(),
                'points_earned': achievement['points']
            }
            
            if user_id not in self.user_achievements:
                self.user_achievements[user_id] = []
            self.user_achievements[user_id].append(user_achievement)
            
            # Update user points
            if user_id not in self.user_points:
                self.user_points[user_id] = 0
            self.user_points[user_id] += achievement['points']
            
            # Check for level up
            level_up_result = await self._check_level_up(user_id)
            
            logger.info(f"Awarded achievement {achievement_id} to user {user_id}")
            return {
                'status': 'success',
                'achievement': achievement,
                'user_achievement': user_achievement,
                'level_up': level_up_result
            }
            
        except Exception as e:
            logger.error(f"Failed to award achievement: {e}")
            return {'error': str(e)}
    
    async def award_badge(self, user_id: str, badge_id: str) -> Dict[str, Any]:
        """Award a badge to a user."""
        try:
            if badge_id not in self.badges:
                return {'error': 'Badge not found'}
            
            badge = self.badges[badge_id]
            
            # Check if user already has this badge
            if user_id in self.user_badges:
                existing_badges = [b['badge_id'] for b in self.user_badges[user_id]]
                if badge_id in existing_badges:
                    return {'error': 'User already has this badge'}
            
            # Award badge
            user_badge = {
                'badge_id': badge_id,
                'user_id': user_id,
                'awarded_at': datetime.now(),
                'points_earned': badge['points']
            }
            
            if user_id not in self.user_badges:
                self.user_badges[user_id] = []
            self.user_badges[user_id].append(user_badge)
            
            # Update user points
            if user_id not in self.user_points:
                self.user_points[user_id] = 0
            self.user_points[user_id] += badge['points']
            
            logger.info(f"Awarded badge {badge_id} to user {user_id}")
            return {
                'status': 'success',
                'badge': badge,
                'user_badge': user_badge
            }
            
        except Exception as e:
            logger.error(f"Failed to award badge: {e}")
            return {'error': str(e)}
    
    async def create_quest(self, name: str, description: str, 
                          quest_type: str, requirements: Dict[str, Any],
                          rewards: Dict[str, Any], duration_days: int = 7) -> Dict[str, Any]:
        """Create a new quest."""
        try:
            quest_id = str(uuid.uuid4())
            
            quest = {
                'quest_id': quest_id,
                'name': name,
                'description': description,
                'quest_type': quest_type,
                'requirements': requirements,
                'rewards': rewards,
                'duration_days': duration_days,
                'created_at': datetime.now(),
                'is_active': True
            }
            
            self.quests[quest_id] = quest
            
            logger.info(f"Created quest: {name} ({quest_id})")
            return {
                'status': 'success',
                'quest_id': quest_id,
                'quest': quest
            }
            
        except Exception as e:
            logger.error(f"Failed to create quest: {e}")
            return {'error': str(e)}
    
    async def start_quest(self, user_id: str, quest_id: str) -> Dict[str, Any]:
        """Start a quest for a user."""
        try:
            if quest_id not in self.quests:
                return {'error': 'Quest not found'}
            
            quest = self.quests[quest_id]
            
            if not quest['is_active']:
                return {'error': 'Quest is not active'}
            
            # Check if user already has this quest
            if user_id in self.user_quests:
                existing_quests = [q['quest_id'] for q in self.user_quests[user_id]]
                if quest_id in existing_quests:
                    return {'error': 'User already has this quest'}
            
            # Start quest
            user_quest = {
                'quest_id': quest_id,
                'user_id': user_id,
                'started_at': datetime.now(),
                'expires_at': datetime.now() + timedelta(days=quest['duration_days']),
                'progress': 0.0,
                'is_completed': False,
                'completed_at': None
            }
            
            if user_id not in self.user_quests:
                self.user_quests[user_id] = []
            self.user_quests[user_id].append(user_quest)
            
            logger.info(f"User {user_id} started quest {quest_id}")
            return {
                'status': 'success',
                'quest_id': quest_id,
                'user_quest': user_quest
            }
            
        except Exception as e:
            logger.error(f"Failed to start quest: {e}")
            return {'error': str(e)}
    
    async def update_quest_progress(self, user_id: str, quest_id: str, 
                                  progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update quest progress for a user."""
        try:
            if user_id not in self.user_quests:
                return {'error': 'User has no active quests'}
            
            # Find user's quest
            user_quest = None
            for quest in self.user_quests[user_id]:
                if quest['quest_id'] == quest_id and not quest['is_completed']:
                    user_quest = quest
                    break
            
            if not user_quest:
                return {'error': 'Quest not found or already completed'}
            
            # Update progress
            quest = self.quests[quest_id]
            new_progress = await self._calculate_quest_progress(quest, progress_data)
            user_quest['progress'] = new_progress
            
            # Check if quest is completed
            if new_progress >= 100.0:
                user_quest['is_completed'] = True
                user_quest['completed_at'] = datetime.now()
                
                # Award rewards
                rewards = await self._award_quest_rewards(user_id, quest['rewards'])
                
                logger.info(f"User {user_id} completed quest {quest_id}")
                return {
                    'status': 'success',
                    'quest_completed': True,
                    'progress': new_progress,
                    'rewards': rewards
                }
            else:
                return {
                    'status': 'success',
                    'quest_completed': False,
                    'progress': new_progress
                }
                
        except Exception as e:
            logger.error(f"Failed to update quest progress: {e}")
            return {'error': str(e)}
    
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user's gamification profile."""
        try:
            # Get user level
            user_level = self.user_levels.get(user_id, {
                'level': 1,
                'points': 0,
                'points_to_next_level': 1000
            })
            
            # Get achievements
            achievements = self.user_achievements.get(user_id, [])
            
            # Get badges
            badges = self.user_badges.get(user_id, [])
            
            # Get active quests
            active_quests = []
            if user_id in self.user_quests:
                active_quests = [q for q in self.user_quests[user_id] if not q['is_completed']]
            
            # Get completed quests
            completed_quests = []
            if user_id in self.user_quests:
                completed_quests = [q for q in self.user_quests[user_id] if q['is_completed']]
            
            return {
                'user_id': user_id,
                'level': user_level,
                'total_points': self.user_points.get(user_id, 0),
                'achievements': achievements,
                'badges': badges,
                'active_quests': active_quests,
                'completed_quests': completed_quests,
                'total_achievements': len(achievements),
                'total_badges': len(badges)
            }
            
        except Exception as e:
            logger.error(f"Failed to get user profile: {e}")
            return {'error': str(e)}
    
    async def _check_level_up(self, user_id: str) -> Dict[str, Any]:
        """Check if user should level up."""
        try:
            current_points = self.user_points.get(user_id, 0)
            current_level = self.user_levels.get(user_id, {}).get('level', 1)
            
            # Calculate required points for next level
            required_points = current_level * 1000
            
            if current_points >= required_points:
                new_level = current_level + 1
                self.user_levels[user_id] = {
                    'level': new_level,
                    'points': current_points,
                    'points_to_next_level': new_level * 1000
                }
                
                return {
                    'leveled_up': True,
                    'new_level': new_level,
                    'points_earned': 100  # Bonus points for leveling up
                }
            else:
                return {
                    'leveled_up': False,
                    'current_level': current_level,
                    'points_to_next_level': required_points - current_points
                }
                
        except Exception as e:
            logger.error(f"Failed to check level up: {e}")
            return {'leveled_up': False}
    
    async def _calculate_quest_progress(self, quest: Dict[str, Any], 
                                      progress_data: Dict[str, Any]) -> float:
        """Calculate quest progress based on requirements."""
        # TODO: Implement quest progress calculation
        # This would check quest requirements against progress data
        return 50.0  # Placeholder
    
    async def _award_quest_rewards(self, user_id: str, rewards: Dict[str, Any]) -> Dict[str, Any]:
        """Award quest rewards to user."""
        try:
            awarded_rewards = []
            
            # Award points
            if 'points' in rewards:
                points = rewards['points']
                if user_id not in self.user_points:
                    self.user_points[user_id] = 0
                self.user_points[user_id] += points
                awarded_rewards.append({'type': 'points', 'amount': points})
            
            # Award achievements
            if 'achievements' in rewards:
                for achievement_id in rewards['achievements']:
                    result = await self.award_achievement(user_id, achievement_id)
                    if result.get('status') == 'success':
                        awarded_rewards.append({'type': 'achievement', 'id': achievement_id})
            
            # Award badges
            if 'badges' in rewards:
                for badge_id in rewards['badges']:
                    result = await self.award_badge(user_id, badge_id)
                    if result.get('status') == 'success':
                        awarded_rewards.append({'type': 'badge', 'id': badge_id})
            
            return {
                'awarded_rewards': awarded_rewards,
                'total_rewards': len(awarded_rewards)
            }
            
        except Exception as e:
            logger.error(f"Failed to award quest rewards: {e}")
            return {'error': str(e)}
    
    def _initialize_default_content(self):
        """Initialize default achievements and badges."""
        # Default achievements
        self.achievements = {
            'first_trade': {
                'achievement_id': 'first_trade',
                'name': 'First Trade',
                'description': 'Complete your first trade',
                'type': AchievementType.TRADING.value,
                'points': 100
            },
            'social_butterfly': {
                'achievement_id': 'social_butterfly',
                'name': 'Social Butterfly',
                'description': 'Follow 10 traders',
                'type': AchievementType.SOCIAL.value,
                'points': 200
            }
        }
        
        # Default badges
        self.badges = {
            'trader_bronze': {
                'badge_id': 'trader_bronze',
                'name': 'Bronze Trader',
                'description': 'Complete 10 trades',
                'type': BadgeType.BRONZE.value,
                'points': 500
            },
            'trader_silver': {
                'badge_id': 'trader_silver',
                'name': 'Silver Trader',
                'description': 'Complete 50 trades',
                'type': BadgeType.SILVER.value,
                'points': 1000
            }
        }
    
    def get_gamification_summary(self) -> Dict[str, Any]:
        """Get gamification system summary."""
        total_achievements = len(self.achievements)
        total_badges = len(self.badges)
        total_quests = len(self.quests)
        total_users = len(self.user_points)
        
        return {
            'total_achievements': total_achievements,
            'total_badges': total_badges,
            'total_quests': total_quests,
            'total_users': total_users,
            'total_user_achievements': sum(len(achievements) for achievements in self.user_achievements.values()),
            'total_user_badges': sum(len(badges) for badges in self.user_badges.values())
        }