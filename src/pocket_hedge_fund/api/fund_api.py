"""
Fund API for Pocket Hedge Fund.

This module provides REST API endpoints for fund management operations
including fund creation, updates, and retrieval.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, validator

from ..database import DatabaseManager, DatabaseUtils
from ..auth.middleware import get_current_user, require_fund_manager

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Create router
router = APIRouter(prefix="/funds", tags=["Fund Management"])


# Pydantic models

class FundCreate(BaseModel):
    """Fund creation request model."""
    name: str
    description: Optional[str] = None
    initial_capital: Decimal = Decimal('0.00')
    management_fee_rate: Decimal = Decimal('0.0200')  # 2%
    performance_fee_rate: Decimal = Decimal('0.2000')  # 20%
    max_drawdown_limit: Decimal = Decimal('0.1000')  # 10%
    max_position_size: Decimal = Decimal('0.1000')  # 10%
    max_leverage: Decimal = Decimal('1.0000')  # 1x
    
    @validator('name')
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError('Fund name must be at least 3 characters long')
        return v
    
    @validator('management_fee_rate', 'performance_fee_rate', 'max_drawdown_limit', 'max_position_size', 'max_leverage')
    def validate_percentages(cls, v):
        if not (0 <= v <= 1):
            raise ValueError('Rate must be between 0 and 1')
        return v


class FundUpdate(BaseModel):
    """Fund update request model."""
    name: Optional[str] = None
    description: Optional[str] = None
    management_fee_rate: Optional[Decimal] = None
    performance_fee_rate: Optional[Decimal] = None
    max_drawdown_limit: Optional[Decimal] = None
    max_position_size: Optional[Decimal] = None
    max_leverage: Optional[Decimal] = None
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None and len(v) < 3:
            raise ValueError('Fund name must be at least 3 characters long')
        return v
    
    @validator('management_fee_rate', 'performance_fee_rate', 'max_drawdown_limit', 'max_position_size', 'max_leverage')
    def validate_percentages(cls, v):
        if v is not None and not (0 <= v <= 1):
            raise ValueError('Rate must be between 0 and 1')
        return v


class FundResponse(BaseModel):
    """Fund response model."""
    id: str
    name: str
    description: Optional[str]
    manager_id: str
    status: str
    initial_capital: Decimal
    current_capital: Decimal
    management_fee_rate: Decimal
    performance_fee_rate: Decimal
    max_drawdown_limit: Decimal
    max_position_size: Decimal
    max_leverage: Decimal
    created_at: datetime
    updated_at: datetime
    launched_at: Optional[datetime]
    closed_at: Optional[datetime]


class FundSummary(BaseModel):
    """Fund summary model."""
    fund: FundResponse
    portfolio: Dict[str, Any]
    performance: Optional[Dict[str, Any]]


# API endpoints

@router.post("/", response_model=FundResponse, status_code=status.HTTP_201_CREATED)
async def create_fund(
    fund_data: FundCreate,
    request: Request,
    current_user: Dict[str, Any] = Depends(require_fund_manager)
) -> FundResponse:
    """
    Create a new fund.
    
    Args:
        fund_data: Fund creation data
        request: HTTP request
        current_user: Current authenticated user
        
    Returns:
        Created fund information
        
    Raises:
        HTTPException: If fund creation fails
    """
    try:
        # Get database manager from app state
        db_manager: DatabaseManager = request.app.state.db_manager
        
        # Check if fund name already exists
        async with db_manager.get_async_session() as session:
            from sqlalchemy import text
            result = await session.execute(
                text("SELECT 1 FROM funds WHERE name = :name"),
                {"name": fund_data.name}
            )
            if result.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Fund with this name already exists"
                )
        
        # Create fund
        import uuid
        fund_id = str(uuid.uuid4())
        
        async with db_manager.get_async_session() as session:
            await session.execute(
                text("""
                    INSERT INTO funds (
                        id, name, description, manager_id, status, initial_capital, current_capital,
                        management_fee_rate, performance_fee_rate, max_drawdown_limit,
                        max_position_size, max_leverage, created_at, updated_at
                    ) VALUES (
                        :id, :name, :description, :manager_id, :status, :initial_capital, :current_capital,
                        :management_fee_rate, :performance_fee_rate, :max_drawdown_limit,
                        :max_position_size, :max_leverage, :created_at, :updated_at
                    )
                """),
                {
                    'id': fund_id,
                    'name': fund_data.name,
                    'description': fund_data.description,
                    'manager_id': current_user['id'],
                    'status': 'active',
                    'initial_capital': fund_data.initial_capital,
                    'current_capital': fund_data.initial_capital,
                    'management_fee_rate': fund_data.management_fee_rate,
                    'performance_fee_rate': fund_data.performance_fee_rate,
                    'max_drawdown_limit': fund_data.max_drawdown_limit,
                    'max_position_size': fund_data.max_position_size,
                    'max_leverage': fund_data.max_leverage,
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
            )
            await session.commit()
        
        logger.info(f"Fund created successfully: {fund_data.name} by user {current_user['id']}")
        
        # Return created fund
        return FundResponse(
            id=fund_id,
            name=fund_data.name,
            description=fund_data.description,
            manager_id=current_user['id'],
            status='active',
            initial_capital=fund_data.initial_capital,
            current_capital=fund_data.initial_capital,
            management_fee_rate=fund_data.management_fee_rate,
            performance_fee_rate=fund_data.performance_fee_rate,
            max_drawdown_limit=fund_data.max_drawdown_limit,
            max_position_size=fund_data.max_position_size,
            max_leverage=fund_data.max_leverage,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            launched_at=None,
            closed_at=None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating fund: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fund creation failed"
        )


@router.get("/", response_model=List[FundResponse])
async def list_funds(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
) -> List[FundResponse]:
    """
    List funds accessible to the current user.
    
    Args:
        request: HTTP request
        current_user: Current authenticated user
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of funds
        
    Raises:
        HTTPException: If fund listing fails
    """
    try:
        # Get database manager from app state
        db_manager: DatabaseManager = request.app.state.db_manager
        db_utils = DatabaseUtils(db_manager)
        
        # Get user funds
        funds_data = await db_utils.get_user_funds(current_user['id'])
        
        # Convert to response models
        funds = []
        for fund_data in funds_data[skip:skip+limit]:
            funds.append(FundResponse(
                id=fund_data['id'],
                name=fund_data['name'],
                description=fund_data.get('description'),
                manager_id=fund_data['manager_id'],
                status=fund_data['status'],
                initial_capital=fund_data['initial_capital'],
                current_capital=fund_data['current_capital'],
                management_fee_rate=fund_data['management_fee_rate'],
                performance_fee_rate=fund_data['performance_fee_rate'],
                max_drawdown_limit=fund_data['max_drawdown_limit'],
                max_position_size=fund_data['max_position_size'],
                max_leverage=fund_data['max_leverage'],
                created_at=fund_data['created_at'],
                updated_at=fund_data['updated_at'],
                launched_at=fund_data.get('launched_at'),
                closed_at=fund_data.get('closed_at')
            ))
        
        return funds
        
    except Exception as e:
        logger.error(f"Error listing funds: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list funds"
        )


@router.get("/{fund_id}", response_model=FundResponse)
async def get_fund(
    fund_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> FundResponse:
    """
    Get fund by ID.
    
    Args:
        fund_id: Fund ID
        request: HTTP request
        current_user: Current authenticated user
        
    Returns:
        Fund information
        
    Raises:
        HTTPException: If fund not found or access denied
    """
    try:
        # Get database manager from app state
        db_manager: DatabaseManager = request.app.state.db_manager
        
        async with db_manager.get_async_session() as session:
            from sqlalchemy import text
            result = await session.execute(
                text("SELECT * FROM funds WHERE id = :fund_id"),
                {"fund_id": fund_id}
            )
            fund_data = result.fetchone()
            
            if not fund_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Fund not found"
                )
            
            # Check access permissions
            if (current_user['role'] not in ['admin', 'fund_manager'] and 
                fund_data.manager_id != current_user['id']):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            
            return FundResponse(
                id=fund_data.id,
                name=fund_data.name,
                description=fund_data.description,
                manager_id=fund_data.manager_id,
                status=fund_data.status,
                initial_capital=fund_data.initial_capital,
                current_capital=fund_data.current_capital,
                management_fee_rate=fund_data.management_fee_rate,
                performance_fee_rate=fund_data.performance_fee_rate,
                max_drawdown_limit=fund_data.max_drawdown_limit,
                max_position_size=fund_data.max_position_size,
                max_leverage=fund_data.max_leverage,
                created_at=fund_data.created_at,
                updated_at=fund_data.updated_at,
                launched_at=fund_data.launched_at,
                closed_at=fund_data.closed_at
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting fund: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get fund"
        )


@router.put("/{fund_id}", response_model=FundResponse)
async def update_fund(
    fund_id: str,
    fund_data: FundUpdate,
    request: Request,
    current_user: Dict[str, Any] = Depends(require_fund_manager)
) -> FundResponse:
    """
    Update fund information.
    
    Args:
        fund_id: Fund ID
        fund_data: Fund update data
        request: HTTP request
        current_user: Current authenticated user
        
    Returns:
        Updated fund information
        
    Raises:
        HTTPException: If fund update fails
    """
    try:
        # Get database manager from app state
        db_manager: DatabaseManager = request.app.state.db_manager
        
        # Check if fund exists and user has access
        async with db_manager.get_async_session() as session:
            from sqlalchemy import text
            result = await session.execute(
                text("SELECT * FROM funds WHERE id = :fund_id"),
                {"fund_id": fund_id}
            )
            fund = result.fetchone()
            
            if not fund:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Fund not found"
                )
            
            # Check if user is fund manager or admin
            if (current_user['role'] != 'admin' and 
                fund.manager_id != current_user['id']):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            
            # Build update query
            update_fields = []
            update_values = {'fund_id': fund_id, 'updated_at': datetime.utcnow()}
            
            for field, value in fund_data.dict(exclude_unset=True).items():
                if value is not None:
                    update_fields.append(f"{field} = :{field}")
                    update_values[field] = value
            
            if not update_fields:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No fields to update"
                )
            
            # Execute update
            update_query = f"""
                UPDATE funds 
                SET {', '.join(update_fields)}, updated_at = :updated_at
                WHERE id = :fund_id
            """
            
            await session.execute(text(update_query), update_values)
            await session.commit()
            
            # Get updated fund
            result = await session.execute(
                text("SELECT * FROM funds WHERE id = :fund_id"),
                {"fund_id": fund_id}
            )
            updated_fund = result.fetchone()
            
            logger.info(f"Fund updated successfully: {fund_id}")
            
            return FundResponse(
                id=updated_fund.id,
                name=updated_fund.name,
                description=updated_fund.description,
                manager_id=updated_fund.manager_id,
                status=updated_fund.status,
                initial_capital=updated_fund.initial_capital,
                current_capital=updated_fund.current_capital,
                management_fee_rate=updated_fund.management_fee_rate,
                performance_fee_rate=updated_fund.performance_fee_rate,
                max_drawdown_limit=updated_fund.max_drawdown_limit,
                max_position_size=updated_fund.max_position_size,
                max_leverage=updated_fund.max_leverage,
                created_at=updated_fund.created_at,
                updated_at=updated_fund.updated_at,
                launched_at=updated_fund.launched_at,
                closed_at=updated_fund.closed_at
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating fund: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fund update failed"
        )


@router.get("/{fund_id}/summary", response_model=FundSummary)
async def get_fund_summary(
    fund_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> FundSummary:
    """
    Get comprehensive fund summary.
    
    Args:
        fund_id: Fund ID
        request: HTTP request
        current_user: Current authenticated user
        
    Returns:
        Fund summary with portfolio and performance data
        
    Raises:
        HTTPException: If fund summary retrieval fails
    """
    try:
        # Get database manager from app state
        db_manager: DatabaseManager = request.app.state.db_manager
        db_utils = DatabaseUtils(db_manager)
        
        # Get fund summary
        summary_data = await db_utils.get_fund_summary(fund_id)
        
        if not summary_data or not summary_data['fund']:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fund not found"
            )
        
        # Check access permissions
        fund_data = summary_data['fund']
        if (current_user['role'] not in ['admin', 'fund_manager'] and 
            fund_data['manager_id'] != current_user['id']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Build response
        fund_response = FundResponse(
            id=fund_data['id'],
            name=fund_data['name'],
            description=fund_data.get('description'),
            manager_id=fund_data['manager_id'],
            status=fund_data['status'],
            initial_capital=fund_data['initial_capital'],
            current_capital=fund_data['current_capital'],
            management_fee_rate=fund_data['management_fee_rate'],
            performance_fee_rate=fund_data['performance_fee_rate'],
            max_drawdown_limit=fund_data['max_drawdown_limit'],
            max_position_size=fund_data['max_position_size'],
            max_leverage=fund_data['max_leverage'],
            created_at=fund_data['created_at'],
            updated_at=fund_data['updated_at'],
            launched_at=fund_data.get('launched_at'),
            closed_at=fund_data.get('closed_at')
        )
        
        return FundSummary(
            fund=fund_response,
            portfolio=summary_data.get('portfolio', {}),
            performance=summary_data.get('performance')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting fund summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get fund summary"
        )


@router.delete("/{fund_id}", response_model=Dict[str, str])
async def delete_fund(
    fund_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(require_fund_manager)
) -> Dict[str, str]:
    """
    Delete fund (soft delete by setting status to closed).
    
    Args:
        fund_id: Fund ID
        request: HTTP request
        current_user: Current authenticated user
        
    Returns:
        Deletion confirmation
        
    Raises:
        HTTPException: If fund deletion fails
    """
    try:
        # Get database manager from app state
        db_manager: DatabaseManager = request.app.state.db_manager
        
        # Check if fund exists and user has access
        async with db_manager.get_async_session() as session:
            from sqlalchemy import text
            result = await session.execute(
                text("SELECT * FROM funds WHERE id = :fund_id"),
                {"fund_id": fund_id}
            )
            fund = result.fetchone()
            
            if not fund:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Fund not found"
                )
            
            # Check if user is fund manager or admin
            if (current_user['role'] != 'admin' and 
                fund.manager_id != current_user['id']):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            
            # Soft delete by setting status to closed
            await session.execute(
                text("""
                    UPDATE funds 
                    SET status = 'closed', closed_at = :closed_at, updated_at = :updated_at
                    WHERE id = :fund_id
                """),
                {
                    'fund_id': fund_id,
                    'closed_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
            )
            await session.commit()
            
            logger.info(f"Fund closed successfully: {fund_id}")
            
            return {
                'message': 'Fund closed successfully'
            }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting fund: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fund deletion failed"
        )