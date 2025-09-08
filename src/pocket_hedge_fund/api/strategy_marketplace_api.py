"""Strategy Marketplace API - RESTful API endpoints for strategy sharing and trading"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import uuid
import json

# Import our components
from ..auth.jwt_manager import JWTManager, UserRole, TokenType

logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter(prefix="/api/v1/strategies", tags=["strategy-marketplace"])
security = HTTPBearer()


class StrategyType(Enum):
    """Strategy type enumeration."""
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    ARBITRAGE = "arbitrage"
    SCALPING = "scalping"
    SWING = "swing"
    TREND_FOLLOWING = "trend_following"
    CONTRARIAN = "contrarian"
    PAIRS_TRADING = "pairs_trading"
    GRID_TRADING = "grid_trading"
    DCA = "dca"


class StrategyStatus(Enum):
    """Strategy status enumeration."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    SUSPENDED = "suspended"


class CreateStrategyRequest(BaseModel):
    """Request model for creating a new strategy."""
    name: str = Field(..., description="Strategy name", min_length=1, max_length=255)
    description: str = Field(..., description="Strategy description", min_length=1, max_length=2000)
    strategy_type: str = Field(..., description="Strategy type")
    parameters: Dict[str, Any] = Field(..., description="Strategy parameters")
    risk_level: int = Field(..., description="Risk level (1-10)", ge=1, le=10)
    expected_return: float = Field(..., description="Expected annual return (%)", ge=0, le=1000)
    max_drawdown: float = Field(..., description="Maximum expected drawdown (%)", ge=0, le=100)
    min_capital: float = Field(..., description="Minimum capital required", gt=0)
    tags: List[str] = Field(default=[], description="Strategy tags")
    is_public: bool = Field(default=False, description="Public visibility")
    price: float = Field(default=0.0, description="Strategy price (0 for free)", ge=0)


class UpdateStrategyRequest(BaseModel):
    """Request model for updating strategy information."""
    name: Optional[str] = Field(None, description="Strategy name", min_length=1, max_length=255)
    description: Optional[str] = Field(None, description="Strategy description", min_length=1, max_length=2000)
    parameters: Optional[Dict[str, Any]] = Field(None, description="Strategy parameters")
    risk_level: Optional[int] = Field(None, description="Risk level (1-10)", ge=1, le=10)
    expected_return: Optional[float] = Field(None, description="Expected annual return (%)", ge=0, le=1000)
    max_drawdown: Optional[float] = Field(None, description="Maximum expected drawdown (%)", ge=0, le=100)
    min_capital: Optional[float] = Field(None, description="Minimum capital required", gt=0)
    tags: Optional[List[str]] = Field(None, description="Strategy tags")
    is_public: Optional[bool] = Field(None, description="Public visibility")
    price: Optional[float] = Field(None, description="Strategy price (0 for free)", ge=0)
    status: Optional[str] = Field(None, description="Strategy status")


class StrategyResponse(BaseModel):
    """Response model for strategy data."""
    strategy_id: str
    name: str
    description: str
    strategy_type: str
    parameters: Dict[str, Any]
    risk_level: int
    expected_return: float
    max_drawdown: float
    min_capital: float
    tags: List[str]
    is_public: bool
    price: float
    status: str
    author_id: str
    author_name: str
    created_at: datetime
    updated_at: datetime
    total_views: int
    total_downloads: int
    rating: float
    total_ratings: int


class StrategyListResponse(BaseModel):
    """Response model for strategy list."""
    strategies: List[StrategyResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int


class StrategyStatsResponse(BaseModel):
    """Response model for strategy statistics."""
    total_strategies: int
    public_strategies: int
    private_strategies: int
    strategies_by_type: Dict[str, int]
    strategies_by_status: Dict[str, int]
    total_downloads: int
    total_views: int
    average_rating: float


class StrategyMarketplaceAPI:
    """Strategy marketplace API endpoints."""
    
    def __init__(self, database_manager, jwt_manager: JWTManager):
        self.database_manager = database_manager
        self.jwt_manager = jwt_manager
        
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
        """Get current authenticated user from token."""
        try:
            token = credentials.credentials
            payload = self.jwt_manager.verify_token(token, TokenType.ACCESS)
            
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Get user details from database
            user_query = """
            SELECT * FROM users WHERE id = :user_id
            """
            
            user_result = await self.database_manager.execute_query(
                user_query, 
                {"user_id": payload.user_id}
            )
            
            if 'error' in user_result or not user_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            user_data = user_result['query_result']['data'][0]
            
            return {
                "user_id": user_data['id'],
                "username": user_data['username'],
                "email": user_data['email'],
                "role": payload.role,
                "permissions": payload.permissions,
                "is_active": user_data['is_active']
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get current user: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def _check_permission(self, user_permissions: List[str], required_permission: str) -> bool:
        """Check if user has required permission."""
        return self.jwt_manager.has_permission(user_permissions, required_permission)
    
    def _validate_strategy_type(self, strategy_type: str) -> bool:
        """Validate strategy type."""
        try:
            StrategyType(strategy_type.lower())
            return True
        except ValueError:
            return False
    
    def _validate_strategy_status(self, status: str) -> bool:
        """Validate strategy status."""
        try:
            StrategyStatus(status.lower())
            return True
        except ValueError:
            return False
    
    def _is_valid_uuid(self, uuid_string: str) -> bool:
        """Validate UUID format."""
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False
    
    @router.post("/", response_model=StrategyResponse)
    async def create_strategy(
        self,
        request: CreateStrategyRequest = ...,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> StrategyResponse:
        """Create a new trading strategy."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "strategies:create"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to create strategies"
                )
            
            # Validate strategy type
            if not self._validate_strategy_type(request.strategy_type):
                valid_types = [t.value for t in StrategyType]
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid strategy type: {request.strategy_type}. Valid types are: {', '.join(valid_types)}"
                )
            
            # Validate parameters
            if not isinstance(request.parameters, dict):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Parameters must be a valid JSON object"
                )
            
            # Create strategy
            strategy_id = str(uuid.uuid4())
            create_strategy_query = """
            INSERT INTO strategies (
                id, name, description, strategy_type, parameters, risk_level,
                expected_return, max_drawdown, min_capital, tags, is_public,
                price, status, author_id, created_at, updated_at
            ) VALUES (
                :id, :name, :description, :strategy_type, :parameters, :risk_level,
                :expected_return, :max_drawdown, :min_capital, :tags, :is_public,
                :price, :status, :author_id, :created_at, :updated_at
            )
            """
            
            now = datetime.now()
            create_params = {
                "id": strategy_id,
                "name": request.name,
                "description": request.description,
                "strategy_type": request.strategy_type.lower(),
                "parameters": json.dumps(request.parameters),
                "risk_level": request.risk_level,
                "expected_return": request.expected_return,
                "max_drawdown": request.max_drawdown,
                "min_capital": request.min_capital,
                "tags": json.dumps(request.tags),
                "is_public": request.is_public,
                "price": request.price,
                "status": StrategyStatus.DRAFT.value,
                "author_id": current_user['user_id'],
                "created_at": now,
                "updated_at": now
            }
            
            create_result = await self.database_manager.execute_query(create_strategy_query, create_params)
            
            if 'error' in create_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to create strategy: {create_result['error']}"
                )
            
            # Get created strategy with author info
            get_strategy_query = """
            SELECT s.*, u.username as author_name
            FROM strategies s
            JOIN users u ON s.author_id = u.id
            WHERE s.id = :strategy_id
            """
            
            get_strategy_result = await self.database_manager.execute_query(
                get_strategy_query,
                {"strategy_id": strategy_id}
            )
            
            if 'error' in get_strategy_result or not get_strategy_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve created strategy"
                )
            
            strategy_data = get_strategy_result['query_result']['data'][0]
            
            logger.info(f"Strategy created successfully: {request.name} ({strategy_id})")
            
            return StrategyResponse(
                strategy_id=strategy_data['id'],
                name=strategy_data['name'],
                description=strategy_data['description'],
                strategy_type=strategy_data['strategy_type'],
                parameters=json.loads(strategy_data['parameters']),
                risk_level=strategy_data['risk_level'],
                expected_return=strategy_data['expected_return'],
                max_drawdown=strategy_data['max_drawdown'],
                min_capital=strategy_data['min_capital'],
                tags=json.loads(strategy_data['tags']),
                is_public=strategy_data['is_public'],
                price=strategy_data['price'],
                status=strategy_data['status'],
                author_id=strategy_data['author_id'],
                author_name=strategy_data['author_name'],
                created_at=strategy_data['created_at'],
                updated_at=strategy_data['updated_at'],
                total_views=0,
                total_downloads=0,
                rating=0.0,
                total_ratings=0
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to create strategy: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.get("/", response_model=StrategyListResponse)
    async def get_strategies(
        self,
        page: int = Query(1, description="Page number", ge=1),
        page_size: int = Query(20, description="Page size", ge=1, le=100),
        strategy_type: Optional[str] = Query(None, description="Filter by strategy type"),
        risk_level: Optional[int] = Query(None, description="Filter by risk level", ge=1, le=10),
        min_return: Optional[float] = Query(None, description="Minimum expected return"),
        max_drawdown: Optional[float] = Query(None, description="Maximum drawdown"),
        tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
        search: Optional[str] = Query(None, description="Search by name or description"),
        sort_by: str = Query("created_at", description="Sort by field"),
        sort_order: str = Query("desc", description="Sort order (asc/desc)"),
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> StrategyListResponse:
        """Get list of strategies with pagination and filtering."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "strategies:read"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to read strategies"
                )
            
            # Build query with filters
            where_conditions = ["s.status = 'published'"]
            params = {}
            
            if strategy_type:
                where_conditions.append("s.strategy_type = :strategy_type")
                params["strategy_type"] = strategy_type.lower()
            
            if risk_level:
                where_conditions.append("s.risk_level = :risk_level")
                params["risk_level"] = risk_level
            
            if min_return:
                where_conditions.append("s.expected_return >= :min_return")
                params["min_return"] = min_return
            
            if max_drawdown:
                where_conditions.append("s.max_drawdown <= :max_drawdown")
                params["max_drawdown"] = max_drawdown
            
            if tags:
                tag_list = [tag.strip() for tag in tags.split(',')]
                tag_conditions = []
                for i, tag in enumerate(tag_list):
                    tag_conditions.append(f"s.tags LIKE :tag_{i}")
                    params[f"tag_{i}"] = f"%{tag}%"
                if tag_conditions:
                    where_conditions.append(f"({' OR '.join(tag_conditions)})")
            
            if search:
                where_conditions.append("(s.name ILIKE :search OR s.description ILIKE :search)")
                params["search"] = f"%{search}%"
            
            where_clause = "WHERE " + " AND ".join(where_conditions)
            
            # Validate sort fields
            valid_sort_fields = ["created_at", "updated_at", "name", "expected_return", "risk_level", "rating"]
            if sort_by not in valid_sort_fields:
                sort_by = "created_at"
            
            if sort_order.lower() not in ["asc", "desc"]:
                sort_order = "desc"
            
            # Get total count
            count_query = f"""
            SELECT COUNT(*) as total 
            FROM strategies s
            JOIN users u ON s.author_id = u.id
            {where_clause}
            """
            count_result = await self.database_manager.execute_query(count_query, params)
            
            if 'error' in count_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {count_result['error']}"
                )
            
            total_count = count_result['query_result']['data'][0]['total']
            total_pages = (total_count + page_size - 1) // page_size
            
            # Get strategies with pagination
            offset = (page - 1) * page_size
            params["limit"] = page_size
            params["offset"] = offset
            
            strategies_query = f"""
            SELECT s.*, u.username as author_name,
                   COALESCE(sp.total_views, 0) as total_views,
                   COALESCE(sp.total_downloads, 0) as total_downloads,
                   COALESCE(sp.rating, 0.0) as rating,
                   COALESCE(sp.total_ratings, 0) as total_ratings
            FROM strategies s
            JOIN users u ON s.author_id = u.id
            LEFT JOIN strategy_performance sp ON s.id = sp.strategy_id
            {where_clause}
            ORDER BY s.{sort_by} {sort_order.upper()}
            LIMIT :limit OFFSET :offset
            """
            
            strategies_result = await self.database_manager.execute_query(strategies_query, params)
            
            if 'error' in strategies_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {strategies_result['error']}"
                )
            
            strategies = []
            for strategy_data in strategies_result['query_result']['data']:
                strategies.append(StrategyResponse(
                    strategy_id=strategy_data['id'],
                    name=strategy_data['name'],
                    description=strategy_data['description'],
                    strategy_type=strategy_data['strategy_type'],
                    parameters=json.loads(strategy_data['parameters']),
                    risk_level=strategy_data['risk_level'],
                    expected_return=strategy_data['expected_return'],
                    max_drawdown=strategy_data['max_drawdown'],
                    min_capital=strategy_data['min_capital'],
                    tags=json.loads(strategy_data['tags']),
                    is_public=strategy_data['is_public'],
                    price=strategy_data['price'],
                    status=strategy_data['status'],
                    author_id=strategy_data['author_id'],
                    author_name=strategy_data['author_name'],
                    created_at=strategy_data['created_at'],
                    updated_at=strategy_data['updated_at'],
                    total_views=strategy_data['total_views'],
                    total_downloads=strategy_data['total_downloads'],
                    rating=strategy_data['rating'],
                    total_ratings=strategy_data['total_ratings']
                ))
            
            return StrategyListResponse(
                strategies=strategies,
                total_count=total_count,
                page=page,
                page_size=page_size,
                total_pages=total_pages
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get strategies: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.get("/{strategy_id}", response_model=StrategyResponse)
    async def get_strategy(
        self,
        strategy_id: str = Path(..., description="Strategy ID"),
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> StrategyResponse:
        """Get strategy by ID."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "strategies:read"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to read strategies"
                )
            
            # Validate strategy_id format
            if not self._is_valid_uuid(strategy_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid strategy ID format"
                )
            
            # Get strategy
            strategy_query = """
            SELECT s.*, u.username as author_name,
                   COALESCE(sp.total_views, 0) as total_views,
                   COALESCE(sp.total_downloads, 0) as total_downloads,
                   COALESCE(sp.rating, 0.0) as rating,
                   COALESCE(sp.total_ratings, 0) as total_ratings
            FROM strategies s
            JOIN users u ON s.author_id = u.id
            LEFT JOIN strategy_performance sp ON s.id = sp.strategy_id
            WHERE s.id = :strategy_id
            """
            
            strategy_result = await self.database_manager.execute_query(
                strategy_query,
                {"strategy_id": strategy_id}
            )
            
            if 'error' in strategy_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {strategy_result['error']}"
                )
            
            if not strategy_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Strategy not found"
                )
            
            strategy_data = strategy_result['query_result']['data'][0]
            
            # Increment view count
            view_query = """
            INSERT INTO strategy_performance (strategy_id, total_views, total_downloads, rating, total_ratings)
            VALUES (:strategy_id, 1, 0, 0.0, 0)
            ON CONFLICT (strategy_id) 
            DO UPDATE SET total_views = strategy_performance.total_views + 1
            """
            
            await self.database_manager.execute_query(view_query, {"strategy_id": strategy_id})
            
            return StrategyResponse(
                strategy_id=strategy_data['id'],
                name=strategy_data['name'],
                description=strategy_data['description'],
                strategy_type=strategy_data['strategy_type'],
                parameters=json.loads(strategy_data['parameters']),
                risk_level=strategy_data['risk_level'],
                expected_return=strategy_data['expected_return'],
                max_drawdown=strategy_data['max_drawdown'],
                min_capital=strategy_data['min_capital'],
                tags=json.loads(strategy_data['tags']),
                is_public=strategy_data['is_public'],
                price=strategy_data['price'],
                status=strategy_data['status'],
                author_id=strategy_data['author_id'],
                author_name=strategy_data['author_name'],
                created_at=strategy_data['created_at'],
                updated_at=strategy_data['updated_at'],
                total_views=strategy_data['total_views'] + 1,
                total_downloads=strategy_data['total_downloads'],
                rating=strategy_data['rating'],
                total_ratings=strategy_data['total_ratings']
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get strategy: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.get("/stats/overview", response_model=StrategyStatsResponse)
    async def get_strategy_stats(
        self,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> StrategyStatsResponse:
        """Get strategy marketplace statistics."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "strategies:read"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to read strategy statistics"
                )
            
            # Get total strategies
            total_query = "SELECT COUNT(*) as total FROM strategies"
            total_result = await self.database_manager.execute_query(total_query)
            
            if 'error' in total_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {total_result['error']}"
                )
            
            total_strategies = total_result['query_result']['data'][0]['total']
            
            # Get public/private strategies
            public_query = "SELECT COUNT(*) as total FROM strategies WHERE is_public = true"
            public_result = await self.database_manager.execute_query(public_query)
            
            if 'error' in public_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {public_result['error']}"
                )
            
            public_strategies = public_result['query_result']['data'][0]['total']
            private_strategies = total_strategies - public_strategies
            
            # Get strategies by type
            type_query = "SELECT strategy_type, COUNT(*) as count FROM strategies GROUP BY strategy_type"
            type_result = await self.database_manager.execute_query(type_query)
            
            if 'error' in type_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {type_result['error']}"
                )
            
            strategies_by_type = {}
            for row in type_result['query_result']['data']:
                strategies_by_type[row['strategy_type']] = row['count']
            
            # Get strategies by status
            status_query = "SELECT status, COUNT(*) as count FROM strategies GROUP BY status"
            status_result = await self.database_manager.execute_query(status_query)
            
            if 'error' in status_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {status_result['error']}"
                )
            
            strategies_by_status = {}
            for row in status_result['query_result']['data']:
                strategies_by_status[row['status']] = row['count']
            
            # Get total downloads and views
            stats_query = """
            SELECT 
                COALESCE(SUM(total_downloads), 0) as total_downloads,
                COALESCE(SUM(total_views), 0) as total_views,
                COALESCE(AVG(rating), 0.0) as average_rating
            FROM strategy_performance
            """
            stats_result = await self.database_manager.execute_query(stats_query)
            
            if 'error' in stats_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {stats_result['error']}"
                )
            
            stats_data = stats_result['query_result']['data'][0]
            
            return StrategyStatsResponse(
                total_strategies=total_strategies,
                public_strategies=public_strategies,
                private_strategies=private_strategies,
                strategies_by_type=strategies_by_type,
                strategies_by_status=strategies_by_status,
                total_downloads=stats_data['total_downloads'],
                total_views=stats_data['total_views'],
                average_rating=float(stats_data['average_rating'])
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get strategy stats: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


# Create router instance
def create_strategy_marketplace_api_router(database_manager, jwt_manager: JWTManager) -> APIRouter:
    """Create and configure the strategy marketplace API router."""
    api = StrategyMarketplaceAPI(database_manager, jwt_manager)
    
    # Add the router methods to the router
    router.add_api_route("/", api.create_strategy, methods=["POST"])
    router.add_api_route("/", api.get_strategies, methods=["GET"])
    router.add_api_route("/{strategy_id}", api.get_strategy, methods=["GET"])
    router.add_api_route("/stats/overview", api.get_strategy_stats, methods=["GET"])
    
    return router
