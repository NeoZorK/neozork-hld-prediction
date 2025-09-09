"""
Investment Management API for Pocket Hedge Fund

This module provides RESTful API endpoints for investment operations
including creating investments, managing portfolios, and tracking returns.
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
from ..auth.auth_manager import get_auth_manager, get_current_user

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/investments", tags=["investments"])

# Security
security = HTTPBearer()

# Pydantic models for request/response
class InvestmentCreateRequest(BaseModel):
    """Request model for creating an investment."""
    fund_id: str = Field(..., description="ID of the fund to invest in")
    amount: float = Field(..., gt=0, description="Investment amount")
    investment_type: str = Field(default="lump_sum", description="Type of investment")
    
    @validator('investment_type')
    def validate_investment_type(cls, v):
        allowed_types = ['lump_sum', 'dca', 'recurring']
        if v not in allowed_types:
            raise ValueError(f'Investment type must be one of: {allowed_types}')
        return v

class InvestmentResponse(BaseModel):
    """Response model for investment data."""
    id: str
    investor_id: str
    fund_id: str
    amount: float
    investment_type: str
    status: str
    shares_acquired: float
    share_price: float
    total_return: float
    total_return_percentage: float
    current_value: float
    created_at: str
    updated_at: str

class PortfolioResponse(BaseModel):
    """Response model for portfolio data."""
    investor_id: str
    total_invested: float
    total_current_value: float
    total_return: float
    total_return_percentage: float
    investments: List[InvestmentResponse]
    created_at: str
    updated_at: str

class InvestmentUpdateRequest(BaseModel):
    """Request model for updating an investment."""
    amount: Optional[float] = Field(None, gt=0, description="New investment amount")
    status: Optional[str] = Field(None, description="Investment status")
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = ['active', 'paused', 'cancelled', 'completed']
            if v not in allowed_statuses:
                raise ValueError(f'Status must be one of: {allowed_statuses}')
        return v

# Investment API endpoints

@router.post("/", response_model=InvestmentResponse, status_code=status.HTTP_201_CREATED)
async def create_investment(
    investment_data: InvestmentCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new investment."""
    try:
        # Check if user has investor role
        if current_user['role'] not in ['investor', 'admin']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Requires investor role"
            )
        
        db_manager = await get_db_manager()
        
        # Validate fund exists and is open for investment
        fund_query = """
            SELECT * FROM funds WHERE id = $1
        """
        funds = await db_manager.execute_query(fund_query, {'1': investment_data.fund_id})
        
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
        
        # Check minimum investment amount
        if investment_data.amount < fund['min_investment']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Investment amount must be at least ${fund['min_investment']}"
            )
        
        # Check maximum investment amount if specified
        if fund['max_investment'] and investment_data.amount > fund['max_investment']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Investment amount cannot exceed ${fund['max_investment']}"
            )
        
        # Calculate share price and shares acquired
        from decimal import Decimal
        share_price = float(fund['current_value']) / float(fund['initial_capital']) if fund['initial_capital'] > 0 else 1.0
        shares_acquired = float(investment_data.amount) / share_price
        
        # Create investment
        investment_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        investment_query = """
            INSERT INTO investments (
                id, investor_id, fund_id, amount, investment_type, status,
                shares_acquired, share_price, created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        """
        
        await db_manager.execute_command(
            investment_query,
            {
                '1': investment_id,
                '2': current_user['id'],
                '3': investment_data.fund_id,
                '4': investment_data.amount,
                '5': investment_data.investment_type,
                '6': 'active',
                '7': shares_acquired,
                '8': share_price,
                '9': now,
                '10': now
            }
        )
        
        # Update fund current investors count
        update_fund_query = """
            UPDATE funds SET current_investors = current_investors + 1,
                           current_value = current_value + $1,
                           updated_at = $2
            WHERE id = $3
        """
        
        await db_manager.execute_command(
            update_fund_query,
            {
                '1': investment_data.amount,
                '2': now,
                '3': investment_data.fund_id
            }
        )
        
        # Get created investment
        investment_query = """
            SELECT * FROM investments WHERE id = $1
        """
        investments = await db_manager.execute_query(investment_query, {'1': investment_id})
        
        if not investments:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve created investment"
            )
        
        investment_data = investments[0]
        
        # Create Investment model instance
        from ..database.models import Investment
        investment = Investment(
            id=investment_data['id'],
            investor_id=investment_data['investor_id'],
            fund_id=investment_data['fund_id'],
            amount=investment_data['amount'],
            investment_type=investment_data['investment_type'],
            status=investment_data['status'],
            shares_acquired=investment_data['shares_acquired'],
            share_price=investment_data['share_price'],
            created_at=investment_data['created_at'],
            updated_at=investment_data['updated_at']
        )
        
        # Log investment creation
        auth_manager = await get_auth_manager()
        await auth_manager._log_audit_event(
            user_id=current_user['id'],
            action="investment_created",
            resource_type="investment",
            resource_id=investment_id,
            new_values=str(investment_data)
        )
        
        return InvestmentResponse(**investment.to_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Investment creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Investment creation failed: {str(e)}"
        )

@router.get("/", response_model=List[InvestmentResponse])
async def list_investments(
    fund_id: Optional[str] = Query(None, description="Filter by fund ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=100, description="Number of investments to return"),
    offset: int = Query(0, ge=0, description="Number of investments to skip"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """List investments for the current user."""
    try:
        db_manager = await get_db_manager()
        
        # Build query with filters
        where_conditions = ["investor_id = $1"]
        params = [current_user['id']]
        
        if fund_id:
            where_conditions.append("fund_id = $2")
            params.append(fund_id)
        
        if status:
            where_conditions.append("status = $3")
            params.append(status)
        
        where_clause = "WHERE " + " AND ".join(where_conditions)
        
        # Add limit and offset parameters
        limit_param = len(params) + 1
        offset_param = len(params) + 2
        params.extend([limit, offset])
        
        query = f"""
            SELECT * FROM investments {where_clause}
            ORDER BY created_at DESC
            LIMIT ${limit_param} OFFSET ${offset_param}
        """
        
        investments = await db_manager.execute_query(query, dict(enumerate(params, 1)))
        
        # Convert to Investment models and then to response
        from ..database.models import Investment
        investment_models = []
        for investment_data in investments:
            investment = Investment(
                id=investment_data['id'],
                investor_id=investment_data['investor_id'],
                fund_id=investment_data['fund_id'],
                amount=investment_data['amount'],
                investment_type=investment_data['investment_type'],
                status=investment_data['status'],
                shares_acquired=investment_data['shares_acquired'],
                share_price=investment_data['share_price'],
                created_at=investment_data['created_at'],
                updated_at=investment_data['updated_at']
            )
            investment_models.append(investment)
        
        return [InvestmentResponse(**investment.to_dict()) for investment in investment_models]
        
    except Exception as e:
        logger.error(f"Failed to list investments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list investments: {str(e)}"
        )

@router.get("/{investment_id}", response_model=InvestmentResponse)
async def get_investment(
    investment_id: str = Path(..., description="Investment ID"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get investment details."""
    try:
        db_manager = await get_db_manager()
        
        query = """
            SELECT * FROM investments WHERE id = $1 AND investor_id = $2
        """
        investments = await db_manager.execute_query(query, {'1': investment_id, '2': current_user['id']})
        
        if not investments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Investment not found"
            )
        
        investment_data = investments[0]
        
        # Create Investment model instance
        from ..database.models import Investment
        investment = Investment(
            id=investment_data['id'],
            investor_id=investment_data['investor_id'],
            fund_id=investment_data['fund_id'],
            amount=investment_data['amount'],
            investment_type=investment_data['investment_type'],
            status=investment_data['status'],
            shares_acquired=investment_data['shares_acquired'],
            share_price=investment_data['share_price'],
            created_at=investment_data['created_at'],
            updated_at=investment_data['updated_at']
        )
        
        return InvestmentResponse(**investment.to_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get investment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get investment: {str(e)}"
        )

@router.put("/{investment_id}", response_model=InvestmentResponse)
async def update_investment(
    investment_id: str = Path(..., description="Investment ID"),
    investment_data: InvestmentUpdateRequest = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update investment."""
    try:
        db_manager = await get_db_manager()
        
        # Check if investment exists and belongs to user
        query = """
            SELECT * FROM investments WHERE id = $1 AND investor_id = $2
        """
        investments = await db_manager.execute_query(query, {'1': investment_id, '2': current_user['id']})
        
        if not investments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Investment not found"
            )
        
        # Build update query
        update_fields = []
        params = {'investment_id': investment_id, 'updated_at': datetime.utcnow()}
        
        for field, value in investment_data.dict(exclude_unset=True).items():
            if value is not None:
                update_fields.append(f"{field} = ${field}")
                params[field] = value
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        update_query = f"""
            UPDATE investments SET {', '.join(update_fields)}, updated_at = $updated_at
            WHERE id = $investment_id
        """
        
        await db_manager.execute_command(update_query, params)
        
        # Get updated investment
        updated_query = """
            SELECT * FROM investments WHERE id = $1
        """
        updated_investments = await db_manager.execute_query(updated_query, {'1': investment_id})
        
        if not updated_investments:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve updated investment"
            )
        
        investment_data = updated_investments[0]
        
        # Create Investment model instance
        from ..database.models import Investment
        investment = Investment(
            id=investment_data['id'],
            investor_id=investment_data['investor_id'],
            fund_id=investment_data['fund_id'],
            amount=investment_data['amount'],
            investment_type=investment_data['investment_type'],
            status=investment_data['status'],
            shares_acquired=investment_data['shares_acquired'],
            share_price=investment_data['share_price'],
            created_at=investment_data['created_at'],
            updated_at=investment_data['updated_at']
        )
        
        return InvestmentResponse(**investment.to_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update investment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update investment: {str(e)}"
        )

@router.delete("/{investment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_investment(
    investment_id: str = Path(..., description="Investment ID"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete investment (soft delete by setting status to cancelled)."""
    try:
        db_manager = await get_db_manager()
        
        # Check if investment exists and belongs to user
        query = """
            SELECT * FROM investments WHERE id = $1 AND investor_id = $2
        """
        investments = await db_manager.execute_query(query, {'1': investment_id, '2': current_user['id']})
        
        if not investments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Investment not found"
            )
        
        # Soft delete by setting status to cancelled
        update_query = """
            UPDATE investments SET status = 'cancelled', updated_at = $1
            WHERE id = $2
        """
        
        await db_manager.execute_command(update_query, {'1': datetime.utcnow(), '2': investment_id})
        
        # Log investment cancellation
        auth_manager = await get_auth_manager()
        await auth_manager._log_audit_event(
            user_id=current_user['id'],
            action="investment_cancelled",
            resource_type="investment",
            resource_id=investment_id,
            new_values="status: cancelled"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete investment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete investment: {str(e)}"
        )
