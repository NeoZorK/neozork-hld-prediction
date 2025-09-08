"""Investor API - RESTful API endpoints for investor portal"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import uuid

logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter(prefix="/api/v1/investors", tags=["investors"])
security = HTTPBearer()


class WidgetType(str, Enum):
    """Widget type enumeration."""
    PORTFOLIO_VALUE = "portfolio_value"
    PERFORMANCE_CHART = "performance_chart"
    RISK_METRICS = "risk_metrics"
    POSITIONS = "positions"
    TRANSACTIONS = "transactions"
    NEWS = "news"
    ALERTS = "alerts"


class MessageType(str, Enum):
    """Message type enumeration."""
    PERFORMANCE_UPDATE = "performance_update"
    RISK_ALERT = "risk_alert"
    MARKET_UPDATE = "market_update"
    FUND_ANNOUNCEMENT = "fund_announcement"
    SYSTEM_NOTIFICATION = "system_notification"


class CreateDashboardRequest(BaseModel):
    """Request model for creating a dashboard."""
    layout: str = Field(default="standard", description="Dashboard layout")
    template: str = Field(default="default", description="Dashboard template")


class DashboardResponse(BaseModel):
    """Response model for dashboard data."""
    dashboard_id: str
    investor_id: str
    layout: str
    theme: str
    auto_refresh: bool
    refresh_interval: int
    widgets: List[Dict[str, Any]]
    last_updated: datetime


class MessageResponse(BaseModel):
    """Response model for messages."""
    message_id: str
    message_type: MessageType
    subject: str
    content: str
    priority: int
    created_at: datetime
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None


class InvestorAPI:
    """Investor portal API endpoints."""
    
    def __init__(self):
        self.dashboard = None  # Will be injected
        self.monitoring_system = None  # Will be injected
        self.communication_system = None  # Will be injected
        self.report_generator = None  # Will be injected
        
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
        """Get current authenticated user."""
        # TODO: Implement JWT token validation
        return "user_123"  # Placeholder
    
    @router.post("/dashboard", response_model=DashboardResponse, status_code=201)
    async def create_dashboard(
        self,
        request: CreateDashboardRequest,
        current_user: str = Depends(get_current_user)
    ) -> DashboardResponse:
        """Create a new dashboard for investor."""
        try:
            result = await self.dashboard.create_dashboard(
                investor_id=current_user,
                layout=request.layout,
                template=request.template
            )
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            dashboard_config = result['dashboard_config']
            
            return DashboardResponse(
                dashboard_id=dashboard_config['dashboard_id'],
                investor_id=dashboard_config['investor_id'],
                layout=dashboard_config['layout'],
                theme=dashboard_config['theme'],
                auto_refresh=dashboard_config['auto_refresh'],
                refresh_interval=dashboard_config['refresh_interval'],
                widgets=[],  # Will be populated when getting dashboard data
                last_updated=dashboard_config['updated_at']
            )
            
        except Exception as e:
            logger.error(f"Failed to create dashboard: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/dashboard/{dashboard_id}", response_model=DashboardResponse)
    async def get_dashboard(
        self,
        dashboard_id: str = Path(..., description="Dashboard ID"),
        current_user: str = Depends(get_current_user)
    ) -> DashboardResponse:
        """Get dashboard data."""
        try:
            result = await self.dashboard.get_dashboard_data(dashboard_id)
            
            if 'error' in result:
                raise HTTPException(status_code=404, detail=result['error'])
            
            return DashboardResponse(
                dashboard_id=result['dashboard_id'],
                investor_id=result['investor_id'],
                layout=result['layout'],
                theme=result['theme'],
                auto_refresh=result['auto_refresh'],
                refresh_interval=result['refresh_interval'],
                widgets=result['widgets'],
                last_updated=result['last_updated']
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get dashboard: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.post("/dashboard/{dashboard_id}/refresh")
    async def refresh_dashboard(
        self,
        dashboard_id: str = Path(..., description="Dashboard ID"),
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Refresh dashboard data."""
        try:
            result = await self.dashboard.refresh_dashboard(dashboard_id)
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return {
                'status': 'success',
                'message': 'Dashboard refreshed successfully',
                'data': result
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to refresh dashboard: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/alerts", response_model=List[Dict[str, Any]])
    async def get_alerts(
        self,
        unread_only: bool = Query(False, description="Show only unread alerts"),
        current_user: str = Depends(get_current_user)
    ) -> List[Dict[str, Any]]:
        """Get investor alerts."""
        try:
            result = await self.monitoring_system.get_investor_alerts(current_user, unread_only)
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return result['alerts']
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get alerts: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.post("/alerts/{alert_id}/acknowledge")
    async def acknowledge_alert(
        self,
        alert_id: str = Path(..., description="Alert ID"),
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Acknowledge an alert."""
        try:
            result = await self.monitoring_system.acknowledge_alert(current_user, alert_id)
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return {
                'status': 'success',
                'message': 'Alert acknowledged successfully'
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to acknowledge alert: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/messages", response_model=List[MessageResponse])
    async def get_messages(
        self,
        message_type: Optional[MessageType] = Query(None, description="Filter by message type"),
        unread_only: bool = Query(False, description="Show only unread messages"),
        current_user: str = Depends(get_current_user)
    ) -> List[MessageResponse]:
        """Get investor messages."""
        try:
            result = await self.communication_system.get_investor_messages(
                current_user, message_type, unread_only
            )
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            messages = []
            for msg_data in result['messages']:
                messages.append(MessageResponse(
                    message_id=msg_data['message_id'],
                    message_type=msg_data['message_type'],
                    subject=msg_data['subject'],
                    content=msg_data['content'],
                    priority=msg_data['priority'],
                    created_at=msg_data['created_at'],
                    sent_at=msg_data.get('sent_at'),
                    read_at=msg_data.get('read_at')
                ))
            
            return messages
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get messages: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.post("/messages/{message_id}/read")
    async def mark_message_read(
        self,
        message_id: str = Path(..., description="Message ID"),
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Mark a message as read."""
        try:
            result = await self.communication_system.mark_message_read(current_user, message_id)
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return {
                'status': 'success',
                'message': 'Message marked as read'
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to mark message as read: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/reports/performance")
    async def get_performance_report(
        self,
        period_days: int = Query(30, description="Period in days", ge=1, le=365),
        format_type: str = Query("json", description="Report format"),
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Generate performance report for investor."""
        try:
            result = await self.report_generator.generate_performance_report(
                current_user, period_days, format_type
            )
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return {
                'status': 'success',
                'data': result
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to generate performance report: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/reports/portfolio")
    async def get_portfolio_report(
        self,
        format_type: str = Query("json", description="Report format"),
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Generate portfolio report for investor."""
        try:
            result = await self.report_generator.generate_portfolio_report(
                current_user, format_type
            )
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return {
                'status': 'success',
                'data': result
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to generate portfolio report: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/reports/tax")
    async def get_tax_report(
        self,
        tax_year: int = Query(None, description="Tax year"),
        format_type: str = Query("json", description="Report format"),
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Generate tax report for investor."""
        try:
            result = await self.report_generator.generate_tax_report(
                current_user, tax_year, format_type
            )
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return {
                'status': 'success',
                'data': result
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to generate tax report: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")


# Create API instance
investor_api = InvestorAPI()

# Add routes to router
router.add_api_route("/dashboard", investor_api.create_dashboard, methods=["POST"])
router.add_api_route("/dashboard/{dashboard_id}", investor_api.get_dashboard, methods=["GET"])
router.add_api_route("/dashboard/{dashboard_id}/refresh", investor_api.refresh_dashboard, methods=["POST"])
router.add_api_route("/alerts", investor_api.get_alerts, methods=["GET"])
router.add_api_route("/alerts/{alert_id}/acknowledge", investor_api.acknowledge_alert, methods=["POST"])
router.add_api_route("/messages", investor_api.get_messages, methods=["GET"])
router.add_api_route("/messages/{message_id}/read", investor_api.mark_message_read, methods=["POST"])
router.add_api_route("/reports/performance", investor_api.get_performance_report, methods=["GET"])
router.add_api_route("/reports/portfolio", investor_api.get_portfolio_report, methods=["GET"])
router.add_api_route("/reports/tax", investor_api.get_tax_report, methods=["GET"])