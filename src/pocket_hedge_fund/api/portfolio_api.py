"""Portfolio API - RESTful API endpoints for portfolio management"""

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

# Import our components
from ..auth.jwt_manager import JWTManager, UserRole, TokenType
from ..fund_management.portfolio_manager_functional import FunctionalPortfolioManager

logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter(prefix="/api/v1/portfolio", tags=["portfolio"])
security = HTTPBearer()


class AddPositionRequest(BaseModel):
    """Request model for adding a position."""
    asset_symbol: str = Field(..., description="Asset symbol", min_length=1, max_length=20)
    asset_name: str = Field(..., description="Asset name", min_length=1, max_length=255)
    asset_type: str = Field(..., description="Asset type", min_length=1, max_length=50)
    quantity: float = Field(..., description="Quantity", gt=0)
    price: float = Field(..., description="Price", gt=0)


class RemovePositionRequest(BaseModel):
    """Request model for removing a position."""
    asset_symbol: str = Field(..., description="Asset symbol", min_length=1, max_length=20)
    quantity: Optional[float] = Field(None, description="Quantity to remove (if None, removes entire position)", gt=0)


class UpdatePricesRequest(BaseModel):
    """Request model for updating position prices."""
    price_updates: Dict[str, float] = Field(..., description="Asset symbol to price mapping")


class RebalanceRequest(BaseModel):
    """Request model for portfolio rebalancing."""
    target_weights: Dict[str, float] = Field(..., description="Target weights for each asset")


class PositionResponse(BaseModel):
    """Response model for position data."""
    position_id: str
    asset_symbol: str
    asset_name: str
    asset_type: str
    quantity: float
    average_price: float
    current_price: Optional[float]
    current_value: Optional[float]
    unrealized_pnl: Optional[float]
    unrealized_pnl_percentage: Optional[float]
    weight_percentage: Optional[float]
    created_at: datetime
    updated_at: datetime


class PortfolioMetricsResponse(BaseModel):
    """Response model for portfolio metrics."""
    fund_id: str
    total_value: float
    initial_capital: float
    total_pnl: float
    total_return_percentage: float
    daily_return: float
    daily_return_percentage: float
    risk_metrics: Optional[Dict[str, Any]]
    calculated_at: datetime


class PortfolioAPI:
    """Portfolio management API endpoints."""
    
    def __init__(self, database_manager, jwt_manager: JWTManager):
        self.database_manager = database_manager
        self.jwt_manager = jwt_manager
        self.portfolio_manager = FunctionalPortfolioManager(database_manager)
        
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
    
    @router.get("/{fund_id}/positions", response_model=List[PositionResponse])
    async def get_portfolio_positions(
        self,
        fund_id: str = Path(..., description="Fund ID"),
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> List[PositionResponse]:
        """Get all portfolio positions for a fund."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "portfolio:read"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to read portfolio"
                )
            
            # Validate fund_id format
            if not self._is_valid_uuid(fund_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid fund ID format"
                )
            
            # Get portfolio positions
            result = await self.portfolio_manager.get_portfolio_positions(fund_id)
            
            if 'error' in result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=result['error']
                )
            
            positions = []
            for position_data in result['positions']:
                positions.append(PositionResponse(
                    position_id=position_data['position_id'],
                    asset_symbol=position_data['asset_symbol'],
                    asset_name=position_data['asset_name'],
                    asset_type=position_data['asset_type'],
                    quantity=position_data['quantity'],
                    average_price=position_data['average_price'],
                    current_price=position_data['current_price'],
                    current_value=position_data['current_value'],
                    unrealized_pnl=position_data['unrealized_pnl'],
                    unrealized_pnl_percentage=position_data['unrealized_pnl_percentage'],
                    weight_percentage=position_data['weight_percentage'],
                    created_at=datetime.fromisoformat(position_data['created_at']),
                    updated_at=datetime.fromisoformat(position_data['updated_at'])
                ))
            
            return positions
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get portfolio positions: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.post("/{fund_id}/positions", response_model=Dict[str, Any])
    async def add_position(
        self,
        fund_id: str = Path(..., description="Fund ID"),
        request: AddPositionRequest = ...,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Add a new position to the portfolio."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "portfolio:update"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to modify portfolio"
                )
            
            # Validate fund_id format
            if not self._is_valid_uuid(fund_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid fund ID format"
                )
            
            # Validate input
            if request.quantity <= 0 or request.price <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Quantity and price must be positive"
                )
            
            # Add position
            result = await self.portfolio_manager.add_position(
                fund_id=fund_id,
                asset_symbol=request.asset_symbol,
                asset_name=request.asset_name,
                asset_type=request.asset_type,
                quantity=request.quantity,
                price=request.price
            )
            
            if 'error' in result:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result['error']
                )
            
            logger.info(f"Position added: {request.asset_symbol} to fund {fund_id}")
            
            return {
                "status": "success",
                "data": result,
                "message": "Position added successfully"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to add position: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.delete("/{fund_id}/positions/{asset_symbol}", response_model=Dict[str, Any])
    async def remove_position(
        self,
        fund_id: str = Path(..., description="Fund ID"),
        asset_symbol: str = Path(..., description="Asset symbol"),
        quantity: Optional[float] = Query(None, description="Quantity to remove (if None, removes entire position)"),
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Remove or reduce a position from the portfolio."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "portfolio:update"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to modify portfolio"
                )
            
            # Validate fund_id format
            if not self._is_valid_uuid(fund_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid fund ID format"
                )
            
            # Remove position
            result = await self.portfolio_manager.remove_position(
                fund_id=fund_id,
                asset_symbol=asset_symbol,
                quantity=quantity
            )
            
            if 'error' in result:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result['error']
                )
            
            logger.info(f"Position removed: {asset_symbol} from fund {fund_id}")
            
            return {
                "status": "success",
                "data": result,
                "message": "Position removed successfully"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to remove position: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.put("/{fund_id}/prices", response_model=Dict[str, Any])
    async def update_position_prices(
        self,
        fund_id: str = Path(..., description="Fund ID"),
        request: UpdatePricesRequest = ...,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Update current prices for portfolio positions."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "portfolio:update"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to modify portfolio"
                )
            
            # Validate fund_id format
            if not self._is_valid_uuid(fund_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid fund ID format"
                )
            
            # Validate input
            if not request.price_updates:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Price updates cannot be empty"
                )
            
            for symbol, price in request.price_updates.items():
                if price <= 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Price for {symbol} must be positive"
                    )
            
            # Update prices
            result = await self.portfolio_manager.update_position_prices(
                fund_id=fund_id,
                price_updates=request.price_updates
            )
            
            if 'error' in result:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result['error']
                )
            
            logger.info(f"Prices updated for {result['total_updated']} positions in fund {fund_id}")
            
            return {
                "status": "success",
                "data": result,
                "message": "Position prices updated successfully"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to update position prices: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.get("/{fund_id}/metrics", response_model=PortfolioMetricsResponse)
    async def get_portfolio_metrics(
        self,
        fund_id: str = Path(..., description="Fund ID"),
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> PortfolioMetricsResponse:
        """Get portfolio performance metrics."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "portfolio:read"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to read portfolio metrics"
                )
            
            # Validate fund_id format
            if not self._is_valid_uuid(fund_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid fund ID format"
                )
            
            # Get portfolio metrics
            result = await self.portfolio_manager.get_portfolio_metrics(fund_id)
            
            if 'error' in result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=result['error']
                )
            
            return PortfolioMetricsResponse(
                fund_id=result['fund_id'],
                total_value=result['total_value'],
                initial_capital=result['initial_capital'],
                total_pnl=result['total_pnl'],
                total_return_percentage=result['total_return_percentage'],
                daily_return=result['daily_return'],
                daily_return_percentage=result['daily_return_percentage'],
                risk_metrics=result['risk_metrics'],
                calculated_at=datetime.fromisoformat(result['calculated_at'])
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get portfolio metrics: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.post("/{fund_id}/rebalance", response_model=Dict[str, Any])
    async def rebalance_portfolio(
        self,
        fund_id: str = Path(..., description="Fund ID"),
        request: RebalanceRequest = ...,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Rebalance portfolio to target weights."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "portfolio:update"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to modify portfolio"
                )
            
            # Validate fund_id format
            if not self._is_valid_uuid(fund_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid fund ID format"
                )
            
            # Validate input
            if not request.target_weights:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Target weights cannot be empty"
                )
            
            # Validate weights sum to 100%
            total_weight = sum(request.target_weights.values())
            if abs(total_weight - 100.0) > 0.01:  # Allow small floating point errors
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Target weights must sum to 100%, got {total_weight}%"
                )
            
            for symbol, weight in request.target_weights.items():
                if weight < 0 or weight > 100:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Weight for {symbol} must be between 0% and 100%"
                    )
            
            # Rebalance portfolio
            result = await self.portfolio_manager.rebalance_portfolio(
                fund_id=fund_id,
                target_weights=request.target_weights
            )
            
            if 'error' in result:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result['error']
                )
            
            logger.info(f"Portfolio rebalanced for fund {fund_id}: {result['total_trades']} trades executed")
            
            return {
                "status": "success",
                "data": result,
                "message": "Portfolio rebalancing completed successfully"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to rebalance portfolio: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.get("/{fund_id}/transactions")
    async def get_portfolio_transactions(
        self,
        fund_id: str = Path(..., description="Fund ID"),
        page: int = Query(1, description="Page number", ge=1),
        page_size: int = Query(20, description="Page size", ge=1, le=100),
        transaction_type: Optional[str] = Query(None, description="Filter by transaction type"),
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Get portfolio transaction history."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "portfolio:read"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to read portfolio transactions"
                )
            
            # Validate fund_id format
            if not self._is_valid_uuid(fund_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid fund ID format"
                )
            
            # Build query with filters
            where_conditions = ["fund_id = :fund_id"]
            params = {"fund_id": fund_id}
            
            if transaction_type:
                where_conditions.append("transaction_type = :transaction_type")
                params["transaction_type"] = transaction_type
            
            where_clause = "WHERE " + " AND ".join(where_conditions)
            
            # Add pagination
            offset = (page - 1) * page_size
            params["limit"] = page_size
            params["offset"] = offset
            
            query = f"""
            SELECT * FROM transactions 
            {where_clause}
            ORDER BY executed_at DESC
            LIMIT :limit OFFSET :offset
            """
            
            result = await self.database_manager.execute_query(query, params)
            
            if 'error' in result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {result['error']}"
                )
            
            transactions = []
            for row in result['query_result']['data']:
                transactions.append({
                    "transaction_id": row['id'],
                    "transaction_type": row['transaction_type'],
                    "asset_symbol": row['asset_symbol'],
                    "quantity": float(row['quantity']),
                    "price": float(row['price']),
                    "total_amount": float(row['total_amount']),
                    "fees": float(row['fees']),
                    "executed_at": row['executed_at'].isoformat()
                })
            
            return {
                "fund_id": fund_id,
                "transactions": transactions,
                "page": page,
                "page_size": page_size,
                "total_transactions": len(transactions)
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get portfolio transactions: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    def _is_valid_uuid(self, uuid_string: str) -> bool:
        """Validate UUID format."""
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False


# Create router instance
def create_portfolio_api_router(database_manager, jwt_manager: JWTManager) -> APIRouter:
    """Create and configure the portfolio API router."""
    api = PortfolioAPI(database_manager, jwt_manager)
    
    # Add the router methods to the router
    router.add_api_route("/{fund_id}/positions", api.get_portfolio_positions, methods=["GET"])
    router.add_api_route("/{fund_id}/positions", api.add_position, methods=["POST"])
    router.add_api_route("/{fund_id}/positions/{asset_symbol}", api.remove_position, methods=["DELETE"])
    router.add_api_route("/{fund_id}/prices", api.update_position_prices, methods=["PUT"])
    router.add_api_route("/{fund_id}/metrics", api.get_portfolio_metrics, methods=["GET"])
    router.add_api_route("/{fund_id}/rebalance", api.rebalance_portfolio, methods=["POST"])
    router.add_api_route("/{fund_id}/transactions", api.get_portfolio_transactions, methods=["GET"])
    
    return router
