"""
Enhanced Portfolio API for Pocket Hedge Fund.

This module provides enhanced portfolio management API endpoints with
real trading functionality and risk management.
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
from ..portfolio.portfolio_manager import PortfolioManager
from ..data.data_manager import DataManager

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Create router
router = APIRouter(prefix="/portfolio", tags=["Enhanced Portfolio Management"])

class PortfolioAPI:
    """Enhanced Portfolio API class for dependency injection."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.router = router
        self.portfolio_managers = {}  # Cache portfolio managers by fund_id
        self.data_manager = DataManager()

# Pydantic models

class PositionRequest(BaseModel):
    fund_id: str
    symbol: str
    quantity: float
    price: float
    position_type: str = "LONG"  # LONG or SHORT
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

class ClosePositionRequest(BaseModel):
    fund_id: str
    symbol: str
    quantity: Optional[float] = None  # If None, close entire position
    price: float

class RebalanceRequest(BaseModel):
    fund_id: str
    target_weights: Dict[str, float]  # symbol -> weight
    current_prices: Dict[str, float]  # symbol -> current price

class RiskLimitsRequest(BaseModel):
    fund_id: str
    max_position_size: Optional[float] = None
    max_sector_exposure: Optional[float] = None
    max_drawdown: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

# API Endpoints

@router.post("/create", response_model=Dict[str, Any])
async def create_portfolio(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    fund_id: str = "default-fund",
    initial_capital: float = 100000.0
) -> Dict[str, Any]:
    """Create a new portfolio for a fund."""
    try:
        logger.info(f"Creating portfolio for fund {fund_id}")
        
        # Create portfolio manager
        portfolio_manager = PortfolioManager(fund_id, initial_capital)
        
        # Store in cache (in production, this would be in database)
        portfolio_api = PortfolioAPI(None)
        portfolio_api.portfolio_managers[fund_id] = portfolio_manager
        
        return {
            'status': 'success',
            'message': f'Portfolio created for fund {fund_id}',
            'fund_id': fund_id,
            'initial_capital': initial_capital,
            'current_capital': initial_capital,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error creating portfolio: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create portfolio: {str(e)}"
        )

@router.post("/add-position", response_model=Dict[str, Any])
async def add_position(
    position_request: PositionRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Add a position to the portfolio."""
    try:
        logger.info(f"Adding position: {position_request.symbol} to fund {position_request.fund_id}")
        
        # Get portfolio manager
        portfolio_api = PortfolioAPI(None)
        if position_request.fund_id not in portfolio_api.portfolio_managers:
            # Create portfolio if it doesn't exist
            portfolio_manager = PortfolioManager(position_request.fund_id)
            portfolio_api.portfolio_managers[position_request.fund_id] = portfolio_manager
        
        portfolio_manager = portfolio_api.portfolio_managers[position_request.fund_id]
        
        # Add position
        result = await portfolio_manager.add_position(
            symbol=position_request.symbol,
            quantity=position_request.quantity,
            price=position_request.price,
            position_type=position_request.position_type,
            stop_loss=position_request.stop_loss,
            take_profit=position_request.take_profit
        )
        
        return {
            'status': 'success',
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error adding position: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add position: {str(e)}"
        )

@router.post("/close-position", response_model=Dict[str, Any])
async def close_position(
    close_request: ClosePositionRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Close a position in the portfolio."""
    try:
        logger.info(f"Closing position: {close_request.symbol} in fund {close_request.fund_id}")
        
        # Get portfolio manager
        portfolio_api = PortfolioAPI(None)
        if close_request.fund_id not in portfolio_api.portfolio_managers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Portfolio for fund {close_request.fund_id} not found"
            )
        
        portfolio_manager = portfolio_api.portfolio_managers[close_request.fund_id]
        
        # Close position
        result = await portfolio_manager.close_position(
            symbol=close_request.symbol,
            quantity=close_request.quantity,
            price=close_request.price
        )
        
        return {
            'status': 'success',
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error closing position: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to close position: {str(e)}"
        )

@router.get("/summary/{fund_id}", response_model=Dict[str, Any])
async def get_portfolio_summary(
    fund_id: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Get comprehensive portfolio summary."""
    try:
        logger.info(f"Getting portfolio summary for fund {fund_id}")
        
        # Get portfolio manager
        portfolio_api = PortfolioAPI(None)
        if fund_id not in portfolio_api.portfolio_managers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Portfolio for fund {fund_id} not found"
            )
        
        portfolio_manager = portfolio_api.portfolio_managers[fund_id]
        
        # Get summary
        summary = portfolio_manager.get_portfolio_summary()
        
        return {
            'status': 'success',
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting portfolio summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get portfolio summary: {str(e)}"
        )

@router.get("/performance/{fund_id}", response_model=Dict[str, Any])
async def get_portfolio_performance(
    fund_id: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Get portfolio performance metrics."""
    try:
        logger.info(f"Getting portfolio performance for fund {fund_id}")
        
        # Get portfolio manager
        portfolio_api = PortfolioAPI(None)
        if fund_id not in portfolio_api.portfolio_managers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Portfolio for fund {fund_id} not found"
            )
        
        portfolio_manager = portfolio_api.portfolio_managers[fund_id]
        
        # Get performance metrics
        performance = portfolio_manager.get_performance_metrics()
        
        return {
            'status': 'success',
            'performance': performance,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting portfolio performance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get portfolio performance: {str(e)}"
        )

@router.post("/update-prices", response_model=Dict[str, Any])
async def update_position_prices(
    fund_id: str,
    current_prices: Dict[str, float],
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Update current prices for all positions."""
    try:
        logger.info(f"Updating prices for fund {fund_id}")
        
        # Get portfolio manager
        portfolio_api = PortfolioAPI(None)
        if fund_id not in portfolio_api.portfolio_managers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Portfolio for fund {fund_id} not found"
            )
        
        portfolio_manager = portfolio_api.portfolio_managers[fund_id]
        
        # Update prices
        result = await portfolio_manager.update_position_prices(current_prices)
        
        return {
            'status': 'success',
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating prices: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update prices: {str(e)}"
        )

@router.post("/rebalance", response_model=Dict[str, Any])
async def rebalance_portfolio(
    rebalance_request: RebalanceRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Rebalance portfolio to target weights."""
    try:
        logger.info(f"Rebalancing portfolio for fund {rebalance_request.fund_id}")
        
        # Get portfolio manager
        portfolio_api = PortfolioAPI(None)
        if rebalance_request.fund_id not in portfolio_api.portfolio_managers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Portfolio for fund {rebalance_request.fund_id} not found"
            )
        
        portfolio_manager = portfolio_api.portfolio_managers[rebalance_request.fund_id]
        
        # Rebalance portfolio
        result = await portfolio_manager.rebalance_portfolio(
            rebalance_request.target_weights,
            rebalance_request.current_prices
        )
        
        return {
            'status': 'success',
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error rebalancing portfolio: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to rebalance portfolio: {str(e)}"
        )

@router.post("/risk-limits", response_model=Dict[str, Any])
async def update_risk_limits(
    risk_request: RiskLimitsRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Update risk limits for the portfolio."""
    try:
        logger.info(f"Updating risk limits for fund {risk_request.fund_id}")
        
        # Get portfolio manager
        portfolio_api = PortfolioAPI(None)
        if risk_request.fund_id not in portfolio_api.portfolio_managers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Portfolio for fund {risk_request.fund_id} not found"
            )
        
        portfolio_manager = portfolio_api.portfolio_managers[risk_request.fund_id]
        
        # Update risk limits
        updated_limits = {}
        if risk_request.max_position_size is not None:
            portfolio_manager.risk_limits['max_position_size'] = risk_request.max_position_size
            updated_limits['max_position_size'] = risk_request.max_position_size
        
        if risk_request.max_sector_exposure is not None:
            portfolio_manager.risk_limits['max_sector_exposure'] = risk_request.max_sector_exposure
            updated_limits['max_sector_exposure'] = risk_request.max_sector_exposure
        
        if risk_request.max_drawdown is not None:
            portfolio_manager.risk_limits['max_drawdown'] = risk_request.max_drawdown
            updated_limits['max_drawdown'] = risk_request.max_drawdown
        
        if risk_request.stop_loss is not None:
            portfolio_manager.risk_limits['stop_loss'] = risk_request.stop_loss
            updated_limits['stop_loss'] = risk_request.stop_loss
        
        if risk_request.take_profit is not None:
            portfolio_manager.risk_limits['take_profit'] = risk_request.take_profit
            updated_limits['take_profit'] = risk_request.take_profit
        
        return {
            'status': 'success',
            'message': 'Risk limits updated successfully',
            'updated_limits': updated_limits,
            'current_limits': portfolio_manager.risk_limits,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating risk limits: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update risk limits: {str(e)}"
        )

@router.get("/risk-limits/{fund_id}", response_model=Dict[str, Any])
async def get_risk_limits(
    fund_id: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Get current risk limits for the portfolio."""
    try:
        logger.info(f"Getting risk limits for fund {fund_id}")
        
        # Get portfolio manager
        portfolio_api = PortfolioAPI(None)
        if fund_id not in portfolio_api.portfolio_managers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Portfolio for fund {fund_id} not found"
            )
        
        portfolio_manager = portfolio_api.portfolio_managers[fund_id]
        
        return {
            'status': 'success',
            'fund_id': fund_id,
            'risk_limits': portfolio_manager.risk_limits,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting risk limits: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get risk limits: {str(e)}"
        )

@router.get("/health", response_model=Dict[str, str])
async def health_check() -> Dict[str, str]:
    """Health check endpoint for enhanced portfolio API."""
    return {"status": "healthy", "service": "enhanced-portfolio-api"}
