"""
NeoZork Pocket Hedge Fund - Dashboard Analytics API

This module provides RESTful API endpoints for dashboard analytics including:
- Dashboard management
- Analytics data retrieval
- Report generation
- Data export
- Real-time analytics
- Custom dashboards
- Widget management
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Body, WebSocket, WebSocketDisconnect
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import logging
import asyncio
import json

from ..analytics.dashboard_analytics import (
    DashboardAnalytics, AnalyticsType, TimeRange, ChartType, MetricType,
    AnalyticsMetric, ChartData, DashboardWidget, Dashboard, Report
)
from ..auth.jwt_manager import JWTManager
from ..config.database_manager import DatabaseManager
from ..config.config_manager import ConfigManager
from ..notifications.notification_manager import NotificationManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])

# Security
security = HTTPBearer()

# Global instances
dashboard_analytics = None
jwt_manager = None
notification_manager = None

async def get_dashboard_analytics() -> DashboardAnalytics:
    """Get dashboard analytics instance"""
    global dashboard_analytics
    if not dashboard_analytics:
        db_manager = DatabaseManager()
        config_manager = ConfigManager()
        notification_mgr = NotificationManager(db_manager, config_manager)
        
        await db_manager.initialize()
        await config_manager.initialize()
        await notification_mgr.initialize()
        
        dashboard_analytics = DashboardAnalytics(db_manager, config_manager, notification_mgr)
        await dashboard_analytics.initialize()
    
    return dashboard_analytics

async def get_jwt_manager() -> JWTManager:
    """Get JWT manager instance"""
    global jwt_manager
    if not jwt_manager:
        jwt_manager = JWTManager()
    
    return jwt_manager

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    jwt_mgr = await get_jwt_manager()
    
    try:
        payload = jwt_mgr.validate_token(credentials.credentials)
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Pydantic models

class DashboardCreateRequest(BaseModel):
    """Request model for creating dashboard"""
    name: str = Field(..., description="Dashboard name")
    description: str = Field(..., description="Dashboard description")
    widgets: List[Dict[str, Any]] = Field(default_factory=list, description="Dashboard widgets")
    layout: Optional[Dict[str, Any]] = Field(default=None, description="Dashboard layout")
    theme: str = Field(default="default", description="Dashboard theme")

class DashboardUpdateRequest(BaseModel):
    """Request model for updating dashboard"""
    name: Optional[str] = Field(default=None, description="Dashboard name")
    description: Optional[str] = Field(default=None, description="Dashboard description")
    widgets: Optional[List[Dict[str, Any]]] = Field(default=None, description="Dashboard widgets")
    layout: Optional[Dict[str, Any]] = Field(default=None, description="Dashboard layout")
    theme: Optional[str] = Field(default=None, description="Dashboard theme")

class DashboardResponse(BaseModel):
    """Response model for dashboard"""
    dashboard_id: str
    name: str
    description: str
    user_id: str
    widgets: List[Dict[str, Any]]
    layout: Dict[str, Any]
    theme: str
    created_at: datetime
    updated_at: datetime

class DashboardListResponse(BaseModel):
    """Response model for dashboard list"""
    dashboards: List[DashboardResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int

class AnalyticsDataResponse(BaseModel):
    """Response model for analytics data"""
    dashboard_id: Optional[str]
    user_id: str
    time_range: str
    generated_at: str
    metrics: Dict[str, List[Dict[str, Any]]]
    charts: Dict[str, List[Dict[str, Any]]]
    widgets: List[Dict[str, Any]]

class ReportGenerateRequest(BaseModel):
    """Request model for generating report"""
    name: str = Field(..., description="Report name")
    description: str = Field(..., description="Report description")
    report_type: str = Field(..., description="Report type")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Report parameters")
    format: str = Field(default="json", description="Report format")

class ReportResponse(BaseModel):
    """Response model for report"""
    report_id: str
    name: str
    description: str
    report_type: str
    parameters: Dict[str, Any]
    data: Dict[str, Any]
    format: str
    generated_at: datetime
    expires_at: Optional[datetime]
    user_id: str

class AnalyticsSummaryResponse(BaseModel):
    """Response model for analytics summary"""
    user_id: str
    time_range: str
    generated_at: str
    summary: Dict[str, Any]

class ExportRequest(BaseModel):
    """Request model for data export"""
    format: str = Field(default="json", description="Export format")
    time_range: str = Field(default="1m", description="Time range")

# API Endpoints

@router.get("/dashboard", response_model=AnalyticsDataResponse)
async def get_dashboard_data(
    dashboard_id: Optional[str] = Query(None, description="Dashboard ID"),
    time_range: str = Query("1m", description="Time range"),
    filters: Optional[str] = Query(None, description="JSON filters"),
    current_user: dict = Depends(get_current_user)
):
    """Get dashboard analytics data"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        # Parse time range
        try:
            time_range_enum = TimeRange(time_range)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid time range")
        
        # Parse filters
        parsed_filters = {}
        if filters:
            try:
                parsed_filters = json.loads(filters)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid filters JSON")
        
        analytics = await get_dashboard_analytics()
        dashboard_data = await analytics.get_dashboard_data(
            user_id=user_id,
            dashboard_id=dashboard_id,
            time_range=time_range_enum,
            filters=parsed_filters
        )
        
        if not dashboard_data:
            raise HTTPException(status_code=404, detail="Dashboard data not found")
        
        return AnalyticsDataResponse(**dashboard_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get dashboard data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/dashboard", response_model=Dict[str, str])
async def create_dashboard(
    request: DashboardCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a new dashboard"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        analytics = await get_dashboard_analytics()
        dashboard_id = await analytics.create_dashboard(
            name=request.name,
            description=request.description,
            user_id=user_id,
            widgets=request.widgets,
            layout=request.layout,
            theme=request.theme
        )
        
        return {
            "status": "success",
            "message": "Dashboard created successfully",
            "dashboard_id": dashboard_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create dashboard: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/dashboards", response_model=DashboardListResponse)
async def get_dashboards(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size"),
    current_user: dict = Depends(get_current_user)
):
    """Get user dashboards"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        analytics = await get_dashboard_analytics()
        
        # Get user dashboards (in real implementation, this would query database)
        user_dashboards = []
        for dashboard_id, dashboard in analytics.dashboards.items():
            if dashboard.user_id == user_id:
                user_dashboards.append(DashboardResponse(
                    dashboard_id=dashboard.dashboard_id,
                    name=dashboard.name,
                    description=dashboard.description,
                    user_id=dashboard.user_id,
                    widgets=[asdict(widget) for widget in dashboard.widgets],
                    layout=dashboard.layout,
                    theme=dashboard.theme,
                    created_at=dashboard.created_at,
                    updated_at=dashboard.updated_at
                ))
        
        # Apply pagination
        total_count = len(user_dashboards)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_dashboards = user_dashboards[start_idx:end_idx]
        
        total_pages = (total_count + page_size - 1) // page_size
        
        return DashboardListResponse(
            dashboards=paginated_dashboards,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get dashboards: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/dashboards/{dashboard_id}", response_model=DashboardResponse)
async def get_dashboard(
    dashboard_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get dashboard by ID"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        analytics = await get_dashboard_analytics()
        dashboard = await analytics.get_dashboard(dashboard_id)
        
        if not dashboard:
            raise HTTPException(status_code=404, detail="Dashboard not found")
        
        # Check if user owns the dashboard
        if dashboard.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return DashboardResponse(
            dashboard_id=dashboard.dashboard_id,
            name=dashboard.name,
            description=dashboard.description,
            user_id=dashboard.user_id,
            widgets=[asdict(widget) for widget in dashboard.widgets],
            layout=dashboard.layout,
            theme=dashboard.theme,
            created_at=dashboard.created_at,
            updated_at=dashboard.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get dashboard: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/dashboards/{dashboard_id}", response_model=Dict[str, str])
async def update_dashboard(
    dashboard_id: str,
    request: DashboardUpdateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Update dashboard"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        analytics = await get_dashboard_analytics()
        dashboard = await analytics.get_dashboard(dashboard_id)
        
        if not dashboard:
            raise HTTPException(status_code=404, detail="Dashboard not found")
        
        # Check if user owns the dashboard
        if dashboard.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Prepare updates
        updates = {}
        if request.name is not None:
            updates["name"] = request.name
        if request.description is not None:
            updates["description"] = request.description
        if request.widgets is not None:
            updates["widgets"] = request.widgets
        if request.layout is not None:
            updates["layout"] = request.layout
        if request.theme is not None:
            updates["theme"] = request.theme
        
        success = await analytics.update_dashboard(dashboard_id, updates)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update dashboard")
        
        return {
            "status": "success",
            "message": "Dashboard updated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update dashboard: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/dashboards/{dashboard_id}", response_model=Dict[str, str])
async def delete_dashboard(
    dashboard_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete dashboard"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        analytics = await get_dashboard_analytics()
        dashboard = await analytics.get_dashboard(dashboard_id)
        
        if not dashboard:
            raise HTTPException(status_code=404, detail="Dashboard not found")
        
        # Check if user owns the dashboard
        if dashboard.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        success = await analytics.delete_dashboard(dashboard_id)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete dashboard")
        
        return {
            "status": "success",
            "message": "Dashboard deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete dashboard: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/reports", response_model=Dict[str, str])
async def generate_report(
    request: ReportGenerateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Generate analytics report"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        # Validate report type
        try:
            report_type = AnalyticsType(request.report_type)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid report type")
        
        # Validate format
        if request.format not in ["json", "csv", "excel", "pdf"]:
            raise HTTPException(status_code=400, detail="Invalid report format")
        
        analytics = await get_dashboard_analytics()
        report_id = await analytics.generate_report(
            name=request.name,
            description=request.description,
            report_type=report_type,
            parameters=request.parameters,
            user_id=user_id,
            format=request.format
        )
        
        return {
            "status": "success",
            "message": "Report generated successfully",
            "report_id": report_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate report: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/reports/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get report by ID"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        analytics = await get_dashboard_analytics()
        report = await analytics.get_report(report_id)
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Check if user owns the report
        if report.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Check if report has expired
        if report.expires_at and report.expires_at < datetime.now(datetime.UTC):
            raise HTTPException(status_code=410, detail="Report has expired")
        
        return ReportResponse(
            report_id=report.report_id,
            name=report.name,
            description=report.description,
            report_type=report.report_type.value,
            parameters=report.parameters,
            data=report.data,
            format=report.format,
            generated_at=report.generated_at,
            expires_at=report.expires_at,
            user_id=report.user_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get report: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/export/{dashboard_id}", response_model=Dict[str, Any])
async def export_dashboard_data(
    dashboard_id: str,
    request: ExportRequest,
    current_user: dict = Depends(get_current_user)
):
    """Export dashboard data"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        # Validate time range
        try:
            time_range = TimeRange(request.time_range)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid time range")
        
        # Validate format
        if request.format not in ["json", "csv", "excel"]:
            raise HTTPException(status_code=400, detail="Invalid export format")
        
        analytics = await get_dashboard_analytics()
        dashboard = await analytics.get_dashboard(dashboard_id)
        
        if not dashboard:
            raise HTTPException(status_code=404, detail="Dashboard not found")
        
        # Check if user owns the dashboard
        if dashboard.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        export_data = await analytics.export_dashboard_data(
            dashboard_id=dashboard_id,
            format=request.format,
            time_range=time_range
        )
        
        return {
            "status": "success",
            "message": "Data exported successfully",
            "format": request.format,
            "data": export_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to export dashboard data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/summary", response_model=AnalyticsSummaryResponse)
async def get_analytics_summary(
    time_range: str = Query("1m", description="Time range"),
    current_user: dict = Depends(get_current_user)
):
    """Get analytics summary"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        # Validate time range
        try:
            time_range_enum = TimeRange(time_range)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid time range")
        
        analytics = await get_dashboard_analytics()
        summary = await analytics.get_analytics_summary(
            user_id=user_id,
            time_range=time_range_enum
        )
        
        if not summary:
            raise HTTPException(status_code=404, detail="Analytics summary not found")
        
        return AnalyticsSummaryResponse(**summary)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get analytics summary: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/metrics/{analytics_type}", response_model=List[Dict[str, Any]])
async def get_analytics_metrics(
    analytics_type: str,
    time_range: str = Query("1m", description="Time range"),
    filters: Optional[str] = Query(None, description="JSON filters"),
    current_user: dict = Depends(get_current_user)
):
    """Get analytics metrics by type"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        # Validate analytics type
        try:
            analytics_type_enum = AnalyticsType(analytics_type)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid analytics type")
        
        # Validate time range
        try:
            time_range_enum = TimeRange(time_range)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid time range")
        
        # Parse filters
        parsed_filters = {"user_id": user_id}
        if filters:
            try:
                parsed_filters.update(json.loads(filters))
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid filters JSON")
        
        analytics = await get_dashboard_analytics()
        
        if analytics_type_enum not in analytics.analytics_engines:
            raise HTTPException(status_code=400, detail="Analytics type not supported")
        
        engine = analytics.analytics_engines[analytics_type_enum]
        metrics = await engine.calculate_metrics(time_range_enum, parsed_filters)
        
        return [asdict(metric) for metric in metrics]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get analytics metrics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/charts/{analytics_type}", response_model=List[Dict[str, Any]])
async def get_analytics_charts(
    analytics_type: str,
    time_range: str = Query("1m", description="Time range"),
    filters: Optional[str] = Query(None, description="JSON filters"),
    current_user: dict = Depends(get_current_user)
):
    """Get analytics charts by type"""
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")
        
        # Validate analytics type
        try:
            analytics_type_enum = AnalyticsType(analytics_type)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid analytics type")
        
        # Validate time range
        try:
            time_range_enum = TimeRange(time_range)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid time range")
        
        # Parse filters
        parsed_filters = {"user_id": user_id}
        if filters:
            try:
                parsed_filters.update(json.loads(filters))
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid filters JSON")
        
        analytics = await get_dashboard_analytics()
        
        if analytics_type_enum not in analytics.analytics_engines:
            raise HTTPException(status_code=400, detail="Analytics type not supported")
        
        engine = analytics.analytics_engines[analytics_type_enum]
        charts = await engine.generate_charts(time_range_enum, parsed_filters)
        
        return [asdict(chart) for chart in charts]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get analytics charts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# WebSocket endpoint for real-time analytics updates
@router.websocket("/ws/{dashboard_id}")
async def websocket_analytics_updates(websocket: WebSocket, dashboard_id: str):
    """WebSocket endpoint for real-time analytics updates"""
    try:
        await websocket.accept()
        
        analytics = await get_dashboard_analytics()
        dashboard = await analytics.get_dashboard(dashboard_id)
        
        if not dashboard:
            await websocket.close(code=1008, reason="Dashboard not found")
            return
        
        # Send initial dashboard data
        dashboard_data = await analytics.get_dashboard_data(
            user_id=dashboard.user_id,
            dashboard_id=dashboard_id,
            time_range=TimeRange.MONTH
        )
        
        await websocket.send_json({
            "type": "dashboard_data",
            "data": dashboard_data
        })
        
        # Keep connection alive and send updates
        while True:
            try:
                # Get updated dashboard data
                updated_data = await analytics.get_dashboard_data(
                    user_id=dashboard.user_id,
                    dashboard_id=dashboard_id,
                    time_range=TimeRange.MONTH
                )
                
                # Send update
                await websocket.send_json({
                    "type": "dashboard_update",
                    "data": updated_data,
                    "timestamp": datetime.now(datetime.UTC).isoformat()
                })
                
                # Wait before next update
                await asyncio.sleep(30)  # 30 seconds
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                break
        
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    finally:
        await websocket.close()

# Import asdict for dataclass serialization
from dataclasses import asdict
