"""Strategy API - RESTful API endpoints for strategy marketplace"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import uuid

logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter(prefix="/api/v1/strategies", tags=["strategies"])
security = HTTPBearer()


class StrategyCategory(str, Enum):
    """Strategy category enumeration."""
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    ARBITRAGE = "arbitrage"
    MARKET_MAKING = "market_making"
    TREND_FOLLOWING = "trend_following"
    QUANTITATIVE = "quantitative"


class StrategyLicense(str, Enum):
    """Strategy license enumeration."""
    FREE = "free"
    PREMIUM = "premium"
    EXCLUSIVE = "exclusive"


class CreateStrategyRequest(BaseModel):
    """Request model for creating a strategy."""
    name: str = Field(..., description="Strategy name", min_length=1, max_length=100)
    description: str = Field(..., description="Strategy description", min_length=1, max_length=1000)
    category: StrategyCategory = Field(..., description="Strategy category")
    code: str = Field(..., description="Strategy code", min_length=1)
    parameters: Optional[Dict[str, Any]] = Field(None, description="Strategy parameters")
    license_type: StrategyLicense = Field(default=StrategyLicense.FREE, description="License type")
    price: float = Field(default=0.0, description="Strategy price", ge=0)


class StrategyResponse(BaseModel):
    """Response model for strategy data."""
    strategy_id: str
    name: str
    description: str
    author_id: str
    category: StrategyCategory
    license_type: StrategyLicense
    price: float
    rating: float
    review_count: int
    download_count: int
    tags: List[str]
    created_at: datetime
    published_at: Optional[datetime] = None


class SearchStrategiesRequest(BaseModel):
    """Request model for searching strategies."""
    query: Optional[str] = Field(None, description="Search query")
    category: Optional[StrategyCategory] = Field(None, description="Filter by category")
    min_rating: float = Field(default=0.0, description="Minimum rating", ge=0, le=5)
    max_price: float = Field(default=float('inf'), description="Maximum price", ge=0)
    sort_by: str = Field(default="rating", description="Sort by field")
    limit: int = Field(default=20, description="Number of results", ge=1, le=100)


class StrategyAPI:
    """Strategy marketplace API endpoints."""
    
    def __init__(self):
        self.strategy_sharing = None  # Will be injected
        self.licensing_system = None  # Will be injected
        self.revenue_sharing = None  # Will be injected
        self.marketplace_analytics = None  # Will be injected
        
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
        """Get current authenticated user."""
        # TODO: Implement JWT token validation
        return "user_123"  # Placeholder
    
    @router.post("/", response_model=StrategyResponse, status_code=201)
    async def create_strategy(
        self,
        request: CreateStrategyRequest,
        current_user: str = Depends(get_current_user)
    ) -> StrategyResponse:
        """Create a new trading strategy."""
        try:
            result = await self.strategy_sharing.create_strategy(
                author_id=current_user,
                name=request.name,
                description=request.description,
                category=request.category,
                code=request.code,
                parameters=request.parameters,
                license_type=request.license_type,
                price=request.price
            )
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            strategy_data = result['strategy']
            
            return StrategyResponse(
                strategy_id=strategy_data['strategy_id'],
                name=strategy_data['name'],
                description=strategy_data['description'],
                author_id=strategy_data['author_id'],
                category=strategy_data['category'],
                license_type=strategy_data['license_type'],
                price=strategy_data['price'],
                rating=strategy_data['rating'],
                review_count=strategy_data['review_count'],
                download_count=strategy_data['download_count'],
                tags=strategy_data['tags'],
                created_at=strategy_data['created_at'],
                published_at=strategy_data.get('published_at')
            )
            
        except Exception as e:
            logger.error(f"Failed to create strategy: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.post("/search", response_model=List[StrategyResponse])
    async def search_strategies(
        self,
        request: SearchStrategiesRequest,
        current_user: str = Depends(get_current_user)
    ) -> List[StrategyResponse]:
        """Search and filter strategies."""
        try:
            result = await self.strategy_sharing.search_strategies(
                query=request.query,
                category=request.category,
                min_rating=request.min_rating,
                max_price=request.max_price,
                sort_by=request.sort_by,
                limit=request.limit
            )
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            strategies = []
            for strategy_data in result['strategies']:
                strategies.append(StrategyResponse(
                    strategy_id=strategy_data['strategy_id'],
                    name=strategy_data['name'],
                    description=strategy_data['description'],
                    author_id=strategy_data['author_id'],
                    category=strategy_data['category'],
                    license_type=strategy_data['license_type'],
                    price=strategy_data['price'],
                    rating=strategy_data['rating'],
                    review_count=strategy_data['review_count'],
                    download_count=strategy_data['download_count'],
                    tags=strategy_data['tags'],
                    created_at=datetime.now(),  # TODO: Get from strategy data
                    published_at=strategy_data.get('published_at')
                ))
            
            return strategies
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to search strategies: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/{strategy_id}", response_model=Dict[str, Any])
    async def get_strategy_details(
        self,
        strategy_id: str = Path(..., description="Strategy ID"),
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Get detailed information about a strategy."""
        try:
            result = await self.strategy_sharing.get_strategy_details(strategy_id)
            
            if 'error' in result:
                raise HTTPException(status_code=404, detail=result['error'])
            
            return {
                'status': 'success',
                'data': result
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get strategy details: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.post("/{strategy_id}/publish")
    async def publish_strategy(
        self,
        strategy_id: str = Path(..., description="Strategy ID"),
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Publish a strategy to the marketplace."""
        try:
            result = await self.strategy_sharing.publish_strategy(strategy_id, current_user)
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return {
                'status': 'success',
                'message': 'Strategy published successfully',
                'data': result
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to publish strategy: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.post("/{strategy_id}/download")
    async def download_strategy(
        self,
        strategy_id: str = Path(..., description="Strategy ID"),
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Download a strategy."""
        try:
            result = await self.strategy_sharing.download_strategy(strategy_id, current_user)
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return {
                'status': 'success',
                'message': 'Strategy downloaded successfully',
                'data': result
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to download strategy: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/{strategy_id}/analytics")
    async def get_strategy_analytics(
        self,
        strategy_id: str = Path(..., description="Strategy ID"),
        period_days: int = Query(30, description="Period in days", ge=1, le=365),
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Get analytics for a specific strategy."""
        try:
            result = await self.marketplace_analytics.get_strategy_analytics(strategy_id, period_days)
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return {
                'status': 'success',
                'data': result
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get strategy analytics: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/user/{user_id}", response_model=List[StrategyResponse])
    async def get_user_strategies(
        self,
        user_id: str = Path(..., description="User ID"),
        include_drafts: bool = Query(False, description="Include draft strategies"),
        current_user: str = Depends(get_current_user)
    ) -> List[StrategyResponse]:
        """Get strategies created by a user."""
        try:
            result = await self.strategy_sharing.get_user_strategies(user_id, include_drafts)
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            strategies = []
            for strategy_data in result['strategies']:
                strategies.append(StrategyResponse(
                    strategy_id=strategy_data['strategy_id'],
                    name=strategy_data['name'],
                    description=strategy_data['description'],
                    author_id=strategy_data['author_id'],
                    category=strategy_data['category'],
                    license_type=strategy_data['license_type'],
                    price=strategy_data['price'],
                    rating=strategy_data['rating'],
                    review_count=strategy_data['review_count'],
                    download_count=strategy_data['download_count'],
                    tags=strategy_data['tags'],
                    created_at=strategy_data['created_at'],
                    published_at=strategy_data.get('published_at')
                ))
            
            return strategies
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get user strategies: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/marketplace/insights")
    async def get_marketplace_insights(
        self,
        period_days: int = Query(30, description="Period in days", ge=1, le=365),
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Get marketplace insights and recommendations."""
        try:
            result = await self.marketplace_analytics.get_marketplace_insights(period_days)
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return {
                'status': 'success',
                'data': result
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get marketplace insights: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")


# Create API instance
strategy_api = StrategyAPI()

# Add routes to router
router.add_api_route("/", strategy_api.create_strategy, methods=["POST"])
router.add_api_route("/search", strategy_api.search_strategies, methods=["POST"])
router.add_api_route("/{strategy_id}", strategy_api.get_strategy_details, methods=["GET"])
router.add_api_route("/{strategy_id}/publish", strategy_api.publish_strategy, methods=["POST"])
router.add_api_route("/{strategy_id}/download", strategy_api.download_strategy, methods=["POST"])
router.add_api_route("/{strategy_id}/analytics", strategy_api.get_strategy_analytics, methods=["GET"])
router.add_api_route("/user/{user_id}", strategy_api.get_user_strategies, methods=["GET"])
router.add_api_route("/marketplace/insights", strategy_api.get_marketplace_insights, methods=["GET"])