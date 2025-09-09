"""
Performance API for Pocket Hedge Fund.

This module provides REST API endpoints for performance tracking,
analytics, and reporting operations.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
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
router = APIRouter(prefix="/performance", tags=["Performance Tracking"])


# Pydantic models

class PerformanceMetrics(BaseModel):
    """Performance metrics model."""
    total_return: Decimal
    annualized_return: Decimal
    volatility: Decimal
    sharpe_ratio: Decimal
    max_drawdown: Decimal
    calmar_ratio: Decimal
    win_rate: Decimal
    profit_factor: Decimal
    sortino_ratio: Decimal
    var_95: Decimal
    cvar_95: Decimal


class PerformanceSnapshot(BaseModel):
    """Performance snapshot model."""
    fund_id: str
    date: datetime
    total_value: Decimal
    cash_balance: Decimal
    invested_value: Decimal
    unrealized_pnl: Decimal
    realized_pnl: Decimal
    daily_return: Decimal
    cumulative_return: Decimal
    drawdown: Decimal
    metrics: PerformanceMetrics


class PerformanceReport(BaseModel):
    """Performance report model."""
    fund_id: str
    period_start: datetime
    period_end: datetime
    total_return: Decimal
    annualized_return: Decimal
    volatility: Decimal
    sharpe_ratio: Decimal
    max_drawdown: Decimal
    win_rate: Decimal
    total_trades: int
    winning_trades: int
    losing_trades: int
    average_win: Decimal
    average_loss: Decimal
    profit_factor: Decimal
    metrics: PerformanceMetrics
    snapshots: List[PerformanceSnapshot]


class BenchmarkComparison(BaseModel):
    """Benchmark comparison model."""
    fund_id: str
    benchmark_symbol: str
    period_start: datetime
    period_end: datetime
    fund_return: Decimal
    benchmark_return: Decimal
    excess_return: Decimal
    tracking_error: Decimal
    information_ratio: Decimal
    beta: Decimal
    alpha: Decimal
    correlation: Decimal


# API endpoints

@router.get("/{fund_id}/metrics", response_model=PerformanceMetrics)
async def get_performance_metrics(
    fund_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    period_days: int = 365
) -> PerformanceMetrics:
    """
    Get performance metrics for a fund.
    
    Args:
        fund_id: Fund ID
        request: HTTP request
        current_user: Current authenticated user
        period_days: Number of days to analyze
        
    Returns:
        Performance metrics
        
    Raises:
        HTTPException: If metrics retrieval fails
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
        
        # Get performance data
        db_utils = DatabaseUtils(db_manager)
        metrics_data = await db_utils.get_performance_metrics(fund_id, period_days)
        
        if not metrics_data:
            # Return default metrics if no data available
            return PerformanceMetrics(
                total_return=Decimal('0.00'),
                annualized_return=Decimal('0.00'),
                volatility=Decimal('0.00'),
                sharpe_ratio=Decimal('0.00'),
                max_drawdown=Decimal('0.00'),
                calmar_ratio=Decimal('0.00'),
                win_rate=Decimal('0.00'),
                profit_factor=Decimal('0.00'),
                sortino_ratio=Decimal('0.00'),
                var_95=Decimal('0.00'),
                cvar_95=Decimal('0.00')
            )
        
        return PerformanceMetrics(
            total_return=metrics_data.get('total_return', Decimal('0.00')),
            annualized_return=metrics_data.get('annualized_return', Decimal('0.00')),
            volatility=metrics_data.get('volatility', Decimal('0.00')),
            sharpe_ratio=metrics_data.get('sharpe_ratio', Decimal('0.00')),
            max_drawdown=metrics_data.get('max_drawdown', Decimal('0.00')),
            calmar_ratio=metrics_data.get('calmar_ratio', Decimal('0.00')),
            win_rate=metrics_data.get('win_rate', Decimal('0.00')),
            profit_factor=metrics_data.get('profit_factor', Decimal('0.00')),
            sortino_ratio=metrics_data.get('sortino_ratio', Decimal('0.00')),
            var_95=metrics_data.get('var_95', Decimal('0.00')),
            cvar_95=metrics_data.get('cvar_95', Decimal('0.00'))
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get performance metrics"
        )


@router.get("/{fund_id}/snapshots", response_model=List[PerformanceSnapshot])
async def get_performance_snapshots(
    fund_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100
) -> List[PerformanceSnapshot]:
    """
    Get performance snapshots for a fund.
    
    Args:
        fund_id: Fund ID
        request: HTTP request
        current_user: Current authenticated user
        start_date: Start date for snapshots
        end_date: End date for snapshots
        limit: Maximum number of snapshots to return
        
    Returns:
        List of performance snapshots
        
    Raises:
        HTTPException: If snapshots retrieval fails
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
        
        # Set default dates if not provided
        if not end_date:
            end_date = datetime.utcnow()
        if not start_date:
            start_date = end_date - timedelta(days=365)
        
        # Get performance snapshots
        db_utils = DatabaseUtils(db_manager)
        snapshots_data = await db_utils.get_performance_snapshots(
            fund_id, start_date, end_date, limit
        )
        
        # Convert to response models
        snapshots = []
        for snapshot_data in snapshots_data:
            metrics = PerformanceMetrics(
                total_return=snapshot_data.get('total_return', Decimal('0.00')),
                annualized_return=snapshot_data.get('annualized_return', Decimal('0.00')),
                volatility=snapshot_data.get('volatility', Decimal('0.00')),
                sharpe_ratio=snapshot_data.get('sharpe_ratio', Decimal('0.00')),
                max_drawdown=snapshot_data.get('max_drawdown', Decimal('0.00')),
                calmar_ratio=snapshot_data.get('calmar_ratio', Decimal('0.00')),
                win_rate=snapshot_data.get('win_rate', Decimal('0.00')),
                profit_factor=snapshot_data.get('profit_factor', Decimal('0.00')),
                sortino_ratio=snapshot_data.get('sortino_ratio', Decimal('0.00')),
                var_95=snapshot_data.get('var_95', Decimal('0.00')),
                cvar_95=snapshot_data.get('cvar_95', Decimal('0.00'))
            )
            
            snapshots.append(PerformanceSnapshot(
                fund_id=snapshot_data['fund_id'],
                date=snapshot_data['date'],
                total_value=snapshot_data['total_value'],
                cash_balance=snapshot_data['cash_balance'],
                invested_value=snapshot_data['invested_value'],
                unrealized_pnl=snapshot_data['unrealized_pnl'],
                realized_pnl=snapshot_data['realized_pnl'],
                daily_return=snapshot_data['daily_return'],
                cumulative_return=snapshot_data['cumulative_return'],
                drawdown=snapshot_data['drawdown'],
                metrics=metrics
            ))
        
        return snapshots
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting performance snapshots: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get performance snapshots"
        )


@router.get("/{fund_id}/report", response_model=PerformanceReport)
async def get_performance_report(
    fund_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> PerformanceReport:
    """
    Get comprehensive performance report for a fund.
    
    Args:
        fund_id: Fund ID
        request: HTTP request
        current_user: Current authenticated user
        start_date: Start date for report
        end_date: End date for report
        
    Returns:
        Performance report
        
    Raises:
        HTTPException: If report generation fails
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
        
        # Set default dates if not provided
        if not end_date:
            end_date = datetime.utcnow()
        if not start_date:
            start_date = end_date - timedelta(days=365)
        
        # Get performance report
        db_utils = DatabaseUtils(db_manager)
        report_data = await db_utils.get_performance_report(fund_id, start_date, end_date)
        
        if not report_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No performance data available for the specified period"
            )
        
        # Build metrics
        metrics = PerformanceMetrics(
            total_return=report_data.get('total_return', Decimal('0.00')),
            annualized_return=report_data.get('annualized_return', Decimal('0.00')),
            volatility=report_data.get('volatility', Decimal('0.00')),
            sharpe_ratio=report_data.get('sharpe_ratio', Decimal('0.00')),
            max_drawdown=report_data.get('max_drawdown', Decimal('0.00')),
            calmar_ratio=report_data.get('calmar_ratio', Decimal('0.00')),
            win_rate=report_data.get('win_rate', Decimal('0.00')),
            profit_factor=report_data.get('profit_factor', Decimal('0.00')),
            sortino_ratio=report_data.get('sortino_ratio', Decimal('0.00')),
            var_95=report_data.get('var_95', Decimal('0.00')),
            cvar_95=report_data.get('cvar_95', Decimal('0.00'))
        )
        
        # Build snapshots
        snapshots = []
        for snapshot_data in report_data.get('snapshots', []):
            snapshot_metrics = PerformanceMetrics(
                total_return=snapshot_data.get('total_return', Decimal('0.00')),
                annualized_return=snapshot_data.get('annualized_return', Decimal('0.00')),
                volatility=snapshot_data.get('volatility', Decimal('0.00')),
                sharpe_ratio=snapshot_data.get('sharpe_ratio', Decimal('0.00')),
                max_drawdown=snapshot_data.get('max_drawdown', Decimal('0.00')),
                calmar_ratio=snapshot_data.get('calmar_ratio', Decimal('0.00')),
                win_rate=snapshot_data.get('win_rate', Decimal('0.00')),
                profit_factor=snapshot_data.get('profit_factor', Decimal('0.00')),
                sortino_ratio=snapshot_data.get('sortino_ratio', Decimal('0.00')),
                var_95=snapshot_data.get('var_95', Decimal('0.00')),
                cvar_95=snapshot_data.get('cvar_95', Decimal('0.00'))
            )
            
            snapshots.append(PerformanceSnapshot(
                fund_id=snapshot_data['fund_id'],
                date=snapshot_data['date'],
                total_value=snapshot_data['total_value'],
                cash_balance=snapshot_data['cash_balance'],
                invested_value=snapshot_data['invested_value'],
                unrealized_pnl=snapshot_data['unrealized_pnl'],
                realized_pnl=snapshot_data['realized_pnl'],
                daily_return=snapshot_data['daily_return'],
                cumulative_return=snapshot_data['cumulative_return'],
                drawdown=snapshot_data['drawdown'],
                metrics=snapshot_metrics
            ))
        
        return PerformanceReport(
            fund_id=report_data['fund_id'],
            period_start=start_date,
            period_end=end_date,
            total_return=report_data.get('total_return', Decimal('0.00')),
            annualized_return=report_data.get('annualized_return', Decimal('0.00')),
            volatility=report_data.get('volatility', Decimal('0.00')),
            sharpe_ratio=report_data.get('sharpe_ratio', Decimal('0.00')),
            max_drawdown=report_data.get('max_drawdown', Decimal('0.00')),
            win_rate=report_data.get('win_rate', Decimal('0.00')),
            total_trades=report_data.get('total_trades', 0),
            winning_trades=report_data.get('winning_trades', 0),
            losing_trades=report_data.get('losing_trades', 0),
            average_win=report_data.get('average_win', Decimal('0.00')),
            average_loss=report_data.get('average_loss', Decimal('0.00')),
            profit_factor=report_data.get('profit_factor', Decimal('0.00')),
            metrics=metrics,
            snapshots=snapshots
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting performance report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate performance report"
        )


@router.get("/{fund_id}/benchmark/{benchmark_symbol}", response_model=BenchmarkComparison)
async def get_benchmark_comparison(
    fund_id: str,
    benchmark_symbol: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> BenchmarkComparison:
    """
    Get benchmark comparison for a fund.
    
    Args:
        fund_id: Fund ID
        benchmark_symbol: Benchmark symbol (e.g., 'SPY', 'QQQ')
        request: HTTP request
        current_user: Current authenticated user
        start_date: Start date for comparison
        end_date: End date for comparison
        
    Returns:
        Benchmark comparison data
        
    Raises:
        HTTPException: If benchmark comparison fails
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
        
        # Set default dates if not provided
        if not end_date:
            end_date = datetime.utcnow()
        if not start_date:
            start_date = end_date - timedelta(days=365)
        
        # Get benchmark comparison
        db_utils = DatabaseUtils(db_manager)
        comparison_data = await db_utils.get_benchmark_comparison(
            fund_id, benchmark_symbol, start_date, end_date
        )
        
        if not comparison_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No benchmark data available for the specified period"
            )
        
        return BenchmarkComparison(
            fund_id=comparison_data['fund_id'],
            benchmark_symbol=comparison_data['benchmark_symbol'],
            period_start=start_date,
            period_end=end_date,
            fund_return=comparison_data.get('fund_return', Decimal('0.00')),
            benchmark_return=comparison_data.get('benchmark_return', Decimal('0.00')),
            excess_return=comparison_data.get('excess_return', Decimal('0.00')),
            tracking_error=comparison_data.get('tracking_error', Decimal('0.00')),
            information_ratio=comparison_data.get('information_ratio', Decimal('0.00')),
            beta=comparison_data.get('beta', Decimal('0.00')),
            alpha=comparison_data.get('alpha', Decimal('0.00')),
            correlation=comparison_data.get('correlation', Decimal('0.00'))
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting benchmark comparison: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get benchmark comparison"
        )


@router.post("/{fund_id}/snapshot", response_model=Dict[str, str])
async def create_performance_snapshot(
    fund_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(require_fund_manager)
) -> Dict[str, str]:
    """
    Create a performance snapshot for a fund.
    
    Args:
        fund_id: Fund ID
        request: HTTP request
        current_user: Current authenticated user
        
    Returns:
        Snapshot creation confirmation
        
    Raises:
        HTTPException: If snapshot creation fails
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
        
        # Create performance snapshot
        db_utils = DatabaseUtils(db_manager)
        result = await db_utils.create_performance_snapshot(fund_id)
        
        if result['status'] == 'error':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result['message']
            )
        
        logger.info(f"Performance snapshot created for fund: {fund_id}")
        
        return {
            'message': 'Performance snapshot created successfully'
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating performance snapshot: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create performance snapshot"
        )
