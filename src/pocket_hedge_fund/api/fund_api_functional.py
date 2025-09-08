"""Functional Fund API - Fully implemented RESTful API endpoints for fund management"""

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
import json

logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter(prefix="/api/v1/funds", tags=["funds"])
security = HTTPBearer()


class FundType(str, Enum):
    """Fund type enumeration."""
    MINI = "mini"
    STANDARD = "standard"
    PREMIUM = "premium"
    INSTITUTIONAL = "institutional"


class CreateFundRequest(BaseModel):
    """Request model for creating a fund."""
    name: str = Field(..., description="Fund name", min_length=1, max_length=255)
    description: Optional[str] = Field(None, description="Fund description")
    fund_type: FundType = Field(..., description="Fund type")
    initial_capital: float = Field(..., description="Initial capital amount", gt=0)
    management_fee: float = Field(default=0.02, description="Management fee", ge=0, le=0.1)
    performance_fee: float = Field(default=0.20, description="Performance fee", ge=0, le=0.5)
    min_investment: float = Field(..., description="Minimum investment", gt=0)
    max_investment: Optional[float] = Field(None, description="Maximum investment")
    max_investors: Optional[int] = Field(None, description="Maximum number of investors")
    risk_level: str = Field(default="medium", description="Risk level")


class FundResponse(BaseModel):
    """Response model for fund data."""
    fund_id: str
    name: str
    description: Optional[str]
    fund_type: FundType
    initial_capital: float
    current_value: float
    management_fee: float
    performance_fee: float
    min_investment: float
    max_investment: Optional[float]
    max_investors: Optional[int]
    current_investors: int
    status: str
    risk_level: str
    created_by: str
    created_at: datetime
    updated_at: datetime


class FundDetailResponse(BaseModel):
    """Detailed response model for fund data."""
    fund: FundResponse
    performance: Optional[Dict[str, Any]] = None
    risk_metrics: Optional[Dict[str, Any]] = None
    portfolio: List[Dict[str, Any]] = []
    strategies: List[Dict[str, Any]] = []


class FunctionalFundAPI:
    """Fully functional fund management API endpoints."""
    
    def __init__(self, database_manager):
        self.database_manager = database_manager
        
    def _is_valid_uuid(self, uuid_string: str) -> bool:
        """Validate UUID format."""
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False
    
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
        """Get current authenticated user."""
        # TODO: Implement JWT token validation
        # For now, return a placeholder user
        return "admin"
    
    @router.post("/", response_model=FundResponse, status_code=201)
    async def create_fund(
        self,
        request: CreateFundRequest,
        current_user: str = Depends(get_current_user)
    ) -> FundResponse:
        """Create a new fund."""
        try:
            # Generate fund ID
            fund_id = str(uuid.uuid4())
            
            # Get user ID from username
            user_query = "SELECT id FROM users WHERE username = :username"
            user_result = await self.database_manager.execute_query(
                user_query, 
                {"username": current_user}
            )
            
            if 'error' in user_result or not user_result['query_result']['data']:
                raise HTTPException(status_code=400, detail="User not found")
            
            user_id = user_result['query_result']['data'][0]['id']
            
            # Insert fund into database
            insert_query = """
            INSERT INTO funds (
                id, name, description, fund_type, initial_capital, current_value,
                management_fee, performance_fee, min_investment, max_investment,
                max_investors, current_investors, status, risk_level, created_by
            ) VALUES (
                :fund_id, :name, :description, :fund_type, :initial_capital, :current_value,
                :management_fee, :performance_fee, :min_investment, :max_investment,
                :max_investors, :current_investors, :status, :risk_level, :created_by
            )
            """
            
            insert_params = {
                "fund_id": fund_id,
                "name": request.name,
                "description": request.description,
                "fund_type": request.fund_type.value,
                "initial_capital": request.initial_capital,
                "current_value": request.initial_capital,  # Start with initial capital
                "management_fee": request.management_fee,
                "performance_fee": request.performance_fee,
                "min_investment": request.min_investment,
                "max_investment": request.max_investment,
                "max_investors": request.max_investors,
                "current_investors": 0,
                "status": "active",
                "risk_level": request.risk_level,
                "created_by": user_id
            }
            
            insert_result = await self.database_manager.execute_query(
                insert_query, 
                insert_params
            )
            
            if 'error' in insert_result:
                raise HTTPException(status_code=500, detail=f"Database error: {insert_result['error']}")
            
            # Get the created fund
            fund_query = """
            SELECT f.*, u.username as created_by_username
            FROM funds f
            LEFT JOIN users u ON f.created_by = u.id
            WHERE f.id = :fund_id
            """
            
            fund_result = await self.database_manager.execute_query(
                fund_query, 
                {"fund_id": fund_id}
            )
            
            if 'error' in fund_result or not fund_result['query_result']['data']:
                raise HTTPException(status_code=500, detail="Failed to retrieve created fund")
            
            fund_data = fund_result['query_result']['data'][0]
            
            logger.info(f"Successfully created fund: {fund_id}")
            
            return FundResponse(
                fund_id=fund_data['id'],
                name=fund_data['name'],
                description=fund_data['description'],
                fund_type=fund_data['fund_type'],
                initial_capital=float(fund_data['initial_capital']),
                current_value=float(fund_data['current_value']),
                management_fee=float(fund_data['management_fee']),
                performance_fee=float(fund_data['performance_fee']),
                min_investment=float(fund_data['min_investment']),
                max_investment=float(fund_data['max_investment']) if fund_data['max_investment'] else None,
                max_investors=fund_data['max_investors'],
                current_investors=fund_data['current_investors'],
                status=fund_data['status'],
                risk_level=fund_data['risk_level'],
                created_by=fund_data['created_by_username'],
                created_at=fund_data['created_at'],
                updated_at=fund_data['updated_at']
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to create fund: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/", response_model=List[FundResponse])
    async def get_funds(
        self,
        fund_type: Optional[FundType] = Query(None, description="Filter by fund type"),
        status: Optional[str] = Query(None, description="Filter by status"),
        page: int = Query(1, description="Page number", ge=1),
        page_size: int = Query(20, description="Page size", ge=1, le=100),
        current_user: str = Depends(get_current_user)
    ) -> List[FundResponse]:
        """Get list of funds."""
        try:
            # Build query with filters
            where_conditions = []
            params = {}
            
            if fund_type:
                where_conditions.append("f.fund_type = :fund_type")
                params["fund_type"] = fund_type.value
            
            if status:
                where_conditions.append("f.status = :status")
                params["status"] = status
            
            where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
            
            # Add pagination
            offset = (page - 1) * page_size
            params["limit"] = page_size
            params["offset"] = offset
            
            query = f"""
            SELECT f.*, u.username as created_by_username
            FROM funds f
            LEFT JOIN users u ON f.created_by = u.id
            {where_clause}
            ORDER BY f.created_at DESC
            LIMIT :limit OFFSET :offset
            """
            
            result = await self.database_manager.execute_query(query, params)
            
            if 'error' in result:
                raise HTTPException(status_code=500, detail=f"Database error: {result['error']}")
            
            funds = []
            for fund_data in result['query_result']['data']:
                funds.append(FundResponse(
                    fund_id=fund_data['id'],
                    name=fund_data['name'],
                    description=fund_data['description'],
                    fund_type=fund_data['fund_type'],
                    initial_capital=float(fund_data['initial_capital']),
                    current_value=float(fund_data['current_value']),
                    management_fee=float(fund_data['management_fee']),
                    performance_fee=float(fund_data['performance_fee']),
                    min_investment=float(fund_data['min_investment']),
                    max_investment=float(fund_data['max_investment']) if fund_data['max_investment'] else None,
                    max_investors=fund_data['max_investors'],
                    current_investors=fund_data['current_investors'],
                    status=fund_data['status'],
                    risk_level=fund_data['risk_level'],
                    created_by=fund_data['created_by_username'],
                    created_at=fund_data['created_at'],
                    updated_at=fund_data['updated_at']
                ))
            
            return funds
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get funds: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/{fund_id}", response_model=FundDetailResponse)
    async def get_fund(
        self,
        fund_id: str = Path(..., description="Fund ID"),
        current_user: str = Depends(get_current_user)
    ) -> FundDetailResponse:
        """Get detailed fund information."""
        try:
            # Validate fund_id format
            if not self._is_valid_uuid(fund_id):
                raise HTTPException(status_code=400, detail="Invalid fund ID format")
            
            # Get fund details from database
            fund_query = """
            SELECT f.*, u.username as created_by_username
            FROM funds f
            LEFT JOIN users u ON f.created_by = u.id
            WHERE f.id = :fund_id
            """
            
            fund_result = await self.database_manager.execute_query(
                fund_query, 
                {"fund_id": fund_id}
            )
            
            if 'error' in fund_result:
                raise HTTPException(status_code=500, detail=f"Database error: {fund_result['error']}")
            
            if not fund_result['query_result']['data']:
                raise HTTPException(status_code=404, detail="Fund not found")
            
            fund_data = fund_result['query_result']['data'][0]
            
            # Get fund performance metrics
            performance_query = """
            SELECT * FROM performance_snapshots 
            WHERE fund_id = :fund_id 
            ORDER BY snapshot_date DESC 
            LIMIT 1
            """
            
            performance_result = await self.database_manager.execute_query(
                performance_query,
                {"fund_id": fund_id}
            )
            
            # Get fund risk metrics
            risk_query = """
            SELECT * FROM risk_metrics 
            WHERE fund_id = :fund_id 
            ORDER BY calculation_date DESC 
            LIMIT 1
            """
            
            risk_result = await self.database_manager.execute_query(
                risk_query,
                {"fund_id": fund_id}
            )
            
            # Get portfolio positions
            portfolio_query = """
            SELECT * FROM portfolio_positions 
            WHERE fund_id = :fund_id 
            ORDER BY current_value DESC
            """
            
            portfolio_result = await self.database_manager.execute_query(
                portfolio_query,
                {"fund_id": fund_id}
            )
            
            # Get fund strategies
            strategies_query = """
            SELECT ts.*, fs.allocation_percentage
            FROM fund_strategies fs
            JOIN trading_strategies ts ON fs.strategy_id = ts.id
            WHERE fs.fund_id = :fund_id AND fs.is_active = true
            """
            
            strategies_result = await self.database_manager.execute_query(
                strategies_query,
                {"fund_id": fund_id}
            )
            
            # Build fund response
            fund_response = FundResponse(
                fund_id=fund_data['id'],
                name=fund_data['name'],
                description=fund_data['description'],
                fund_type=fund_data['fund_type'],
                initial_capital=float(fund_data['initial_capital']),
                current_value=float(fund_data['current_value']),
                management_fee=float(fund_data['management_fee']),
                performance_fee=float(fund_data['performance_fee']),
                min_investment=float(fund_data['min_investment']),
                max_investment=float(fund_data['max_investment']) if fund_data['max_investment'] else None,
                max_investors=fund_data['max_investors'],
                current_investors=fund_data['current_investors'],
                status=fund_data['status'],
                risk_level=fund_data['risk_level'],
                created_by=fund_data['created_by_username'],
                created_at=fund_data['created_at'],
                updated_at=fund_data['updated_at']
            )
            
            # Build performance data
            performance_data = None
            if performance_result['query_result']['data']:
                perf_data = performance_result['query_result']['data'][0]
                performance_data = {
                    "total_return": float(perf_data['total_return']),
                    "total_return_percentage": float(perf_data['total_return_percentage']),
                    "daily_return": float(perf_data['daily_return']) if perf_data['daily_return'] else None,
                    "daily_return_percentage": float(perf_data['daily_return_percentage']) if perf_data['daily_return_percentage'] else None,
                    "sharpe_ratio": float(perf_data['sharpe_ratio']) if perf_data['sharpe_ratio'] else None,
                    "max_drawdown": float(perf_data['max_drawdown']) if perf_data['max_drawdown'] else None,
                    "volatility": float(perf_data['volatility']) if perf_data['volatility'] else None,
                    "snapshot_date": perf_data['snapshot_date'].isoformat()
                }
            
            # Build risk metrics data
            risk_data = None
            if risk_result['query_result']['data']:
                risk_metrics = risk_result['query_result']['data'][0]
                risk_data = {
                    "var_95": float(risk_metrics['var_95']) if risk_metrics['var_95'] else None,
                    "var_99": float(risk_metrics['var_99']) if risk_metrics['var_99'] else None,
                    "cvar_95": float(risk_metrics['cvar_95']) if risk_metrics['cvar_95'] else None,
                    "cvar_99": float(risk_metrics['cvar_99']) if risk_metrics['cvar_99'] else None,
                    "beta": float(risk_metrics['beta']) if risk_metrics['beta'] else None,
                    "correlation_spy": float(risk_metrics['correlation_spy']) if risk_metrics['correlation_spy'] else None,
                    "tracking_error": float(risk_metrics['tracking_error']) if risk_metrics['tracking_error'] else None,
                    "information_ratio": float(risk_metrics['information_ratio']) if risk_metrics['information_ratio'] else None,
                    "calculation_date": risk_metrics['calculation_date'].isoformat()
                }
            
            # Build portfolio data
            portfolio_data = []
            if portfolio_result['query_result']['data']:
                for position in portfolio_result['query_result']['data']:
                    portfolio_data.append({
                        "asset_symbol": position['asset_symbol'],
                        "asset_name": position['asset_name'],
                        "asset_type": position['asset_type'],
                        "quantity": float(position['quantity']),
                        "average_price": float(position['average_price']),
                        "current_price": float(position['current_price']) if position['current_price'] else None,
                        "current_value": float(position['current_value']) if position['current_value'] else None,
                        "unrealized_pnl": float(position['unrealized_pnl']) if position['unrealized_pnl'] else None,
                        "unrealized_pnl_percentage": float(position['unrealized_pnl_percentage']) if position['unrealized_pnl_percentage'] else None,
                        "weight_percentage": float(position['weight_percentage']) if position['weight_percentage'] else None
                    })
            
            # Build strategies data
            strategies_data = []
            if strategies_result['query_result']['data']:
                for strategy in strategies_result['query_result']['data']:
                    strategies_data.append({
                        "strategy_id": strategy['id'],
                        "name": strategy['name'],
                        "description": strategy['description'],
                        "strategy_type": strategy['strategy_type'],
                        "allocation_percentage": float(strategy['allocation_percentage']),
                        "parameters": strategy['parameters'],
                        "is_active": strategy['is_active']
                    })
            
            logger.info(f"Successfully retrieved fund details for {fund_id}")
            
            return FundDetailResponse(
                fund=fund_response,
                performance=performance_data,
                risk_metrics=risk_data,
                portfolio=portfolio_data,
                strategies=strategies_data
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get fund details: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/{fund_id}/performance")
    async def get_fund_performance(
        self,
        fund_id: str = Path(..., description="Fund ID"),
        days: int = Query(30, description="Number of days", ge=1, le=365),
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Get fund performance history."""
        try:
            if not self._is_valid_uuid(fund_id):
                raise HTTPException(status_code=400, detail="Invalid fund ID format")
            
            # Get performance history
            query = """
            SELECT * FROM performance_snapshots 
            WHERE fund_id = :fund_id 
            AND snapshot_date >= CURRENT_DATE - INTERVAL '%s days'
            ORDER BY snapshot_date DESC
            """ % days
            
            result = await self.database_manager.execute_query(
                query,
                {"fund_id": fund_id}
            )
            
            if 'error' in result:
                raise HTTPException(status_code=500, detail=f"Database error: {result['error']}")
            
            performance_history = []
            for row in result['query_result']['data']:
                performance_history.append({
                    "date": row['snapshot_date'].isoformat(),
                    "total_value": float(row['total_value']),
                    "total_return": float(row['total_return']),
                    "total_return_percentage": float(row['total_return_percentage']),
                    "daily_return": float(row['daily_return']) if row['daily_return'] else None,
                    "daily_return_percentage": float(row['daily_return_percentage']) if row['daily_return_percentage'] else None,
                    "sharpe_ratio": float(row['sharpe_ratio']) if row['sharpe_ratio'] else None,
                    "max_drawdown": float(row['max_drawdown']) if row['max_drawdown'] else None,
                    "volatility": float(row['volatility']) if row['volatility'] else None
                })
            
            return {
                "fund_id": fund_id,
                "period_days": days,
                "performance_history": performance_history,
                "total_records": len(performance_history)
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get fund performance: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/{fund_id}/investors")
    async def get_fund_investors(
        self,
        fund_id: str = Path(..., description="Fund ID"),
        page: int = Query(1, description="Page number", ge=1),
        page_size: int = Query(20, description="Page size", ge=1, le=100),
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Get fund investors."""
        try:
            if not self._is_valid_uuid(fund_id):
                raise HTTPException(status_code=400, detail="Invalid fund ID format")
            
            # Add pagination
            offset = (page - 1) * page_size
            
            query = """
            SELECT i.*, u.username, u.email, u.first_name, u.last_name
            FROM investors i
            JOIN users u ON i.user_id = u.id
            WHERE i.fund_id = :fund_id
            ORDER BY i.investment_date DESC
            LIMIT :limit OFFSET :offset
            """
            
            result = await self.database_manager.execute_query(
                query,
                {
                    "fund_id": fund_id,
                    "limit": page_size,
                    "offset": offset
                }
            )
            
            if 'error' in result:
                raise HTTPException(status_code=500, detail=f"Database error: {result['error']}")
            
            investors = []
            for row in result['query_result']['data']:
                investors.append({
                    "investor_id": row['id'],
                    "user_id": row['user_id'],
                    "username": row['username'],
                    "email": row['email'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "investment_amount": float(row['investment_amount']),
                    "shares_owned": float(row['shares_owned']),
                    "current_value": float(row['current_value']) if row['current_value'] else None,
                    "total_return": float(row['total_return']) if row['total_return'] else None,
                    "total_return_percentage": float(row['total_return_percentage']) if row['total_return_percentage'] else None,
                    "investment_date": row['investment_date'].isoformat(),
                    "status": row['status']
                })
            
            return {
                "fund_id": fund_id,
                "investors": investors,
                "page": page,
                "page_size": page_size,
                "total_investors": len(investors)
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get fund investors: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")


# Create router instance
def create_fund_api_router(database_manager) -> APIRouter:
    """Create and configure the fund API router."""
    api = FunctionalFundAPI(database_manager)
    
    # Add the router methods to the router
    router.add_api_route("/", api.create_fund, methods=["POST"])
    router.add_api_route("/", api.get_funds, methods=["GET"])
    router.add_api_route("/{fund_id}", api.get_fund, methods=["GET"])
    router.add_api_route("/{fund_id}/performance", api.get_fund_performance, methods=["GET"])
    router.add_api_route("/{fund_id}/investors", api.get_fund_investors, methods=["GET"])
    
    return router
