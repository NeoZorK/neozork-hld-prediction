"""Strategy Sharing - Strategy sharing and discovery platform"""

import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class StrategyStatus(Enum):
    """Strategy status enumeration."""
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class StrategyCategory(Enum):
    """Strategy category enumeration."""
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    ARBITRAGE = "arbitrage"
    MARKET_MAKING = "market_making"
    TREND_FOLLOWING = "trend_following"
    QUANTITATIVE = "quantitative"


class StrategyLicense(Enum):
    """Strategy license enumeration."""
    FREE = "free"
    PREMIUM = "premium"
    EXCLUSIVE = "exclusive"


@dataclass
class Strategy:
    """Strategy data class."""
    strategy_id: str
    name: str
    description: str
    author_id: str
    category: StrategyCategory
    status: StrategyStatus
    license_type: StrategyLicense
    price: float
    performance_metrics: Dict[str, Any]
    code: str
    parameters: Dict[str, Any]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    download_count: int = 0
    rating: float = 0.0
    review_count: int = 0


class StrategySharing:
    """Strategy sharing and discovery platform."""
    
    def __init__(self):
        self.strategies: Dict[str, Strategy] = {}
        self.strategy_reviews: Dict[str, List[Dict[str, Any]]] = {}
        self.strategy_downloads: Dict[str, List[Dict[str, Any]]] = {}
        
    async def create_strategy(self, author_id: str, name: str, description: str,
                            category: StrategyCategory, code: str,
                            parameters: Dict[str, Any] = None,
                            license_type: StrategyLicense = StrategyLicense.FREE,
                            price: float = 0.0) -> Dict[str, Any]:
        """Create a new trading strategy."""
        try:
            strategy_id = str(uuid.uuid4())
            
            # Validate strategy code
            validation_result = await self._validate_strategy_code(code)
            if not validation_result['valid']:
                return {'error': f'Invalid strategy code: {validation_result["error"]}'}
            
            # Create strategy
            strategy = Strategy(
                strategy_id=strategy_id,
                name=name,
                description=description,
                author_id=author_id,
                category=category,
                status=StrategyStatus.DRAFT,
                license_type=license_type,
                price=price,
                performance_metrics={},
                code=code,
                parameters=parameters or {},
                tags=await self._extract_tags(name, description),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            self.strategies[strategy_id] = strategy
            
            logger.info(f"Created strategy: {name} ({strategy_id}) by {author_id}")
            return {
                'status': 'success',
                'strategy_id': strategy_id,
                'strategy': strategy.__dict__
            }
            
        except Exception as e:
            logger.error(f"Failed to create strategy: {e}")
            return {'error': str(e)}
    
    async def publish_strategy(self, strategy_id: str, author_id: str) -> Dict[str, Any]:
        """Publish a strategy to the marketplace."""
        try:
            if strategy_id not in self.strategies:
                return {'error': 'Strategy not found'}
            
            strategy = self.strategies[strategy_id]
            
            # Verify ownership
            if strategy.author_id != author_id:
                return {'error': 'Unauthorized: Not the strategy author'}
            
            # Update strategy status
            strategy.status = StrategyStatus.PUBLISHED
            strategy.published_at = datetime.now()
            strategy.updated_at = datetime.now()
            
            logger.info(f"Published strategy: {strategy.name} ({strategy_id})")
            return {
                'status': 'success',
                'strategy_id': strategy_id,
                'published_at': strategy.published_at
            }
            
        except Exception as e:
            logger.error(f"Failed to publish strategy: {e}")
            return {'error': str(e)}
    
    async def search_strategies(self, query: str = "", category: Optional[StrategyCategory] = None,
                              min_rating: float = 0.0, max_price: float = float('inf'),
                              sort_by: str = "rating", limit: int = 20) -> Dict[str, Any]:
        """Search and filter strategies."""
        try:
            # Start with all published strategies
            filtered_strategies = [
                strategy for strategy in self.strategies.values()
                if strategy.status == StrategyStatus.PUBLISHED
            ]
            
            # Filter by category
            if category:
                filtered_strategies = [s for s in filtered_strategies if s.category == category]
            
            # Filter by price and rating
            filtered_strategies = [s for s in filtered_strategies if s.price <= max_price and s.rating >= min_rating]
            
            # Text search
            if query:
                query_lower = query.lower()
                filtered_strategies = [
                    s for s in filtered_strategies
                    if (query_lower in s.name.lower() or
                        query_lower in s.description.lower() or
                        any(query_lower in tag.lower() for tag in s.tags))
                ]
            
            # Sort strategies
            if sort_by == "rating":
                filtered_strategies.sort(key=lambda x: x.rating, reverse=True)
            elif sort_by == "downloads":
                filtered_strategies.sort(key=lambda x: x.download_count, reverse=True)
            elif sort_by == "newest":
                filtered_strategies.sort(key=lambda x: x.published_at or x.created_at, reverse=True)
            
            # Apply limit
            filtered_strategies = filtered_strategies[:limit]
            
            # Format results
            results = []
            for strategy in filtered_strategies:
                results.append({
                    'strategy_id': strategy.strategy_id,
                    'name': strategy.name,
                    'description': strategy.description,
                    'author_id': strategy.author_id,
                    'category': strategy.category.value,
                    'license_type': strategy.license_type.value,
                    'price': strategy.price,
                    'rating': strategy.rating,
                    'review_count': strategy.review_count,
                    'download_count': strategy.download_count,
                    'tags': strategy.tags,
                    'published_at': strategy.published_at
                })
            
            logger.info(f"Found {len(results)} strategies matching search criteria")
            return {
                'strategies': results,
                'total_count': len(results),
                'search_params': {
                    'query': query,
                    'category': category.value if category else None,
                    'min_rating': min_rating,
                    'max_price': max_price,
                    'sort_by': sort_by
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to search strategies: {e}")
            return {'error': str(e)}
    
    async def download_strategy(self, strategy_id: str, user_id: str) -> Dict[str, Any]:
        """Download a strategy."""
        try:
            if strategy_id not in self.strategies:
                return {'error': 'Strategy not found'}
            
            strategy = self.strategies[strategy_id]
            
            # Check if strategy is published
            if strategy.status != StrategyStatus.PUBLISHED:
                return {'error': 'Strategy is not available for download'}
            
            # Record download
            download_record = {
                'user_id': user_id,
                'strategy_id': strategy_id,
                'downloaded_at': datetime.now(),
                'license_type': strategy.license_type.value,
                'price_paid': strategy.price if strategy.license_type == StrategyLicense.PREMIUM else 0
            }
            
            if strategy_id not in self.strategy_downloads:
                self.strategy_downloads[strategy_id] = []
            self.strategy_downloads[strategy_id].append(download_record)
            
            # Update download count
            strategy.download_count += 1
            strategy.updated_at = datetime.now()
            
            logger.info(f"Strategy {strategy_id} downloaded by user {user_id}")
            return {
                'status': 'success',
                'strategy_id': strategy_id,
                'download_record': download_record,
                'strategy_code': strategy.code,
                'parameters': strategy.parameters
            }
            
        except Exception as e:
            logger.error(f"Failed to download strategy: {e}")
            return {'error': str(e)}
    
    async def get_strategy_details(self, strategy_id: str) -> Dict[str, Any]:
        """Get detailed information about a strategy."""
        try:
            if strategy_id not in self.strategies:
                return {'error': 'Strategy not found'}
            
            strategy = self.strategies[strategy_id]
            reviews = self.strategy_reviews.get(strategy_id, [])
            downloads = self.strategy_downloads.get(strategy_id, [])
            
            strategy_details = {
                'strategy': strategy.__dict__,
                'reviews': reviews[-10:],  # Last 10 reviews
                'total_reviews': len(reviews),
                'total_downloads': len(downloads),
                'recent_downloads': downloads[-5:] if downloads else []
            }
            
            return strategy_details
            
        except Exception as e:
            logger.error(f"Failed to get strategy details: {e}")
            return {'error': str(e)}
    
    async def _validate_strategy_code(self, code: str) -> Dict[str, Any]:
        """Validate strategy code."""
        try:
            if not code or len(code.strip()) == 0:
                return {'valid': False, 'error': 'Strategy code cannot be empty'}
            
            if len(code) > 100000:  # 100KB limit
                return {'valid': False, 'error': 'Strategy code too large (max 100KB)'}
            
            return {'valid': True, 'error': None}
            
        except Exception as e:
            return {'valid': False, 'error': f'Validation error: {str(e)}'}
    
    async def _extract_tags(self, name: str, description: str) -> List[str]:
        """Extract tags from strategy name and description."""
        text = f"{name} {description}".lower()
        common_tags = ['trading', 'algorithm', 'strategy', 'crypto', 'forex', 'stocks']
        
        tags = []
        for tag in common_tags:
            if tag in text:
                tags.append(tag)
        
        return tags[:5]  # Limit to 5 tags