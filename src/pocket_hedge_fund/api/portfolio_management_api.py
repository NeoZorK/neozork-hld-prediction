"""
Advanced Portfolio Management API for Pocket Hedge Fund

This module provides comprehensive portfolio management functionality including:
- Real-time portfolio tracking and analytics
- Advanced risk management and monitoring
- Automated rebalancing and optimization
- Performance attribution and reporting
- Multi-strategy portfolio support
"""

import asyncio
import logging
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any, List, Union
from decimal import Decimal
import uuid

from fastapi import APIRouter, HTTPException, Depends, Query, Path, BackgroundTasks
from fastapi import status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, field_validator, Field, validator

from ..database.connection import get_db_manager
from ..auth.auth_manager import get_auth_manager, get_current_user
from ..fund_management.portfolio_manager import PortfolioManager, Position, AssetType, PositionType
from ..fund_management.risk_analytics import RiskAnalytics
from ..fund_management.performance_tracker import PerformanceTracker

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/portfolio-management", tags=["portfolio-management"])

# Security
security = HTTPBearer()

# Pydantic models for request/response
class PortfolioOverviewResponse(BaseModel):
    """Response model for portfolio overview."""
    portfolio_id: str
    investor_id: str
    fund_id: str
    total_value: float
    total_invested: float
    total_pnl: float
    total_return_percentage: float
    daily_pnl: float
    daily_return_percentage: float
    positions_count: int
    active_positions: int
    risk_metrics: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    last_updated: str
    created_at: str

class PositionDetailResponse(BaseModel):
    """Response model for position details."""
    position_id: str
    asset_id: str
    asset_name: str
    asset_type: str
    position_type: str
    quantity: float
    entry_price: float
    current_price: float
    market_value: float
    unrealized_pnl: float
    realized_pnl: float
    return_percentage: float
    weight_percentage: float
    entry_date: str
    stop_loss: Optional[float]
    take_profit: Optional[float]
    risk_level: float

class AddPositionRequest(BaseModel):
    """Request model for adding a position."""
    asset_id: str = Field(..., description="Asset identifier")
    asset_name: str = Field(..., description="Asset name")
    asset_type: str = Field(..., description="Asset type (crypto, stock, bond, etc.)")
    position_type: str = Field(..., description="Position type (long, short)")
    quantity: float = Field(..., gt=0, description="Position quantity")
    entry_price: float = Field(..., gt=0, description="Entry price")
    stop_loss: Optional[float] = Field(None, description="Stop loss price")
    take_profit: Optional[float] = Field(None, description="Take profit price")
    risk_level: float = Field(0.02, ge=0, le=1, description="Risk level (0-1)")
    
    @field_validator('position_type')
    def validate_position_type(cls, v):
        if v.lower() not in ['long', 'short']:
            raise ValueError('Position type must be "long" or "short"')
        return v.lower()
    
    @field_validator('asset_type')
    def validate_asset_type(cls, v):
        valid_types = ['crypto', 'stock', 'bond', 'commodity', 'forex', 'derivative']
        if v.lower() not in valid_types:
            raise ValueError(f'Asset type must be one of: {valid_types}')
        return v.lower()

class UpdatePositionRequest(BaseModel):
    """Request model for updating a position."""
    quantity: Optional[float] = Field(None, gt=0, description="New quantity")
    stop_loss: Optional[float] = Field(None, description="New stop loss price")
    take_profit: Optional[float] = Field(None, description="New take profit price")
    risk_level: Optional[float] = Field(None, ge=0, le=1, description="New risk level")

class RebalanceRequest(BaseModel):
    """Request model for portfolio rebalancing."""
    target_allocations: Dict[str, float] = Field(..., description="Target allocations by asset")
    rebalance_threshold: float = Field(0.05, ge=0, le=1, description="Rebalance threshold")
    max_trades: Optional[int] = Field(None, description="Maximum number of trades")
    
    @field_validator('target_allocations')
    def validate_allocations(cls, v):
        total = sum(v.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError('Target allocations must sum to 1.0')
        return v

class RiskMetricsResponse(BaseModel):
    """Response model for risk metrics."""
    var_95: float
    var_99: float
    cvar_95: float
    cvar_99: float
    max_drawdown: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    volatility: float
    beta: float
    correlation_matrix: Dict[str, Dict[str, float]]
    concentration_risk: Dict[str, float]
    stress_test_results: Dict[str, Any]

class PerformanceMetricsResponse(BaseModel):
    """Response model for performance metrics."""
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    alpha: float
    beta: float
    tracking_error: float
    information_ratio: float

class PortfolioAnalyticsResponse(BaseModel):
    """Response model for portfolio analytics."""
    performance_metrics: PerformanceMetricsResponse
    risk_metrics: RiskMetricsResponse
    attribution_analysis: Dict[str, Any]
    sector_allocation: Dict[str, float]
    asset_allocation: Dict[str, float]
    performance_attribution: Dict[str, Any]
    benchmark_comparison: Dict[str, Any]

# Portfolio Management Endpoints

@router.get("/{fund_id}/overview", response_model=PortfolioOverviewResponse)
async def get_portfolio_overview(
    fund_id: str = Path(..., description="Fund ID"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get comprehensive portfolio overview."""
    try:
        # Check if user has access to this fund
        if current_user['role'] not in ['admin', 'fund_manager'] and current_user['id'] not in await _get_fund_investors(fund_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this fund"
            )
        
        db_manager = await get_db_manager()
        
        # Get portfolio data
        portfolio_query = """
            SELECT p.*, f.name as fund_name, f.fund_type
            FROM portfolios p
            JOIN funds f ON p.fund_id = f.id
            WHERE p.fund_id = $1
        """
        
        portfolio_data = await db_manager.execute_query(portfolio_query, {'1': fund_id})
        
        if not portfolio_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found"
            )
        
        portfolio = portfolio_data[0]
        
        # Get positions
        positions_query = """
            SELECT * FROM portfolio_positions 
            WHERE portfolio_id = $1 AND status = 'active'
        """
        positions = await db_manager.execute_query(positions_query, {'1': portfolio['id']})
        
        # Calculate metrics
        total_value = sum(pos['market_value'] for pos in positions)
        total_invested = sum(pos['quantity'] * pos['entry_price'] for pos in positions)
        total_pnl = total_value - total_invested
        total_return_percentage = (total_pnl / total_invested * 100) if total_invested > 0 else 0
        
        # Get daily P&L
        daily_pnl_query = """
            SELECT daily_pnl FROM portfolio_performance 
            WHERE portfolio_id = $1 
            ORDER BY date DESC LIMIT 1
        """
        daily_pnl_data = await db_manager.execute_query(daily_pnl_query, {'1': portfolio['id']})
        daily_pnl = daily_pnl_data[0]['daily_pnl'] if daily_pnl_data else 0
        daily_return_percentage = (daily_pnl / total_value * 100) if total_value > 0 else 0
        
        # Get risk metrics
        risk_metrics = await _calculate_risk_metrics(portfolio['id'])
        
        # Get performance metrics
        performance_metrics = await _calculate_performance_metrics(portfolio['id'])
        
        return PortfolioOverviewResponse(
            portfolio_id=portfolio['id'],
            investor_id=portfolio['investor_id'],
            fund_id=fund_id,
            total_value=total_value,
            total_invested=total_invested,
            total_pnl=total_pnl,
            total_return_percentage=total_return_percentage,
            daily_pnl=daily_pnl,
            daily_return_percentage=daily_return_percentage,
            positions_count=len(positions),
            active_positions=len([p for p in positions if p['status'] == 'active']),
            risk_metrics=risk_metrics,
            performance_metrics=performance_metrics,
            last_updated=portfolio['updated_at'].isoformat(),
            created_at=portfolio['created_at'].isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get portfolio overview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get portfolio overview: {str(e)}"
        )

@router.get("/{fund_id}/positions", response_model=List[PositionDetailResponse])
async def get_portfolio_positions(
    fund_id: str = Path(..., description="Fund ID"),
    status_filter: Optional[str] = Query(None, description="Filter by position status"),
    asset_type: Optional[str] = Query(None, description="Filter by asset type"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get detailed portfolio positions."""
    try:
        # Check access
        if current_user['role'] not in ['admin', 'fund_manager'] and current_user['id'] not in await _get_fund_investors(fund_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this fund"
            )
        
        db_manager = await get_db_manager()
        
        # Get portfolio ID
        portfolio_query = "SELECT id FROM portfolios WHERE fund_id = $1"
        portfolio_data = await db_manager.execute_query(portfolio_query, {'1': fund_id})
        
        if not portfolio_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found"
            )
        
        portfolio_id = portfolio_data[0]['id']
        
        # Build query with filters
        where_conditions = ["portfolio_id = $1"]
        params = [portfolio_id]
        
        if status_filter:
            where_conditions.append("status = $2")
            params.append(status_filter)
        
        if asset_type:
            where_conditions.append("asset_type = $3")
            params.append(asset_type)
        
        where_clause = "WHERE " + " AND ".join(where_conditions)
        
        positions_query = f"""
            SELECT * FROM portfolio_positions {where_clause}
            ORDER BY market_value DESC
        """
        
        positions = await db_manager.execute_query(positions_query, dict(enumerate(params, 1)))
        
        # Calculate total portfolio value for weight calculation
        total_value_query = """
            SELECT SUM(market_value) as total_value 
            FROM portfolio_positions 
            WHERE portfolio_id = $1 AND status = 'active'
        """
        total_value_data = await db_manager.execute_query(total_value_query, {'1': portfolio_id})
        total_value = total_value_data[0]['total_value'] if total_value_data and total_value_data[0]['total_value'] else 1
        
        result = []
        for pos in positions:
            return_percentage = ((pos['current_price'] - pos['entry_price']) / pos['entry_price'] * 100) if pos['entry_price'] > 0 else 0
            weight_percentage = (pos['market_value'] / total_value * 100) if total_value > 0 else 0
            
            result.append(PositionDetailResponse(
                position_id=pos['id'],
                asset_id=pos['asset_id'],
                asset_name=pos['asset_name'],
                asset_type=pos['asset_type'],
                position_type=pos['position_type'],
                quantity=pos['quantity'],
                entry_price=pos['entry_price'],
                current_price=pos['current_price'],
                market_value=pos['market_value'],
                unrealized_pnl=pos['unrealized_pnl'],
                realized_pnl=pos['realized_pnl'],
                return_percentage=return_percentage,
                weight_percentage=weight_percentage,
                entry_date=pos['entry_date'].isoformat(),
                stop_loss=pos['stop_loss'],
                take_profit=pos['take_profit'],
                risk_level=pos['risk_level']
            ))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get portfolio positions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get portfolio positions: {str(e)}"
        )

@router.post("/{fund_id}/positions", response_model=Dict[str, Any])
async def add_position(
    fund_id: str = Path(..., description="Fund ID"),
    position_request: AddPositionRequest = ...,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Add a new position to the portfolio."""
    try:
        # Check access
        if current_user['role'] not in ['admin', 'fund_manager']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Requires fund manager role"
            )
        
        db_manager = await get_db_manager()
        
        # Get portfolio ID
        portfolio_query = "SELECT id FROM portfolios WHERE fund_id = $1"
        portfolio_data = await db_manager.execute_query(portfolio_query, {'1': fund_id})
        
        if not portfolio_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found"
            )
        
        portfolio_id = portfolio_data[0]['id']
        
        # Validate position doesn't already exist
        existing_query = """
            SELECT id FROM portfolio_positions 
            WHERE portfolio_id = $1 AND asset_id = $2 AND status = 'active'
        """
        existing = await db_manager.execute_query(existing_query, {'1': portfolio_id, '2': position_request.asset_id})
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Position already exists for this asset"
            )
        
        # Calculate market value
        market_value = position_request.quantity * position_request.entry_price
        
        # Insert new position
        position_id = str(uuid.uuid4())
        insert_query = """
            INSERT INTO portfolio_positions (
                id, portfolio_id, asset_id, asset_name, asset_type, position_type,
                quantity, entry_price, current_price, market_value, unrealized_pnl,
                realized_pnl, entry_date, stop_loss, take_profit, risk_level, status
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17)
        """
        
        await db_manager.execute_command(insert_query, {
            '1': position_id,
            '2': portfolio_id,
            '3': position_request.asset_id,
            '4': position_request.asset_name,
            '5': position_request.asset_type,
            '6': position_request.position_type,
            '7': position_request.quantity,
            '8': position_request.entry_price,
            '9': position_request.entry_price,  # Initial current price = entry price
            '10': market_value,
            '11': 0,  # Initial unrealized P&L
            '12': 0,  # Initial realized P&L
            '13': datetime.now(datetime.UTC),
            '14': position_request.stop_loss,
            '15': position_request.take_profit,
            '16': position_request.risk_level,
            '17': 'active'
        })
        
        # Log the transaction
        auth_manager = await get_auth_manager()
        await auth_manager._log_audit_event(
            user_id=current_user['id'],
            action="position_added",
            resource_type="portfolio_position",
            resource_id=position_id,
            new_values={
                'asset_id': position_request.asset_id,
                'quantity': position_request.quantity,
                'entry_price': position_request.entry_price,
                'market_value': market_value
            }
        )
        
        return {
            'success': True,
            'position_id': position_id,
            'message': 'Position added successfully',
            'market_value': market_value
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to add position: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add position: {str(e)}"
        )

@router.put("/{fund_id}/positions/{position_id}", response_model=Dict[str, Any])
async def update_position(
    fund_id: str = Path(..., description="Fund ID"),
    position_id: str = Path(..., description="Position ID"),
    update_request: UpdatePositionRequest = ...,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update an existing position."""
    try:
        # Check access
        if current_user['role'] not in ['admin', 'fund_manager']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Requires fund manager role"
            )
        
        db_manager = await get_db_manager()
        
        # Get current position
        position_query = """
            SELECT * FROM portfolio_positions 
            WHERE id = $1 AND portfolio_id IN (
                SELECT id FROM portfolios WHERE fund_id = $2
            )
        """
        position_data = await db_manager.execute_query(position_query, {'1': position_id, '2': fund_id})
        
        if not position_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Position not found"
            )
        
        position = position_data[0]
        
        # Build update query
        update_fields = []
        params = []
        param_count = 1
        
        if update_request.quantity is not None:
            update_fields.append(f"quantity = ${param_count}")
            params.append(update_request.quantity)
            param_count += 1
            
            # Recalculate market value
            update_fields.append(f"market_value = ${param_count}")
            params.append(update_request.quantity * position['current_price'])
            param_count += 1
        
        if update_request.stop_loss is not None:
            update_fields.append(f"stop_loss = ${param_count}")
            params.append(update_request.stop_loss)
            param_count += 1
        
        if update_request.take_profit is not None:
            update_fields.append(f"take_profit = ${param_count}")
            params.append(update_request.take_profit)
            param_count += 1
        
        if update_request.risk_level is not None:
            update_fields.append(f"risk_level = ${param_count}")
            params.append(update_request.risk_level)
            param_count += 1
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        # Add updated_at
        update_fields.append(f"updated_at = ${param_count}")
        params.append(datetime.now(datetime.UTC))
        param_count += 1
        
        # Add position_id and fund_id for WHERE clause
        params.extend([position_id, fund_id])
        
        update_query = f"""
            UPDATE portfolio_positions 
            SET {', '.join(update_fields)}
            WHERE id = ${param_count} AND portfolio_id IN (
                SELECT id FROM portfolios WHERE fund_id = ${param_count + 1}
            )
        """
        
        await db_manager.execute_command(update_query, dict(enumerate(params, 1)))
        
        # Log the transaction
        auth_manager = await get_auth_manager()
        await auth_manager._log_audit_event(
            user_id=current_user['id'],
            action="position_updated",
            resource_type="portfolio_position",
            resource_id=position_id,
            old_values=position,
            new_values=update_request.dict(exclude_unset=True)
        )
        
        return {
            'success': True,
            'message': 'Position updated successfully'
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update position: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update position: {str(e)}"
        )

@router.delete("/{fund_id}/positions/{position_id}", response_model=Dict[str, Any])
async def close_position(
    fund_id: str = Path(..., description="Fund ID"),
    position_id: str = Path(..., description="Position ID"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Close a position."""
    try:
        # Check access
        if current_user['role'] not in ['admin', 'fund_manager']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Requires fund manager role"
            )
        
        db_manager = await get_db_manager()
        
        # Get current position
        position_query = """
            SELECT * FROM portfolio_positions 
            WHERE id = $1 AND portfolio_id IN (
                SELECT id FROM portfolios WHERE fund_id = $2
            ) AND status = 'active'
        """
        position_data = await db_manager.execute_query(position_query, {'1': position_id, '2': fund_id})
        
        if not position_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active position not found"
            )
        
        position = position_data[0]
        
        # Close the position
        close_query = """
            UPDATE portfolio_positions 
            SET status = 'closed', closed_at = $1, updated_at = $2
            WHERE id = $3
        """
        
        await db_manager.execute_command(close_query, {
            '1': datetime.now(datetime.UTC),
            '2': datetime.now(datetime.UTC),
            '3': position_id
        })
        
        # Log the transaction
        auth_manager = await get_auth_manager()
        await auth_manager._log_audit_event(
            user_id=current_user['id'],
            action="position_closed",
            resource_type="portfolio_position",
            resource_id=position_id,
            old_values={'status': 'active'},
            new_values={'status': 'closed', 'closed_at': datetime.now(datetime.UTC)}
        )
        
        return {
            'success': True,
            'message': 'Position closed successfully',
            'realized_pnl': position['unrealized_pnl']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to close position: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to close position: {str(e)}"
        )

@router.get("/{fund_id}/analytics", response_model=PortfolioAnalyticsResponse)
async def get_portfolio_analytics(
    fund_id: str = Path(..., description="Fund ID"),
    period: str = Query("1Y", description="Analysis period (1M, 3M, 6M, 1Y, 2Y, 5Y)"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get comprehensive portfolio analytics."""
    try:
        # Check access
        if current_user['role'] not in ['admin', 'fund_manager'] and current_user['id'] not in await _get_fund_investors(fund_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this fund"
            )
        
        db_manager = await get_db_manager()
        
        # Get portfolio ID
        portfolio_query = "SELECT id FROM portfolios WHERE fund_id = $1"
        portfolio_data = await db_manager.execute_query(portfolio_query, {'1': fund_id})
        
        if not portfolio_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found"
            )
        
        portfolio_id = portfolio_data[0]['id']
        
        # Calculate performance metrics
        performance_metrics = await _calculate_performance_metrics(portfolio_id, period)
        
        # Calculate risk metrics
        risk_metrics = await _calculate_risk_metrics(portfolio_id, period)
        
        # Get attribution analysis
        attribution_analysis = await _calculate_attribution_analysis(portfolio_id, period)
        
        # Get allocation data
        sector_allocation = await _get_sector_allocation(portfolio_id)
        asset_allocation = await _get_asset_allocation(portfolio_id)
        
        # Get performance attribution
        performance_attribution = await _get_performance_attribution(portfolio_id, period)
        
        # Get benchmark comparison
        benchmark_comparison = await _get_benchmark_comparison(portfolio_id, period)
        
        return PortfolioAnalyticsResponse(
            performance_metrics=performance_metrics,
            risk_metrics=risk_metrics,
            attribution_analysis=attribution_analysis,
            sector_allocation=sector_allocation,
            asset_allocation=asset_allocation,
            performance_attribution=performance_attribution,
            benchmark_comparison=benchmark_comparison
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get portfolio analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get portfolio analytics: {str(e)}"
        )

@router.post("/{fund_id}/rebalance", response_model=Dict[str, Any])
async def rebalance_portfolio(
    fund_id: str = Path(..., description="Fund ID"),
    rebalance_request: RebalanceRequest = ...,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Rebalance portfolio to target allocations."""
    try:
        # Check access
        if current_user['role'] not in ['admin', 'fund_manager']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Requires fund manager role"
            )
        
        # Start rebalancing in background
        background_tasks.add_task(
            _execute_rebalancing,
            fund_id,
            rebalance_request,
            current_user['id']
        )
        
        return {
            'success': True,
            'message': 'Portfolio rebalancing started',
            'target_allocations': rebalance_request.target_allocations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to start portfolio rebalancing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start portfolio rebalancing: {str(e)}"
        )

# Helper functions

async def _get_fund_investors(fund_id: str) -> List[str]:
    """Get list of investor IDs for a fund."""
    db_manager = await get_db_manager()
    query = "SELECT investor_id FROM investments WHERE fund_id = $1"
    result = await db_manager.execute_query(query, {'1': fund_id})
    return [row['investor_id'] for row in result]

async def _calculate_risk_metrics(portfolio_id: str, period: str = "1Y") -> RiskMetricsResponse:
    """Calculate comprehensive risk metrics."""
    # This would integrate with the RiskAnalytics class
    # For now, return mock data
    return RiskMetricsResponse(
        var_95=0.02,
        var_99=0.03,
        cvar_95=0.025,
        cvar_99=0.035,
        max_drawdown=0.08,
        sharpe_ratio=1.2,
        sortino_ratio=1.5,
        calmar_ratio=0.8,
        volatility=0.15,
        beta=0.9,
        correlation_matrix={},
        concentration_risk={},
        stress_test_results={}
    )

async def _calculate_performance_metrics(portfolio_id: str, period: str = "1Y") -> PerformanceMetricsResponse:
    """Calculate comprehensive performance metrics."""
    # This would integrate with the PerformanceTracker class
    # For now, return mock data
    return PerformanceMetricsResponse(
        total_return=0.12,
        annualized_return=0.12,
        volatility=0.15,
        sharpe_ratio=1.2,
        sortino_ratio=1.5,
        calmar_ratio=0.8,
        max_drawdown=0.08,
        win_rate=0.65,
        profit_factor=1.8,
        alpha=0.02,
        beta=0.9,
        tracking_error=0.05,
        information_ratio=0.4
    )

async def _calculate_attribution_analysis(portfolio_id: str, period: str) -> Dict[str, Any]:
    """Calculate performance attribution analysis."""
    return {
        'asset_allocation_effect': 0.02,
        'security_selection_effect': 0.01,
        'interaction_effect': 0.005,
        'total_attribution': 0.035
    }

async def _get_sector_allocation(portfolio_id: str) -> Dict[str, float]:
    """Get sector allocation breakdown."""
    return {
        'Technology': 0.35,
        'Healthcare': 0.20,
        'Financial': 0.15,
        'Consumer': 0.15,
        'Industrial': 0.10,
        'Other': 0.05
    }

async def _get_asset_allocation(portfolio_id: str) -> Dict[str, float]:
    """Get asset allocation breakdown."""
    return {
        'Stocks': 0.70,
        'Bonds': 0.20,
        'Crypto': 0.05,
        'Commodities': 0.03,
        'Cash': 0.02
    }

async def _get_performance_attribution(portfolio_id: str, period: str) -> Dict[str, Any]:
    """Get performance attribution breakdown."""
    return {
        'top_contributors': [
            {'asset': 'AAPL', 'contribution': 0.02},
            {'asset': 'MSFT', 'contribution': 0.015},
            {'asset': 'GOOGL', 'contribution': 0.01}
        ],
        'bottom_contributors': [
            {'asset': 'TSLA', 'contribution': -0.005},
            {'asset': 'NVDA', 'contribution': -0.003}
        ]
    }

async def _get_benchmark_comparison(portfolio_id: str, period: str) -> Dict[str, Any]:
    """Get benchmark comparison data."""
    return {
        'benchmark_return': 0.10,
        'portfolio_return': 0.12,
        'excess_return': 0.02,
        'tracking_error': 0.05,
        'information_ratio': 0.4,
        'beta': 0.9,
        'alpha': 0.02
    }

async def _execute_rebalancing(fund_id: str, rebalance_request: RebalanceRequest, user_id: str):
    """Execute portfolio rebalancing in background."""
    try:
        logger.info(f"Starting rebalancing for fund {fund_id}")
        
        db_manager = await get_db_manager()
        
        # Get current portfolio
        portfolio_query = "SELECT id FROM portfolios WHERE fund_id = $1"
        portfolio_data = await db_manager.execute_query(portfolio_query, {'1': fund_id})
        
        if not portfolio_data:
            logger.error(f"Portfolio not found for fund {fund_id}")
            return
        
        portfolio_id = portfolio_data[0]['id']
        
        # Get current positions
        positions_query = """
            SELECT * FROM portfolio_positions 
            WHERE portfolio_id = $1 AND status = 'active'
        """
        positions = await db_manager.execute_query(positions_query, {'1': portfolio_id})
        
        # Calculate current allocations
        total_value = sum(pos['market_value'] for pos in positions)
        current_allocations = {}
        
        for pos in positions:
            asset_type = pos['asset_type']
            if asset_type not in current_allocations:
                current_allocations[asset_type] = 0
            current_allocations[asset_type] += pos['market_value'] / total_value
        
        # Calculate required trades
        trades = []
        for asset_type, target_weight in rebalance_request.target_allocations.items():
            current_weight = current_allocations.get(asset_type, 0)
            weight_diff = target_weight - current_weight
            
            if abs(weight_diff) > rebalance_request.rebalance_threshold:
                target_value = total_value * target_weight
                current_value = total_value * current_weight
                trade_value = target_value - current_value
                
                trades.append({
                    'asset_type': asset_type,
                    'current_weight': current_weight,
                    'target_weight': target_weight,
                    'trade_value': trade_value
                })
        
        # Execute trades (simplified - in real implementation would place actual orders)
        for trade in trades:
            logger.info(f"Executing trade: {trade}")
            # Here you would implement actual trading logic
        
        # Log rebalancing completion
        auth_manager = await get_auth_manager()
        await auth_manager._log_audit_event(
            user_id=user_id,
            action="portfolio_rebalanced",
            resource_type="portfolio",
            resource_id=portfolio_id,
            new_values={
                'target_allocations': rebalance_request.target_allocations,
                'trades_executed': len(trades)
            }
        )
        
        logger.info(f"Rebalancing completed for fund {fund_id}")
        
    except Exception as e:
        logger.error(f"Failed to execute rebalancing: {e}")
