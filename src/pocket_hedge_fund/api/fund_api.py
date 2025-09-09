"""
Fund Management API for Pocket Hedge Fund

This module provides RESTful API endpoints for fund management operations
including fund creation, investment management, portfolio operations,
and performance tracking.
"""

import asyncio
import logging
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from decimal import Decimal
import uuid

from fastapi import APIRouter, HTTPException, Depends, Query, Path
from fastapi import status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
from sqlalchemy import text

from ..database.connection import get_db_manager
from ..database.models import Fund, FundType, FundStatus, RiskLevel
from ..auth.auth_manager import get_auth_manager, AuthenticationManager

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# API Router
router = APIRouter(prefix="/api/v1/funds", tags=["Fund Management"])


# Pydantic Models
class FundCreateRequest(BaseModel):
    """Request model for fund creation."""
    name: str = Field(..., min_length=1, max_length=255, description="Fund name")
    description: Optional[str] = Field(None, description="Fund description")
    fund_type: str = Field(..., description="Fund type: mini, standard, or premium")
    initial_capital: float = Field(..., gt=0, description="Initial capital amount")
    management_fee: float = Field(..., ge=0, le=1, description="Management fee (0.02 = 2%)")
    performance_fee: float = Field(..., ge=0, le=1, description="Performance fee (0.20 = 20%)")
    min_investment: float = Field(..., gt=0, description="Minimum investment amount")
    max_investment: Optional[float] = Field(None, gt=0, description="Maximum investment amount")
    max_investors: Optional[int] = Field(None, gt=0, description="Maximum number of investors")
    risk_level: str = Field(default="medium", description="Risk level: low, medium, high, very_high")
    
    @validator('fund_type')
    def validate_fund_type(cls, v):
        if v not in ['mini', 'standard', 'premium']:
            raise ValueError('Fund type must be mini, standard, or premium')
        return v
    
    @validator('risk_level')
    def validate_risk_level(cls, v):
        if v not in ['low', 'medium', 'high', 'very_high']:
            raise ValueError('Risk level must be low, medium, high, or very_high')
        return v


class FundUpdateRequest(BaseModel):
    """Request model for fund updates."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    management_fee: Optional[float] = Field(None, ge=0, le=1)
    performance_fee: Optional[float] = Field(None, ge=0, le=1)
    min_investment: Optional[float] = Field(None, gt=0)
    max_investment: Optional[float] = Field(None, gt=0)
    max_investors: Optional[int] = Field(None, gt=0)
    risk_level: Optional[str] = None
    status: Optional[str] = None
    
    @validator('risk_level')
    def validate_risk_level(cls, v):
        if v is not None and v not in ['low', 'medium', 'high', 'very_high']:
            raise ValueError('Risk level must be low, medium, high, or very_high')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None and v not in ['active', 'paused', 'closed', 'liquidating']:
            raise ValueError('Status must be active, paused, closed, or liquidating')
        return v


class InvestmentRequest(BaseModel):
    """Request model for fund investment."""
    amount: float = Field(..., gt=0, description="Investment amount")
    notes: Optional[str] = Field(None, description="Investment notes")


class FundResponse(BaseModel):
    """Response model for fund data."""
    id: str
    name: str
    description: Optional[str]
    fund_type: str
    initial_capital: float
    current_value: float
    total_return: float
    total_return_percentage: float
    management_fee: float
    performance_fee: float
    min_investment: float
    max_investment: Optional[float]
    max_investors: Optional[int]
    current_investors: int
    status: str
    risk_level: str
    is_open_for_investment: bool
    created_by: str
    created_at: str
    updated_at: str


class InvestmentResponse(BaseModel):
    """Response model for investment data."""
    id: str
    user_id: str
    fund_id: str
    investment_amount: float
    shares_owned: float
    investment_date: str
    current_value: Optional[float]
    total_return: Optional[float]
    total_return_percentage: Optional[float]
    unrealized_pnl: float
    unrealized_pnl_percentage: float
    status: str


class PerformanceResponse(BaseModel):
    """Response model for fund performance."""
    fund_id: str
    snapshot_date: str
    total_value: float
    total_return: float
    total_return_percentage: float
    daily_return: Optional[float]
    daily_return_percentage: Optional[float]
    sharpe_ratio: Optional[float]
    max_drawdown: Optional[float]
    volatility: Optional[float]


# Dependency functions
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user."""
    auth_manager = await get_auth_manager()
    
    success, message, user_data = await auth_manager.verify_token(credentials.credentials)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_data


async def require_role(required_role: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Require specific user role."""
    if current_user['role'] != required_role and current_user['role'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Requires {required_role} role"
        )
    return current_user


# API Endpoints

@router.post("/", response_model=FundResponse, status_code=status.HTTP_201_CREATED)
async def create_fund(
    fund_data: FundCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new fund."""
    try:
        # Check if user has fund_manager role
        if current_user['role'] != 'fund_manager' and current_user['role'] != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Requires fund_manager role"
            )
        
        db_manager = await get_db_manager()
        
        # Validate fund type constraints
        if fund_data.fund_type == "mini":
            if fund_data.initial_capital < 10000 or fund_data.initial_capital > 100000:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Mini fund initial capital must be between $10,000 and $100,000"
                )
        elif fund_data.fund_type == "standard":
            if fund_data.initial_capital < 100000 or fund_data.initial_capital > 1000000:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Standard fund initial capital must be between $100,000 and $1,000,000"
                )
        elif fund_data.fund_type == "premium":
            if fund_data.initial_capital < 1000000:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Premium fund initial capital must be at least $1,000,000"
                )
        
        # Create fund
        fund_id = str(uuid.uuid4())
        create_fund_query = """
            INSERT INTO funds (
                id, name, description, fund_type, initial_capital, current_value,
                management_fee, performance_fee, min_investment, max_investment,
                max_investors, current_investors, status, risk_level, created_by,
                created_at, updated_at
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17
            )
        """
        
        now = datetime.utcnow()
        await db_manager.execute_command(
            create_fund_query,
            {
                'fund_id': fund_id,
                    'name': fund_data.name,
                    'description': fund_data.description,
                'fund_type': fund_data.fund_type,
                'initial_capital': fund_data.initial_capital,
                'current_value': fund_data.initial_capital,  # Start with initial capital
                'management_fee': fund_data.management_fee,
                'performance_fee': fund_data.performance_fee,
                'min_investment': fund_data.min_investment,
                'max_investment': fund_data.max_investment,
                'max_investors': fund_data.max_investors,
                'current_investors': 0,
                    'status': 'active',
                'risk_level': fund_data.risk_level,
                'created_by': current_user['id'],
                'created_at': now,
                'updated_at': now
            }
        )
        
        # Get created fund
        fund_query = """
            SELECT * FROM funds WHERE id = $1
        """
        funds = await db_manager.execute_query(fund_query, {'fund_id': fund_id})
        
        if not funds:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve created fund"
            )
        
        fund_data = funds[0]
        
        # Create Fund model instance to get computed properties
        from ..database.models import Fund
        fund = Fund(
            id=fund_data['id'],
            name=fund_data['name'],
            description=fund_data['description'],
            fund_type=fund_data['fund_type'],
            initial_capital=fund_data['initial_capital'],
            current_value=fund_data['current_value'],
            management_fee=fund_data['management_fee'],
            performance_fee=fund_data['performance_fee'],
            min_investment=fund_data['min_investment'],
            max_investment=fund_data['max_investment'],
            max_investors=fund_data['max_investors'],
            current_investors=fund_data['current_investors'],
            status=fund_data['status'],
            risk_level=fund_data['risk_level'],
            created_by=fund_data['created_by'],
            created_at=fund_data['created_at'],
            updated_at=fund_data['updated_at']
        )
        
        # Log fund creation
        auth_manager = await get_auth_manager()
        await auth_manager._log_audit_event(
            user_id=current_user['id'],
            action="fund_created",
            resource_type="fund",
            resource_id=fund_id,
            new_values=str(fund_data)
        )
        
        return FundResponse(**fund.to_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fund creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fund creation failed: {str(e)}"
        )


@router.get("/", response_model=List[FundResponse])
async def list_funds(
    fund_type: Optional[str] = Query(None, description="Filter by fund type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level"),
    limit: int = Query(50, ge=1, le=100, description="Number of funds to return"),
    offset: int = Query(0, ge=0, description="Number of funds to skip"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """List funds with optional filtering."""
    try:
        db_manager = await get_db_manager()
        
        # Build query with filters
        where_conditions = []
        params = []
        
        if fund_type:
            where_conditions.append("fund_type = $1")
            params.append(fund_type)
        
        if status:
            where_conditions.append("status = $2")
            params.append(status)
        
        if risk_level:
            where_conditions.append("risk_level = $3")
            params.append(risk_level)
        
        where_clause = ""
        if where_conditions:
            where_clause = "WHERE " + " AND ".join(where_conditions)
        
        # Add limit and offset parameters
        limit_param = len(params) + 1
        offset_param = len(params) + 2
        params.extend([limit, offset])
        
        query = f"""
            SELECT * FROM funds {where_clause}
            ORDER BY created_at DESC
            LIMIT ${limit_param} OFFSET ${offset_param}
        """
        
        funds = await db_manager.execute_query(query, params)
        
        # Convert to Fund models and then to response
        from ..database.models import Fund
        fund_models = []
        for fund_data in funds:
            fund = Fund(
                id=fund_data['id'],
                name=fund_data['name'],
                description=fund_data['description'],
                fund_type=fund_data['fund_type'],
                initial_capital=fund_data['initial_capital'],
                current_value=fund_data['current_value'],
                management_fee=fund_data['management_fee'],
                performance_fee=fund_data['performance_fee'],
                min_investment=fund_data['min_investment'],
                max_investment=fund_data['max_investment'],
                max_investors=fund_data['max_investors'],
                current_investors=fund_data['current_investors'],
                status=fund_data['status'],
                risk_level=fund_data['risk_level'],
                created_by=fund_data['created_by'],
                created_at=fund_data['created_at'],
                updated_at=fund_data['updated_at']
            )
            fund_models.append(fund)
        
        return [FundResponse(**fund.to_dict()) for fund in fund_models]
        
    except Exception as e:
        logger.error(f"Failed to list funds: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list funds: {str(e)}"
        )


@router.get("/{fund_id}", response_model=FundResponse)
async def get_fund(
    fund_id: str = Path(..., description="Fund ID"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get fund by ID."""
    try:
        db_manager = await get_db_manager()
        
        fund_query = "SELECT * FROM funds WHERE id = $1"
        funds = await db_manager.execute_query(fund_query, {'fund_id': fund_id})
        
        if not funds:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Fund not found"
                )
            
        return FundResponse(**funds[0])
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get fund: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get fund: {str(e)}"
        )


@router.put("/{fund_id}", response_model=FundResponse)
async def update_fund(
    fund_id: str = Path(..., description="Fund ID"),
    fund_data: FundUpdateRequest = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update fund."""
    try:
        db_manager = await get_db_manager()
        
        # Check if fund exists
        fund_query = "SELECT * FROM funds WHERE id = $1"
        funds = await db_manager.execute_query(fund_query, {'fund_id': fund_id})
        
        if not funds:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Fund not found"
                )
            
        # Check if user has permission to update this fund
        fund = funds[0]
        if fund['created_by'] != current_user['id'] and current_user['role'] != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this fund"
            )
        
        # Build update query
        update_fields = []
        params = {'fund_id': fund_id, 'updated_at': datetime.utcnow()}
        
        for field, value in fund_data.dict(exclude_unset=True).items():
            if value is not None:
                update_fields.append(f"{field} = ${field}")
                params[field] = value
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
                )
            
            update_query = f"""
            UPDATE funds SET {', '.join(update_fields)}, updated_at = $updated_at
            WHERE id = $fund_id
            """
            
        await db_manager.execute_command(update_query, params)
            
            # Get updated fund
        updated_funds = await db_manager.execute_query(fund_query, {'fund_id': fund_id})
        
        # Log fund update
        auth_manager = await get_auth_manager()
        await auth_manager._log_audit_event(
            user_id=current_user['id'],
            action="fund_updated",
            resource_type="fund",
            resource_id=fund_id,
            old_values=fund,
            new_values=updated_funds[0]
        )
        
        return FundResponse(**updated_funds[0])
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fund update failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fund update failed: {str(e)}"
        )


@router.post("/{fund_id}/invest", response_model=InvestmentResponse, status_code=status.HTTP_201_CREATED)
async def invest_in_fund(
    fund_id: str = Path(..., description="Fund ID"),
    investment_data: InvestmentRequest = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Invest in a fund."""
    try:
        db_manager = await get_db_manager()
        
        # Get fund details
        fund_query = "SELECT * FROM funds WHERE id = $1"
        funds = await db_manager.execute_query(fund_query, {'fund_id': fund_id})
        
        if not funds:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fund not found"
            )
        
        fund = funds[0]
        
        # Check if fund is open for investment
        if fund['status'] != 'active':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Fund is not open for investment"
            )
        
        # Check minimum investment
        if investment_data.amount < fund['min_investment']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Investment amount must be at least ${fund['min_investment']}"
            )
        
        # Check maximum investment
        if fund['max_investment'] and investment_data.amount > fund['max_investment']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Investment amount cannot exceed ${fund['max_investment']}"
            )
        
        # Check maximum investors
        if fund['max_investors'] and fund['current_investors'] >= fund['max_investors']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Fund has reached maximum number of investors"
            )
        
        # Check if user already invested in this fund
        existing_investment_query = """
            SELECT id FROM investors WHERE user_id = $1 AND fund_id = $2
        """
        existing_investments = await db_manager.execute_query(
            existing_investment_query,
            {'user_id': current_user['id'], 'fund_id': fund_id}
        )
        
        if existing_investments:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already invested in this fund"
            )
        
        # Calculate shares (simplified: 1 share = $1)
        shares_owned = investment_data.amount
        
        # Create investment
        investment_id = str(uuid.uuid4())
        create_investment_query = """
            INSERT INTO investors (
                id, user_id, fund_id, investment_amount, shares_owned,
                investment_date, current_value, total_return, total_return_percentage,
                status, created_at, updated_at
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12
            )
        """
        
        now = datetime.utcnow()
        await db_manager.execute_command(
            create_investment_query,
            {
                'investment_id': investment_id,
                'user_id': current_user['id'],
                'fund_id': fund_id,
                'investment_amount': investment_data.amount,
                'shares_owned': shares_owned,
                'investment_date': now,
                'current_value': investment_data.amount,  # Start with investment amount
                'total_return': 0,
                'total_return_percentage': 0,
                'status': 'active',
                'created_at': now,
                'updated_at': now
            }
        )
        
        # Update fund investor count
        update_fund_query = """
            UPDATE funds SET current_investors = current_investors + 1, updated_at = $1
            WHERE id = $2
        """
        await db_manager.execute_command(
            update_fund_query,
            {'updated_at': now, 'fund_id': fund_id}
        )
        
        # Get created investment
        investment_query = "SELECT * FROM investors WHERE id = $1"
        investments = await db_manager.execute_query(
            investment_query,
            {'investment_id': investment_id}
        )
        
        # Log investment
        auth_manager = await get_auth_manager()
        await auth_manager._log_audit_event(
            user_id=current_user['id'],
            action="fund_investment",
            resource_type="investment",
            resource_id=investment_id,
            new_values={
                'fund_id': fund_id,
                'amount': investment_data.amount,
                'shares': shares_owned
            }
        )
        
        return InvestmentResponse(**investments[0])
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Investment failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Investment failed: {str(e)}"
        )


@router.get("/{fund_id}/performance", response_model=List[PerformanceResponse])
async def get_fund_performance(
    fund_id: str = Path(..., description="Fund ID"),
    days: int = Query(30, ge=1, le=365, description="Number of days to retrieve"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get fund performance history."""
    try:
        db_manager = await get_db_manager()
        
        # Check if fund exists
        fund_query = "SELECT id FROM funds WHERE id = $1"
        funds = await db_manager.execute_query(fund_query, {'fund_id': fund_id})
        
        if not funds:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fund not found"
            )
        
        # Get performance data
        performance_query = """
            SELECT * FROM performance_snapshots
            WHERE fund_id = $1
            ORDER BY snapshot_date DESC
            LIMIT $2
        """
        
        performance_data = await db_manager.execute_query(
            performance_query,
            {'fund_id': fund_id, 'days': days}
        )
        
        return [PerformanceResponse(**perf) for perf in performance_data]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get fund performance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get fund performance: {str(e)}"
        )


@router.get("/{fund_id}/investors", response_model=List[InvestmentResponse])
async def get_fund_investors(
    fund_id: str = Path(..., description="Fund ID"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get fund investors (fund managers only)."""
    try:
        db_manager = await get_db_manager()
        
        # Check if fund exists and user has permission
        fund_query = "SELECT created_by FROM funds WHERE id = $1"
        funds = await db_manager.execute_query(fund_query, {'fund_id': fund_id})
        
        if not funds:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Fund not found"
                )
            
        fund = funds[0]
        if fund['created_by'] != current_user['id'] and current_user['role'] != 'admin':
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to view this fund's investors"
            )
        
        # Get investors
        investors_query = """
            SELECT * FROM investors WHERE fund_id = $1 ORDER BY investment_date DESC
        """
        investors = await db_manager.execute_query(
            investors_query,
            {'fund_id': fund_id}
        )
        
        return [InvestmentResponse(**investor) for investor in investors]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get fund investors: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get fund investors: {str(e)}"
        )