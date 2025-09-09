"""
Portfolio API for Pocket Hedge Fund.

This module provides REST API endpoints for portfolio management operations
including position management, portfolio analysis, and risk monitoring.
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
router = APIRouter(prefix="/portfolios", tags=["Portfolio Management"])


# Pydantic models

class PositionCreate(BaseModel):
    """Position creation request model."""
    fund_id: str
    symbol: str
    position_type: str  # 'long', 'short', 'cash'
    quantity: Decimal
    entry_price: Decimal
    stop_loss: Optional[Decimal] = None
    take_profit: Optional[Decimal] = None
    notes: Optional[str] = None
    
    @validator('position_type')
    def validate_position_type(cls, v):
        if v not in ['long', 'short', 'cash']:
            raise ValueError('Position type must be long, short, or cash')
        return v
    
    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v
    
    @validator('entry_price')
    def validate_entry_price(cls, v):
        if v <= 0:
            raise ValueError('Entry price must be positive')
        return v


class PositionUpdate(BaseModel):
    """Position update request model."""
    quantity: Optional[Decimal] = None
    stop_loss: Optional[Decimal] = None
    take_profit: Optional[Decimal] = None
    notes: Optional[str] = None
    
    @validator('quantity')
    def validate_quantity(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Quantity must be positive')
        return v


class PositionResponse(BaseModel):
    """Position response model."""
    id: str
    fund_id: str
    symbol: str
    position_type: str
    quantity: Decimal
    entry_price: Decimal
    current_price: Optional[Decimal]
    stop_loss: Optional[Decimal]
    take_profit: Optional[Decimal]
    unrealized_pnl: Optional[Decimal]
    realized_pnl: Optional[Decimal]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime]


class PortfolioResponse(BaseModel):
    """Portfolio response model."""
    fund_id: str
    total_value: Decimal
    cash_balance: Decimal
    invested_value: Decimal
    unrealized_pnl: Decimal
    realized_pnl: Decimal
    total_return: Decimal
    positions: List[PositionResponse]
    last_updated: datetime


class PortfolioSummary(BaseModel):
    """Portfolio summary model."""
    portfolio: PortfolioResponse
    risk_metrics: Dict[str, Any]
    performance_metrics: Dict[str, Any]


# API endpoints

@router.post("/{fund_id}/positions", response_model=PositionResponse, status_code=status.HTTP_201_CREATED)
async def create_position(
    fund_id: str,
    position_data: PositionCreate,
    request: Request,
    current_user: Dict[str, Any] = Depends(require_fund_manager)
) -> PositionResponse:
    """
    Create a new position in the fund portfolio.
    
    Args:
        fund_id: Fund ID
        position_data: Position creation data
        request: HTTP request
        current_user: Current authenticated user
        
    Returns:
        Created position information
        
    Raises:
        HTTPException: If position creation fails
    """
    try:
        # Get database manager from app state
        db_manager: DatabaseManager = request.app.state.db_manager
        
        # Verify fund access
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
        
        # Create position
        import uuid
        position_id = str(uuid.uuid4())
        
        async with db_manager.get_async_session() as session:
            await session.execute(
                text("""
                    INSERT INTO positions (
                        id, fund_id, symbol, position_type, quantity, entry_price,
                        stop_loss, take_profit, notes, created_at, updated_at
                    ) VALUES (
                        :id, :fund_id, :symbol, :position_type, :quantity, :entry_price,
                        :stop_loss, :take_profit, :notes, :created_at, :updated_at
                    )
                """),
                {
                    'id': position_id,
                    'fund_id': fund_id,
                    'symbol': position_data.symbol,
                    'position_type': position_data.position_type,
                    'quantity': position_data.quantity,
                    'entry_price': position_data.entry_price,
                    'stop_loss': position_data.stop_loss,
                    'take_profit': position_data.take_profit,
                    'notes': position_data.notes,
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
            )
            await session.commit()
        
        logger.info(f"Position created successfully: {position_data.symbol} in fund {fund_id}")
        
        # Return created position
        return PositionResponse(
            id=position_id,
            fund_id=fund_id,
            symbol=position_data.symbol,
            position_type=position_data.position_type,
            quantity=position_data.quantity,
            entry_price=position_data.entry_price,
            current_price=None,
            stop_loss=position_data.stop_loss,
            take_profit=position_data.take_profit,
            unrealized_pnl=None,
            realized_pnl=None,
            notes=position_data.notes,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            closed_at=None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating position: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Position creation failed"
        )


@router.get("/{fund_id}/positions", response_model=List[PositionResponse])
async def list_positions(
    fund_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
) -> List[PositionResponse]:
    """
    List positions in the fund portfolio.
    
    Args:
        fund_id: Fund ID
        request: HTTP request
        current_user: Current authenticated user
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of positions
        
    Raises:
        HTTPException: If position listing fails
    """
    try:
        # Get database manager from app state
        db_manager: DatabaseManager = request.app.state.db_manager
        
        # Verify fund access
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
            
            # Check access permissions
            if (current_user['role'] not in ['admin', 'fund_manager'] and 
                fund.manager_id != current_user['id']):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            
            # Get positions
            result = await session.execute(
                text("""
                    SELECT * FROM positions 
                    WHERE fund_id = :fund_id AND closed_at IS NULL
                    ORDER BY created_at DESC
                    LIMIT :limit OFFSET :skip
                """),
                {"fund_id": fund_id, "limit": limit, "skip": skip}
            )
            positions_data = result.fetchall()
        
        # Convert to response models
        positions = []
        for position_data in positions_data:
            positions.append(PositionResponse(
                id=position_data.id,
                fund_id=position_data.fund_id,
                symbol=position_data.symbol,
                position_type=position_data.position_type,
                quantity=position_data.quantity,
                entry_price=position_data.entry_price,
                current_price=position_data.current_price,
                stop_loss=position_data.stop_loss,
                take_profit=position_data.take_profit,
                unrealized_pnl=position_data.unrealized_pnl,
                realized_pnl=position_data.realized_pnl,
                notes=position_data.notes,
                created_at=position_data.created_at,
                updated_at=position_data.updated_at,
                closed_at=position_data.closed_at
            ))
        
        return positions
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing positions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list positions"
        )


@router.get("/{fund_id}/positions/{position_id}", response_model=PositionResponse)
async def get_position(
    fund_id: str,
    position_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> PositionResponse:
    """
    Get position by ID.
    
    Args:
        fund_id: Fund ID
        position_id: Position ID
        request: HTTP request
        current_user: Current authenticated user
        
    Returns:
        Position information
        
    Raises:
        HTTPException: If position not found or access denied
    """
    try:
        # Get database manager from app state
        db_manager: DatabaseManager = request.app.state.db_manager
        
        async with db_manager.get_async_session() as session:
            from sqlalchemy import text
            result = await session.execute(
                text("""
                    SELECT p.*, f.manager_id 
                    FROM positions p
                    JOIN funds f ON p.fund_id = f.id
                    WHERE p.id = :position_id AND p.fund_id = :fund_id
                """),
                {"position_id": position_id, "fund_id": fund_id}
            )
            position_data = result.fetchone()
            
            if not position_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Position not found"
                )
            
            # Check access permissions
            if (current_user['role'] not in ['admin', 'fund_manager'] and 
                position_data.manager_id != current_user['id']):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            
            return PositionResponse(
                id=position_data.id,
                fund_id=position_data.fund_id,
                symbol=position_data.symbol,
                position_type=position_data.position_type,
                quantity=position_data.quantity,
                entry_price=position_data.entry_price,
                current_price=position_data.current_price,
                stop_loss=position_data.stop_loss,
                take_profit=position_data.take_profit,
                unrealized_pnl=position_data.unrealized_pnl,
                realized_pnl=position_data.realized_pnl,
                notes=position_data.notes,
                created_at=position_data.created_at,
                updated_at=position_data.updated_at,
                closed_at=position_data.closed_at
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting position: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get position"
        )


@router.put("/{fund_id}/positions/{position_id}", response_model=PositionResponse)
async def update_position(
    fund_id: str,
    position_id: str,
    position_data: PositionUpdate,
    request: Request,
    current_user: Dict[str, Any] = Depends(require_fund_manager)
) -> PositionResponse:
    """
    Update position information.
    
    Args:
        fund_id: Fund ID
        position_id: Position ID
        position_data: Position update data
        request: HTTP request
        current_user: Current authenticated user
        
    Returns:
        Updated position information
        
    Raises:
        HTTPException: If position update fails
    """
    try:
        # Get database manager from app state
        db_manager: DatabaseManager = request.app.state.db_manager
        
        # Check if position exists and user has access
        async with db_manager.get_async_session() as session:
            from sqlalchemy import text
            result = await session.execute(
                text("""
                    SELECT p.*, f.manager_id 
                    FROM positions p
                    JOIN funds f ON p.fund_id = f.id
                    WHERE p.id = :position_id AND p.fund_id = :fund_id
                """),
                {"position_id": position_id, "fund_id": fund_id}
            )
            position = result.fetchone()
            
            if not position:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Position not found"
                )
            
            # Check if user is fund manager or admin
            if (current_user['role'] != 'admin' and 
                position.manager_id != current_user['id']):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            
            # Build update query
            update_fields = []
            update_values = {'position_id': position_id, 'updated_at': datetime.utcnow()}
            
            for field, value in position_data.dict(exclude_unset=True).items():
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
                UPDATE positions 
                SET {', '.join(update_fields)}, updated_at = :updated_at
                WHERE id = :position_id
            """
            
            await session.execute(text(update_query), update_values)
            await session.commit()
            
            # Get updated position
            result = await session.execute(
                text("SELECT * FROM positions WHERE id = :position_id"),
                {"position_id": position_id}
            )
            updated_position = result.fetchone()
            
            logger.info(f"Position updated successfully: {position_id}")
            
            return PositionResponse(
                id=updated_position.id,
                fund_id=updated_position.fund_id,
                symbol=updated_position.symbol,
                position_type=updated_position.position_type,
                quantity=updated_position.quantity,
                entry_price=updated_position.entry_price,
                current_price=updated_position.current_price,
                stop_loss=updated_position.stop_loss,
                take_profit=updated_position.take_profit,
                unrealized_pnl=updated_position.unrealized_pnl,
                realized_pnl=updated_position.realized_pnl,
                notes=updated_position.notes,
                created_at=updated_position.created_at,
                updated_at=updated_position.updated_at,
                closed_at=updated_position.closed_at
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating position: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Position update failed"
        )


@router.delete("/{fund_id}/positions/{position_id}", response_model=Dict[str, str])
async def close_position(
    fund_id: str,
    position_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(require_fund_manager)
) -> Dict[str, str]:
    """
    Close position (soft delete by setting closed_at).
    
    Args:
        fund_id: Fund ID
        position_id: Position ID
        request: HTTP request
        current_user: Current authenticated user
        
    Returns:
        Position closure confirmation
        
    Raises:
        HTTPException: If position closure fails
    """
    try:
        # Get database manager from app state
        db_manager: DatabaseManager = request.app.state.db_manager
        
        # Check if position exists and user has access
        async with db_manager.get_async_session() as session:
            from sqlalchemy import text
            result = await session.execute(
                text("""
                    SELECT p.*, f.manager_id 
                    FROM positions p
                    JOIN funds f ON p.fund_id = f.id
                    WHERE p.id = :position_id AND p.fund_id = :fund_id
                """),
                {"position_id": position_id, "fund_id": fund_id}
            )
            position = result.fetchone()
            
            if not position:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Position not found"
                )
            
            # Check if user is fund manager or admin
            if (current_user['role'] != 'admin' and 
                position.manager_id != current_user['id']):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            
            # Close position
            await session.execute(
                text("""
                    UPDATE positions 
                    SET closed_at = :closed_at, updated_at = :updated_at
                    WHERE id = :position_id
                """),
                {
                    'position_id': position_id,
                    'closed_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
            )
            await session.commit()
            
            logger.info(f"Position closed successfully: {position_id}")
            
            return {
                'message': 'Position closed successfully'
            }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error closing position: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Position closure failed"
        )


@router.get("/{fund_id}/summary", response_model=PortfolioSummary)
async def get_portfolio_summary(
    fund_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> PortfolioSummary:
    """
    Get comprehensive portfolio summary.
    
    Args:
        fund_id: Fund ID
        request: HTTP request
        current_user: Current authenticated user
        
    Returns:
        Portfolio summary with risk and performance metrics
        
    Raises:
        HTTPException: If portfolio summary retrieval fails
    """
    try:
        # Get database manager from app state
        db_manager: DatabaseManager = request.app.state.db_manager
        db_utils = DatabaseUtils(db_manager)
        
        # Get portfolio summary
        summary_data = await db_utils.get_portfolio_summary(fund_id)
        
        if not summary_data or not summary_data['portfolio']:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found"
            )
        
        # Check access permissions
        portfolio_data = summary_data['portfolio']
        if (current_user['role'] not in ['admin', 'fund_manager'] and 
            portfolio_data['manager_id'] != current_user['id']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Build response
        portfolio_response = PortfolioResponse(
            fund_id=portfolio_data['fund_id'],
            total_value=portfolio_data['total_value'],
            cash_balance=portfolio_data['cash_balance'],
            invested_value=portfolio_data['invested_value'],
            unrealized_pnl=portfolio_data['unrealized_pnl'],
            realized_pnl=portfolio_data['realized_pnl'],
            total_return=portfolio_data['total_return'],
            positions=[],  # Will be populated from positions data
            last_updated=portfolio_data['last_updated']
        )
        
        return PortfolioSummary(
            portfolio=portfolio_response,
            risk_metrics=summary_data.get('risk_metrics', {}),
            performance_metrics=summary_data.get('performance_metrics', {})
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting portfolio summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get portfolio summary"
        )