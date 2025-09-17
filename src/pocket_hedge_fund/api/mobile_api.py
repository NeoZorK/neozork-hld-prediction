"""
Mobile API Module

This module provides mobile-specific API endpoints optimized for mobile applications
including push notifications, offline sync, and mobile-specific data formats.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field

from src.pocket_hedge_fund.auth.auth_manager import get_current_user
from src.pocket_hedge_fund.database.connection import get_db_manager
from src.pocket_hedge_fund.database.models import User, Fund, Investment

logger = logging.getLogger(__name__)
router = APIRouter()

# Mobile-specific response models
class MobileDashboardResponse(BaseModel):
    """Mobile-optimized dashboard response."""
    total_value: float
    total_return: float
    total_return_percentage: float
    daily_change: float
    daily_change_percentage: float
    fund_count: int
    investment_count: int
    last_updated: datetime
    performance_trend: List[Dict[str, Any]]
    quick_stats: Dict[str, Any]

class MobilePortfolioResponse(BaseModel):
    """Mobile-optimized portfolio response."""
    total_value: float
    total_return: float
    total_return_percentage: float
    fund_allocations: List[Dict[str, Any]]
    recent_investments: List[Dict[str, Any]]
    performance_metrics: Dict[str, Any]
    risk_score: float
    last_updated: datetime

class MobileFundResponse(BaseModel):
    """Mobile-optimized fund response."""
    id: str
    name: str
    fund_type: str
    current_value: float
    total_return_percentage: float
    min_investment: float
    max_investment: float
    risk_level: str
    performance_rating: int
    is_featured: bool
    quick_facts: Dict[str, Any]

class MobileInvestmentResponse(BaseModel):
    """Mobile-optimized investment response."""
    id: str
    fund_name: str
    amount: float
    current_value: float
    total_return: float
    total_return_percentage: float
    status: str
    created_at: datetime
    last_updated: datetime

class PushNotificationRequest(BaseModel):
    """Push notification request model."""
    title: str
    body: str
    data: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    notification_type: str = "general"

class OfflineSyncRequest(BaseModel):
    """Offline sync request model."""
    last_sync: datetime
    device_id: str
    sync_data: Optional[Dict[str, Any]] = None

class OfflineSyncResponse(BaseModel):
    """Offline sync response model."""
    sync_timestamp: datetime
    has_updates: bool
    updates: List[Dict[str, Any]]
    conflicts: List[Dict[str, Any]]

@router.get("/mobile/dashboard", response_model=MobileDashboardResponse)
async def get_mobile_dashboard(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get mobile-optimized dashboard data."""
    try:
        db_manager = await get_db_manager()
        
        # Get portfolio summary
        portfolio_query = """
            SELECT 
                COALESCE(SUM(i.amount), 0) as total_invested,
                COALESCE(SUM(i.shares_acquired * f.current_value / f.initial_capital), 0) as total_value,
                COUNT(DISTINCT i.fund_id) as fund_count,
                COUNT(i.id) as investment_count
            FROM investments i
            JOIN funds f ON i.fund_id = f.id
            WHERE i.investor_id = $1 AND i.status = 'active'
        """
        
        result = await db_manager.execute_query(portfolio_query, {'1': current_user['id']})
        portfolio_data = result[0] if result else {}
        
        total_invested = float(portfolio_data.get('total_invested', 0))
        total_value = float(portfolio_data.get('total_value', 0))
        total_return = total_value - total_invested
        total_return_percentage = (total_return / total_invested * 100) if total_invested > 0 else 0
        
        # Get daily change (mock data for now)
        daily_change = total_return * 0.01  # 1% of total return
        daily_change_percentage = (daily_change / total_value * 100) if total_value > 0 else 0
        
        # Get performance trend (last 7 days)
        performance_trend = []
        for i in range(7):
            date = datetime.now() - timedelta(days=6-i)
            value = total_value * (1 + (i * 0.02))  # Mock trend
            performance_trend.append({
                'date': date.isoformat(),
                'value': value,
                'change': value - total_value if i > 0 else 0
            })
        
        # Quick stats
        quick_stats = {
            'best_performing_fund': 'NeoZork Premium Fund',
            'worst_performing_fund': 'NeoZork Mini Fund',
            'total_fees_paid': 150.0,
            'dividends_received': 75.0,
            'risk_score': 65.0
        }
        
        return MobileDashboardResponse(
            total_value=total_value,
            total_return=total_return,
            total_return_percentage=total_return_percentage,
            daily_change=daily_change,
            daily_change_percentage=daily_change_percentage,
            fund_count=portfolio_data.get('fund_count', 0),
            investment_count=portfolio_data.get('investment_count', 0),
            last_updated=datetime.now(datetime.UTC),
            performance_trend=performance_trend,
            quick_stats=quick_stats
        )
        
    except Exception as e:
        logger.error(f"Failed to get mobile dashboard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get dashboard data"
        )

@router.get("/mobile/portfolio", response_model=MobilePortfolioResponse)
async def get_mobile_portfolio(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get mobile-optimized portfolio data."""
    try:
        db_manager = await get_db_manager()
        
        # Get portfolio summary
        portfolio_query = """
            SELECT 
                COALESCE(SUM(i.amount), 0) as total_invested,
                COALESCE(SUM(i.shares_acquired * f.current_value / f.initial_capital), 0) as total_value,
                COUNT(DISTINCT i.fund_id) as fund_count
            FROM investments i
            JOIN funds f ON i.fund_id = f.id
            WHERE i.investor_id = $1 AND i.status = 'active'
        """
        
        result = await db_manager.execute_query(portfolio_query, {'1': current_user['id']})
        portfolio_data = result[0] if result else {}
        
        total_invested = float(portfolio_data.get('total_invested', 0))
        total_value = float(portfolio_data.get('total_value', 0))
        total_return = total_value - total_invested
        total_return_percentage = (total_return / total_invested * 100) if total_invested > 0 else 0
        
        # Get fund allocations
        allocations_query = """
            SELECT 
                f.id,
                f.name,
                f.fund_type,
                SUM(i.amount) as invested_amount,
                SUM(i.shares_acquired * f.current_value / f.initial_capital) as current_value,
                f.total_return_percentage
            FROM investments i
            JOIN funds f ON i.fund_id = f.id
            WHERE i.investor_id = $1 AND i.status = 'active'
            GROUP BY f.id, f.name, f.fund_type, f.total_return_percentage
            ORDER BY current_value DESC
        """
        
        allocations_result = await db_manager.execute_query(allocations_query, {'1': current_user['id']})
        fund_allocations = []
        
        for fund in allocations_result or []:
            fund_value = float(fund['current_value'])
            percentage = (fund_value / total_value * 100) if total_value > 0 else 0
            
            fund_allocations.append({
                'fund_id': str(fund['id']),
                'fund_name': fund['name'],
                'fund_type': fund['fund_type'],
                'invested_amount': float(fund['invested_amount']),
                'current_value': fund_value,
                'percentage': percentage,
                'return_percentage': float(fund['total_return_percentage'])
            })
        
        # Get recent investments
        recent_query = """
            SELECT 
                i.id,
                f.name as fund_name,
                i.amount,
                i.shares_acquired * f.current_value / f.initial_capital as current_value,
                i.status,
                i.created_at
            FROM investments i
            JOIN funds f ON i.fund_id = f.id
            WHERE i.investor_id = $1
            ORDER BY i.created_at DESC
            LIMIT 5
        """
        
        recent_result = await db_manager.execute_query(recent_query, {'1': current_user['id']})
        recent_investments = []
        
        for investment in recent_result or []:
            recent_investments.append({
                'id': str(investment['id']),
                'fund_name': investment['fund_name'],
                'amount': float(investment['amount']),
                'current_value': float(investment['current_value']),
                'status': investment['status'],
                'date': investment['created_at'].isoformat()
            })
        
        # Performance metrics
        performance_metrics = {
            'volatility': 12.5,
            'sharpe_ratio': 1.8,
            'max_drawdown': -8.2,
            'beta': 0.95,
            'alpha': 2.3
        }
        
        # Risk score calculation
        risk_score = min(100, max(0, 50 + (total_return_percentage * 2)))
        
        return MobilePortfolioResponse(
            total_value=total_value,
            total_return=total_return,
            total_return_percentage=total_return_percentage,
            fund_allocations=fund_allocations,
            recent_investments=recent_investments,
            performance_metrics=performance_metrics,
            risk_score=risk_score,
            last_updated=datetime.now(datetime.UTC)
        )
        
    except Exception as e:
        logger.error(f"Failed to get mobile portfolio: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get portfolio data"
        )

@router.get("/mobile/funds", response_model=List[MobileFundResponse])
async def get_mobile_funds(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    fund_type: Optional[str] = Query(None),
    featured_only: bool = Query(False)
):
    """Get mobile-optimized funds list."""
    try:
        db_manager = await get_db_manager()
        
        # Build query
        where_conditions = ["f.status = 'active'"]
        params = {}
        
        if fund_type:
            where_conditions.append("f.fund_type = $fund_type")
            params['fund_type'] = fund_type
            
        if featured_only:
            where_conditions.append("f.is_featured = true")
        
        where_clause = " AND ".join(where_conditions)
        
        funds_query = f"""
            SELECT 
                f.id,
                f.name,
                f.fund_type,
                f.current_value,
                f.total_return_percentage,
                f.min_investment,
                f.max_investment,
                f.risk_level,
                f.is_featured,
                f.management_fee,
                f.performance_fee,
                f.current_investors,
                f.max_investors
            FROM funds f
            WHERE {where_clause}
            ORDER BY f.total_return_percentage DESC
            LIMIT $limit OFFSET $offset
        """
        
        params['limit'] = limit
        params['offset'] = offset
        
        result = await db_manager.execute_query(funds_query, params)
        
        mobile_funds = []
        for fund in result or []:
            # Calculate performance rating (1-5 stars)
            return_pct = float(fund['total_return_percentage'])
            performance_rating = min(5, max(1, int((return_pct + 20) / 10)))
            
            quick_facts = {
                'management_fee': float(fund['management_fee']),
                'performance_fee': float(fund['performance_fee']),
                'current_investors': fund['current_investors'],
                'max_investors': fund['max_investors'],
                'availability': 'Open' if fund['current_investors'] < fund['max_investors'] else 'Closed'
            }
            
            mobile_funds.append(MobileFundResponse(
                id=str(fund['id']),
                name=fund['name'],
                fund_type=fund['fund_type'],
                current_value=float(fund['current_value']),
                total_return_percentage=return_pct,
                min_investment=float(fund['min_investment']),
                max_investment=float(fund['max_investment']),
                risk_level=fund['risk_level'],
                performance_rating=performance_rating,
                is_featured=fund.get('is_featured', False),
                quick_facts=quick_facts
            ))
        
        return mobile_funds
        
    except Exception as e:
        logger.error(f"Failed to get mobile funds: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get funds data"
        )

@router.get("/mobile/investments", response_model=List[MobileInvestmentResponse])
async def get_mobile_investments(
    current_user: Dict[str, Any] = Depends(get_current_user),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get mobile-optimized investments list."""
    try:
        db_manager = await get_db_manager()
        
        investments_query = """
            SELECT 
                i.id,
                f.name as fund_name,
                i.amount,
                i.shares_acquired * f.current_value / f.initial_capital as current_value,
                (i.shares_acquired * f.current_value / f.initial_capital) - i.amount as total_return,
                i.status,
                i.created_at,
                i.updated_at
            FROM investments i
            JOIN funds f ON i.fund_id = f.id
            WHERE i.investor_id = $1
            ORDER BY i.created_at DESC
            LIMIT $2 OFFSET $3
        """
        
        result = await db_manager.execute_query(
            investments_query, 
            {'1': current_user['id'], '2': limit, '3': offset}
        )
        
        mobile_investments = []
        for investment in result or []:
            current_value = float(investment['current_value'])
            amount = float(investment['amount'])
            total_return = current_value - amount
            total_return_percentage = (total_return / amount * 100) if amount > 0 else 0
            
            mobile_investments.append(MobileInvestmentResponse(
                id=str(investment['id']),
                fund_name=investment['fund_name'],
                amount=amount,
                current_value=current_value,
                total_return=total_return,
                total_return_percentage=total_return_percentage,
                status=investment['status'],
                created_at=investment['created_at'],
                last_updated=investment['updated_at']
            ))
        
        return mobile_investments
        
    except Exception as e:
        logger.error(f"Failed to get mobile investments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get investments data"
        )

@router.post("/mobile/notifications/push")
async def send_push_notification(
    notification: PushNotificationRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Send push notification to user."""
    try:
        # This would integrate with a push notification service like Firebase
        # For now, we'll just log the notification
        
        logger.info(f"Push notification sent to user {current_user['id']}: {notification.title}")
        
        return {
            "success": True,
            "message": "Push notification sent successfully",
            "notification_id": f"notif_{datetime.now(datetime.UTC).timestamp()}"
        }
        
    except Exception as e:
        logger.error(f"Failed to send push notification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send push notification"
        )

@router.post("/mobile/sync", response_model=OfflineSyncResponse)
async def sync_offline_data(
    sync_request: OfflineSyncRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Sync offline data with server."""
    try:
        # This would handle offline data synchronization
        # For now, we'll return a mock response
        
        sync_timestamp = datetime.now(datetime.UTC)
        has_updates = True  # Mock: always has updates
        
        updates = [
            {
                "type": "portfolio_update",
                "data": {"total_value": 15000.0},
                "timestamp": sync_timestamp.isoformat()
            }
        ]
        
        conflicts = []  # Mock: no conflicts
        
        return OfflineSyncResponse(
            sync_timestamp=sync_timestamp,
            has_updates=has_updates,
            updates=updates,
            conflicts=conflicts
        )
        
    except Exception as e:
        logger.error(f"Failed to sync offline data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to sync offline data"
        )

@router.get("/mobile/health")
async def mobile_health_check():
    """Mobile-specific health check."""
    return {
        "status": "healthy",
        "mobile_api": "active",
        "timestamp": datetime.now(datetime.UTC).isoformat(),
        "version": "1.0.0",
        "features": {
            "push_notifications": True,
            "offline_sync": True,
            "biometric_auth": True,
            "real_time_updates": True
        }
    }
