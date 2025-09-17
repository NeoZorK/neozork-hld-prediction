"""
Portfolio Management API for Pocket Hedge Fund

This module provides RESTful API endpoints for portfolio operations
including portfolio overview, performance tracking, and analytics.
"""

import asyncio
import logging
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Depends, Query, Path
from fastapi import status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

from ..database.connection import get_db_manager
from ..auth.auth_manager import get_auth_manager, get_current_user

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/portfolio", tags=["portfolio"])

# Security
security = HTTPBearer()

# Pydantic models for request/response
class PortfolioSummaryResponse(BaseModel):
    """Response model for portfolio summary."""
    investor_id: str
    total_invested: float
    total_current_value: float
    total_return: float
    total_return_percentage: float
    active_investments: int
    total_investments: int
    created_at: str
    updated_at: str

class PortfolioPerformanceResponse(BaseModel):
    """Response model for portfolio performance."""
    period: str
    start_date: str
    end_date: str
    total_return: float
    total_return_percentage: float
    best_performing_fund: Optional[str]
    worst_performing_fund: Optional[str]
    volatility: float
    sharpe_ratio: float

class FundAllocationResponse(BaseModel):
    """Response model for fund allocation."""
    fund_id: str
    fund_name: str
    fund_type: str
    invested_amount: float
    current_value: float
    allocation_percentage: float
    return_amount: float
    return_percentage: float
    shares_owned: float
    share_price: float

class PortfolioAnalyticsResponse(BaseModel):
    """Response model for portfolio analytics."""
    summary: PortfolioSummaryResponse
    performance: PortfolioPerformanceResponse
    fund_allocations: List[FundAllocationResponse]
    risk_metrics: Dict[str, Any]

# Portfolio API endpoints

@router.get("/summary", response_model=PortfolioSummaryResponse)
async def get_portfolio_summary(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get portfolio summary for the current user."""
    try:
        db_manager = await get_db_manager()
        
        # Get all investments for the user
        investments_query = """
            SELECT i.*, f.name as fund_name, f.fund_type, f.current_value as fund_current_value, f.initial_capital
            FROM investments i
            JOIN funds f ON i.fund_id = f.id
            WHERE i.investor_id = $1 AND i.status = 'active'
        """
        investments = await db_manager.execute_query(investments_query, {'1': current_user['id']})
        
        # Calculate portfolio metrics
        total_invested = sum(float(inv['amount']) for inv in investments)
        total_current_value = 0.0
        active_investments = len(investments)
        
        for inv in investments:
            # Calculate current value based on fund performance
            fund_share_price = float(inv['fund_current_value']) / float(inv['initial_capital']) if inv['initial_capital'] > 0 else 1.0
            current_value = float(inv['shares_acquired']) * fund_share_price
            total_current_value += current_value
        
        total_return = total_current_value - total_invested
        total_return_percentage = (total_return / total_invested * 100) if total_invested > 0 else 0.0
        
        # Get total investments count (including inactive)
        total_investments_query = """
            SELECT COUNT(*) as total_count FROM investments WHERE investor_id = $1
        """
        total_result = await db_manager.execute_query(total_investments_query, {'1': current_user['id']})
        total_investments = total_result[0]['total_count'] if total_result else 0
        
        return PortfolioSummaryResponse(
            investor_id=str(current_user['id']),
            total_invested=total_invested,
            total_current_value=total_current_value,
            total_return=total_return,
            total_return_percentage=total_return_percentage,
            active_investments=active_investments,
            total_investments=total_investments,
            created_at=datetime.now(datetime.UTC).isoformat(),
            updated_at=datetime.now(datetime.UTC).isoformat()
        )
        
    except Exception as e:
        logger.error(f"Failed to get portfolio summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get portfolio summary: {str(e)}"
        )

@router.get("/allocations", response_model=List[FundAllocationResponse])
async def get_fund_allocations(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get fund allocations for the current user's portfolio."""
    try:
        db_manager = await get_db_manager()
        
        # Get all active investments with fund details
        investments_query = """
            SELECT i.*, f.name as fund_name, f.fund_type, f.current_value as fund_current_value, f.initial_capital
            FROM investments i
            JOIN funds f ON i.fund_id = f.id
            WHERE i.investor_id = $1 AND i.status = 'active'
        """
        investments = await db_manager.execute_query(investments_query, {'1': current_user['id']})
        
        # Group by fund and calculate allocations
        fund_allocations = {}
        total_portfolio_value = 0.0
        
        for inv in investments:
            fund_id = inv['fund_id']
            fund_share_price = float(inv['fund_current_value']) / float(inv['initial_capital']) if inv['initial_capital'] > 0 else 1.0
            current_value = float(inv['shares_acquired']) * fund_share_price
            
            if fund_id not in fund_allocations:
                fund_allocations[fund_id] = {
                    'fund_id': fund_id,
                    'fund_name': inv['fund_name'],
                    'fund_type': inv['fund_type'],
                    'invested_amount': 0.0,
                    'current_value': 0.0,
                    'shares_owned': 0.0,
                    'share_price': fund_share_price
                }
            
            fund_allocations[fund_id]['invested_amount'] += float(inv['amount'])
            fund_allocations[fund_id]['current_value'] += current_value
            fund_allocations[fund_id]['shares_owned'] += float(inv['shares_acquired'])
            total_portfolio_value += current_value
        
        # Calculate allocation percentages and returns
        allocations = []
        for fund_id, allocation in fund_allocations.items():
            allocation_percentage = (allocation['current_value'] / total_portfolio_value * 100) if total_portfolio_value > 0 else 0.0
            return_amount = allocation['current_value'] - allocation['invested_amount']
            return_percentage = (return_amount / allocation['invested_amount'] * 100) if allocation['invested_amount'] > 0 else 0.0
            
            allocations.append(FundAllocationResponse(
                fund_id=str(fund_id),
                fund_name=allocation['fund_name'],
                fund_type=allocation['fund_type'],
                invested_amount=allocation['invested_amount'],
                current_value=allocation['current_value'],
                allocation_percentage=allocation_percentage,
                return_amount=return_amount,
                return_percentage=return_percentage,
                shares_owned=allocation['shares_owned'],
                share_price=allocation['share_price']
            ))
        
        # Sort by allocation percentage (descending)
        allocations.sort(key=lambda x: x.allocation_percentage, reverse=True)
        
        return allocations
        
    except Exception as e:
        logger.error(f"Failed to get fund allocations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get fund allocations: {str(e)}"
        )

@router.get("/analytics", response_model=PortfolioAnalyticsResponse)
async def get_portfolio_analytics(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get comprehensive portfolio analytics."""
    try:
        # Get portfolio summary
        summary = await get_portfolio_summary(current_user)
        
        # Get fund allocations
        allocations = await get_fund_allocations(current_user)
        
        # Calculate additional risk metrics
        risk_metrics = {
            "diversification_score": min(len(allocations) * 20, 100),  # Simple diversification score
            "concentration_risk": max([alloc.allocation_percentage for alloc in allocations], default=0),
            "portfolio_beta": 1.0,  # Placeholder - would need market data
            "max_drawdown": 0.0,  # Placeholder - would need historical data
            "var_95": 0.0  # Placeholder - would need historical data
        }
        
        # Create mock performance data
        performance = PortfolioPerformanceResponse(
            period="1M",
            start_date=datetime.now(datetime.UTC).replace(day=1).isoformat(),
            end_date=datetime.now(datetime.UTC).isoformat(),
            total_return=summary.total_return,
            total_return_percentage=summary.total_return_percentage,
            best_performing_fund=allocations[0].fund_name if allocations else None,
            worst_performing_fund=allocations[-1].fund_name if allocations else None,
            volatility=0.15,
            sharpe_ratio=1.2
        )
        
        return PortfolioAnalyticsResponse(
            summary=summary,
            performance=performance,
            fund_allocations=allocations,
            risk_metrics=risk_metrics
        )
        
    except Exception as e:
        logger.error(f"Failed to get portfolio analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get portfolio analytics: {str(e)}"
        )