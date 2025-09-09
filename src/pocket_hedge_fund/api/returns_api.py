"""
Returns Calculation API for Pocket Hedge Fund

This module provides RESTful API endpoints for real-time return calculations
including investment returns, portfolio performance, and risk metrics.
"""

import asyncio
import logging
from datetime import datetime, date
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Query, Path
from fastapi import status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

from ..database.connection import get_db_manager
from ..auth.auth_manager import get_auth_manager, get_current_user
from ..services.return_calculator import get_return_calculator

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/returns", tags=["returns"])

# Security
security = HTTPBearer()

# Pydantic models for request/response
class InvestmentReturnResponse(BaseModel):
    """Response model for investment return calculation."""
    investment_id: str
    fund_name: str
    invested_amount: float
    current_value: float
    total_return: float
    total_return_percentage: float
    annualized_return: float
    days_held: int
    shares_owned: float
    current_share_price: float
    original_share_price: float
    last_updated: str

class PortfolioReturnResponse(BaseModel):
    """Response model for portfolio return calculation."""
    investor_id: str
    total_invested: float
    total_current_value: float
    total_return: float
    total_return_percentage: float
    investments: List[Dict[str, Any]]
    last_updated: str

class FundPerformanceResponse(BaseModel):
    """Response model for fund performance calculation."""
    fund_id: str
    fund_name: str
    fund_type: str
    initial_capital: float
    current_value: float
    total_return: float
    total_return_percentage: float
    annualized_return: float
    days_active: int
    investor_count: int
    total_investments: float
    management_fee: float
    performance_fee: float
    last_updated: str

class RiskMetricsResponse(BaseModel):
    """Response model for risk metrics calculation."""
    investor_id: str
    risk_metrics: Dict[str, Any]
    last_updated: str

# Returns API endpoints

@router.get("/investment/{investment_id}", response_model=InvestmentReturnResponse)
async def get_investment_return(
    investment_id: str = Path(..., description="Investment ID"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get real-time return calculation for a specific investment."""
    try:
        # Verify investment belongs to user
        db_manager = await get_db_manager()
        verify_query = """
            SELECT id FROM investments WHERE id = $1 AND investor_id = $2
        """
        investments = await db_manager.execute_query(verify_query, {'1': investment_id, '2': current_user['id']})
        
        if not investments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Investment not found or access denied"
            )
        
        # Calculate return
        return_calculator = await get_return_calculator()
        result = await return_calculator.calculate_investment_return(investment_id)
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        return InvestmentReturnResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get investment return: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get investment return: {str(e)}"
        )

@router.get("/portfolio", response_model=PortfolioReturnResponse)
async def get_portfolio_return(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get real-time return calculation for entire portfolio."""
    try:
        return_calculator = await get_return_calculator()
        result = await return_calculator.calculate_portfolio_return(current_user['id'])
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        return PortfolioReturnResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get portfolio return: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get portfolio return: {str(e)}"
        )

@router.get("/fund/{fund_id}", response_model=FundPerformanceResponse)
async def get_fund_performance(
    fund_id: str = Path(..., description="Fund ID"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get real-time performance calculation for a specific fund."""
    try:
        return_calculator = await get_return_calculator()
        result = await return_calculator.calculate_fund_performance(fund_id)
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["error"]
            )
        
        return FundPerformanceResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get fund performance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get fund performance: {str(e)}"
        )

@router.get("/risk-metrics", response_model=RiskMetricsResponse)
async def get_risk_metrics(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get risk metrics for investor's portfolio."""
    try:
        return_calculator = await get_return_calculator()
        result = await return_calculator.calculate_risk_metrics(current_user['id'])
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        return RiskMetricsResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get risk metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get risk metrics: {str(e)}"
        )

@router.get("/summary", response_model=Dict[str, Any])
async def get_returns_summary(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get comprehensive returns summary for investor."""
    try:
        return_calculator = await get_return_calculator()
        
        # Get portfolio return
        portfolio_result = await return_calculator.calculate_portfolio_return(current_user['id'])
        
        # Get risk metrics
        risk_result = await return_calculator.calculate_risk_metrics(current_user['id'])
        
        if "error" in portfolio_result or "error" in risk_result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to calculate returns summary"
            )
        
        return {
            "portfolio": portfolio_result,
            "risk_metrics": risk_result,
            "summary_generated_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get returns summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get returns summary: {str(e)}"
        )
