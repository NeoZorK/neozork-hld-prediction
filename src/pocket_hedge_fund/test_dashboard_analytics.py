"""
NeoZork Pocket Hedge Fund - Dashboard Analytics Test Suite

This module provides comprehensive testing for the dashboard analytics including:
- Analytics engines testing
- Dashboard management
- Report generation
- Data export
- Real-time analytics
- API endpoints
- Error handling and edge cases
"""

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, List, Any
import numpy as np

from .analytics.dashboard_analytics import (
    DashboardAnalytics, PerformanceAnalytics, RiskAnalytics, PortfolioAnalytics,
    AnalyticsType, TimeRange, ChartType, MetricType,
    AnalyticsMetric, ChartData, DashboardWidget, Dashboard, Report
)
from .config.database_manager import DatabaseManager
from .config.config_manager import ConfigManager
from .notifications.notification_manager import NotificationManager

class TestPerformanceAnalytics:
    """Test suite for PerformanceAnalytics"""
    
    @pytest.fixture
    def performance_analytics(self):
        """Create performance analytics instance for testing"""
        return PerformanceAnalytics()
    
    @pytest.mark.asyncio
    async def test_performance_analytics_initialization(self, performance_analytics):
        """Test performance analytics initialization"""
        assert performance_analytics.analytics_type == AnalyticsType.PERFORMANCE
        assert isinstance(performance_analytics.metrics, dict)
        assert isinstance(performance_analytics.charts, dict)
        assert isinstance(performance_analytics.data_cache, dict)
    
    @pytest.mark.asyncio
    async def test_calculate_metrics(self, performance_analytics):
        """Test performance metrics calculation"""
        time_range = TimeRange.MONTH
        filters = {"user_id": "test_user"}
        
        metrics = await performance_analytics.calculate_metrics(time_range, filters)
        
        assert isinstance(metrics, list)
        assert len(metrics) > 0
        
        # Check metric structure
        for metric in metrics:
            assert isinstance(metric, AnalyticsMetric)
            assert metric.metric_id is not None
            assert metric.name is not None
            assert metric.value is not None
            assert metric.metric_type in MetricType
            assert metric.unit is not None
            assert metric.trend in ["up", "down", "stable"]
            assert metric.timestamp is not None
    
    @pytest.mark.asyncio
    async def test_generate_charts(self, performance_analytics):
        """Test performance charts generation"""
        time_range = TimeRange.MONTH
        filters = {"user_id": "test_user"}
        
        charts = await performance_analytics.generate_charts(time_range, filters)
        
        assert isinstance(charts, list)
        assert len(charts) > 0
        
        # Check chart structure
        for chart in charts:
            assert isinstance(chart, ChartData)
            assert chart.chart_id is not None
            assert chart.title is not None
            assert chart.chart_type in ChartType
            assert isinstance(chart.data, list)
            assert chart.x_axis is not None
            assert chart.y_axis is not None
            assert isinstance(chart.series, list)
            assert isinstance(chart.colors, list)
    
    @pytest.mark.asyncio
    async def test_cached_data_operations(self, performance_analytics):
        """Test cached data operations"""
        # Test setting cached data
        await performance_analytics.set_cached_data("test_key", {"test": "data"}, ttl=60)
        
        # Test getting cached data
        cached_data = await performance_analytics.get_cached_data("test_key")
        assert cached_data is not None
        assert cached_data["data"]["test"] == "data"
        
        # Test getting non-existent cached data
        non_existent = await performance_analytics.get_cached_data("non_existent")
        assert non_existent is None

class TestRiskAnalytics:
    """Test suite for RiskAnalytics"""
    
    @pytest.fixture
    def risk_analytics(self):
        """Create risk analytics instance for testing"""
        return RiskAnalytics()
    
    @pytest.mark.asyncio
    async def test_risk_analytics_initialization(self, risk_analytics):
        """Test risk analytics initialization"""
        assert risk_analytics.analytics_type == AnalyticsType.RISK
        assert isinstance(risk_analytics.metrics, dict)
        assert isinstance(risk_analytics.charts, dict)
        assert isinstance(risk_analytics.data_cache, dict)
    
    @pytest.mark.asyncio
    async def test_calculate_risk_metrics(self, risk_analytics):
        """Test risk metrics calculation"""
        time_range = TimeRange.MONTH
        filters = {"user_id": "test_user"}
        
        metrics = await risk_analytics.calculate_metrics(time_range, filters)
        
        assert isinstance(metrics, list)
        assert len(metrics) > 0
        
        # Check for specific risk metrics
        metric_ids = [metric.metric_id for metric in metrics]
        assert "var_95" in metric_ids
        assert "cvar_95" in metric_ids
        assert "volatility" in metric_ids
        assert "beta" in metric_ids
        
        # Check metric structure
        for metric in metrics:
            assert isinstance(metric, AnalyticsMetric)
            assert metric.metric_id is not None
            assert metric.name is not None
            assert metric.value is not None
            assert metric.metric_type in MetricType
            assert metric.unit is not None
            assert metric.trend in ["up", "down", "stable"]
            assert metric.timestamp is not None
    
    @pytest.mark.asyncio
    async def test_generate_risk_charts(self, risk_analytics):
        """Test risk charts generation"""
        time_range = TimeRange.MONTH
        filters = {"user_id": "test_user"}
        
        charts = await risk_analytics.generate_charts(time_range, filters)
        
        assert isinstance(charts, list)
        assert len(charts) > 0
        
        # Check chart structure
        for chart in charts:
            assert isinstance(chart, ChartData)
            assert chart.chart_id is not None
            assert chart.title is not None
            assert chart.chart_type in ChartType
            assert isinstance(chart.data, list)
            assert chart.x_axis is not None
            assert chart.y_axis is not None
            assert isinstance(chart.series, list)
            assert isinstance(chart.colors, list)

class TestPortfolioAnalytics:
    """Test suite for PortfolioAnalytics"""
    
    @pytest.fixture
    def portfolio_analytics(self):
        """Create portfolio analytics instance for testing"""
        return PortfolioAnalytics()
    
    @pytest.mark.asyncio
    async def test_portfolio_analytics_initialization(self, portfolio_analytics):
        """Test portfolio analytics initialization"""
        assert portfolio_analytics.analytics_type == AnalyticsType.PORTFOLIO
        assert isinstance(portfolio_analytics.metrics, dict)
        assert isinstance(portfolio_analytics.charts, dict)
        assert isinstance(portfolio_analytics.data_cache, dict)
    
    @pytest.mark.asyncio
    async def test_calculate_portfolio_metrics(self, portfolio_analytics):
        """Test portfolio metrics calculation"""
        time_range = TimeRange.MONTH
        filters = {"user_id": "test_user"}
        
        metrics = await portfolio_analytics.calculate_metrics(time_range, filters)
        
        assert isinstance(metrics, list)
        assert len(metrics) > 0
        
        # Check for specific portfolio metrics
        metric_ids = [metric.metric_id for metric in metrics]
        assert "total_value" in metric_ids
        assert "position_count" in metric_ids
        assert "diversification_ratio" in metric_ids
        
        # Check metric structure
        for metric in metrics:
            assert isinstance(metric, AnalyticsMetric)
            assert metric.metric_id is not None
            assert metric.name is not None
            assert metric.value is not None
            assert metric.metric_type in MetricType
            assert metric.unit is not None
            assert metric.trend in ["up", "down", "stable"]
            assert metric.timestamp is not None
    
    @pytest.mark.asyncio
    async def test_generate_portfolio_charts(self, portfolio_analytics):
        """Test portfolio charts generation"""
        time_range = TimeRange.MONTH
        filters = {"user_id": "test_user"}
        
        charts = await portfolio_analytics.generate_charts(time_range, filters)
        
        assert isinstance(charts, list)
        assert len(charts) > 0
        
        # Check chart structure
        for chart in charts:
            assert isinstance(chart, ChartData)
            assert chart.chart_id is not None
            assert chart.title is not None
            assert chart.chart_type in ChartType
            assert isinstance(chart.data, list)
            assert chart.x_axis is not None
            assert chart.y_axis is not None
            assert isinstance(chart.series, list)
            assert isinstance(chart.colors, list)

class TestDashboardAnalytics:
    """Test suite for DashboardAnalytics"""
    
    @pytest.fixture
    async def dashboard_analytics(self):
        """Create dashboard analytics instance for testing"""
        db_manager = Mock(spec=DatabaseManager)
        config_manager = Mock(spec=ConfigManager)
        notification_manager = Mock(spec=NotificationManager)
        
        # Mock configuration
        config_manager.get_config.side_effect = lambda key: {
            "redis": {"host": "localhost", "port": 6379, "db": 0}
        }.get(key, {})
        
        analytics = DashboardAnalytics(db_manager, config_manager, notification_manager)
        
        # Mock Redis client
        analytics.redis_client = AsyncMock()
        
        await analytics.initialize()
        return analytics
    
    @pytest.mark.asyncio
    async def test_dashboard_analytics_initialization(self, dashboard_analytics):
        """Test dashboard analytics initialization"""
        assert isinstance(dashboard_analytics.analytics_engines, dict)
        assert AnalyticsType.PERFORMANCE in dashboard_analytics.analytics_engines
        assert AnalyticsType.RISK in dashboard_analytics.analytics_engines
        assert AnalyticsType.PORTFOLIO in dashboard_analytics.analytics_engines
        assert isinstance(dashboard_analytics.dashboards, dict)
        assert isinstance(dashboard_analytics.reports, dict)
    
    @pytest.mark.asyncio
    async def test_get_dashboard_data(self, dashboard_analytics):
        """Test getting dashboard data"""
        user_id = "test_user"
        time_range = TimeRange.MONTH
        filters = {"user_id": user_id}
        
        dashboard_data = await dashboard_analytics.get_dashboard_data(
            user_id=user_id,
            time_range=time_range,
            filters=filters
        )
        
        assert isinstance(dashboard_data, dict)
        assert "user_id" in dashboard_data
        assert "time_range" in dashboard_data
        assert "generated_at" in dashboard_data
        assert "metrics" in dashboard_data
        assert "charts" in dashboard_data
        assert "widgets" in dashboard_data
        
        # Check metrics structure
        assert isinstance(dashboard_data["metrics"], dict)
        assert "performance" in dashboard_data["metrics"]
        assert "risk" in dashboard_data["metrics"]
        assert "portfolio" in dashboard_data["metrics"]
        
        # Check charts structure
        assert isinstance(dashboard_data["charts"], dict)
        assert "performance" in dashboard_data["charts"]
        assert "risk" in dashboard_data["charts"]
        assert "portfolio" in dashboard_data["charts"]
    
    @pytest.mark.asyncio
    async def test_create_dashboard(self, dashboard_analytics):
        """Test creating dashboard"""
        name = "Test Dashboard"
        description = "Test dashboard description"
        user_id = "test_user"
        widgets = [
            {
                "title": "Test Widget",
                "type": "metric",
                "position": {"x": 0, "y": 0, "width": 4, "height": 3},
                "data": {"metric_id": "total_return"},
                "refresh_interval": 60,
                "visible": True
            }
        ]
        layout = {"columns": 12, "rows": 8}
        theme = "default"
        
        dashboard_id = await dashboard_analytics.create_dashboard(
            name=name,
            description=description,
            user_id=user_id,
            widgets=widgets,
            layout=layout,
            theme=theme
        )
        
        assert dashboard_id is not None
        assert dashboard_id in dashboard_analytics.dashboards
        
        dashboard = dashboard_analytics.dashboards[dashboard_id]
        assert dashboard.name == name
        assert dashboard.description == description
        assert dashboard.user_id == user_id
        assert dashboard.layout == layout
        assert dashboard.theme == theme
        assert len(dashboard.widgets) == 1
    
    @pytest.mark.asyncio
    async def test_get_dashboard(self, dashboard_analytics):
        """Test getting dashboard by ID"""
        # Create dashboard first
        dashboard_id = await dashboard_analytics.create_dashboard(
            name="Test Dashboard",
            description="Test description",
            user_id="test_user",
            widgets=[],
            layout={"columns": 12, "rows": 8},
            theme="default"
        )
        
        # Get dashboard
        dashboard = await dashboard_analytics.get_dashboard(dashboard_id)
        
        assert dashboard is not None
        assert dashboard.dashboard_id == dashboard_id
        assert dashboard.name == "Test Dashboard"
        assert dashboard.user_id == "test_user"
    
    @pytest.mark.asyncio
    async def test_update_dashboard(self, dashboard_analytics):
        """Test updating dashboard"""
        # Create dashboard first
        dashboard_id = await dashboard_analytics.create_dashboard(
            name="Test Dashboard",
            description="Test description",
            user_id="test_user",
            widgets=[],
            layout={"columns": 12, "rows": 8},
            theme="default"
        )
        
        # Update dashboard
        updates = {
            "name": "Updated Dashboard",
            "description": "Updated description",
            "theme": "dark"
        }
        
        success = await dashboard_analytics.update_dashboard(dashboard_id, updates)
        
        assert success is True
        
        # Verify updates
        dashboard = await dashboard_analytics.get_dashboard(dashboard_id)
        assert dashboard.name == "Updated Dashboard"
        assert dashboard.description == "Updated description"
        assert dashboard.theme == "dark"
    
    @pytest.mark.asyncio
    async def test_delete_dashboard(self, dashboard_analytics):
        """Test deleting dashboard"""
        # Create dashboard first
        dashboard_id = await dashboard_analytics.create_dashboard(
            name="Test Dashboard",
            description="Test description",
            user_id="test_user",
            widgets=[],
            layout={"columns": 12, "rows": 8},
            theme="default"
        )
        
        # Delete dashboard
        success = await dashboard_analytics.delete_dashboard(dashboard_id)
        
        assert success is True
        assert dashboard_id not in dashboard_analytics.dashboards
        
        # Verify dashboard is deleted
        dashboard = await dashboard_analytics.get_dashboard(dashboard_id)
        assert dashboard is None
    
    @pytest.mark.asyncio
    async def test_generate_report(self, dashboard_analytics):
        """Test generating report"""
        name = "Test Report"
        description = "Test report description"
        report_type = AnalyticsType.PERFORMANCE
        parameters = {"time_range": "1m", "user_id": "test_user"}
        user_id = "test_user"
        format = "json"
        
        report_id = await dashboard_analytics.generate_report(
            name=name,
            description=description,
            report_type=report_type,
            parameters=parameters,
            user_id=user_id,
            format=format
        )
        
        assert report_id is not None
        assert report_id in dashboard_analytics.reports
        
        report = dashboard_analytics.reports[report_id]
        assert report.name == name
        assert report.description == description
        assert report.report_type == report_type
        assert report.parameters == parameters
        assert report.user_id == user_id
        assert report.format == format
    
    @pytest.mark.asyncio
    async def test_get_report(self, dashboard_analytics):
        """Test getting report by ID"""
        # Generate report first
        report_id = await dashboard_analytics.generate_report(
            name="Test Report",
            description="Test description",
            report_type=AnalyticsType.PERFORMANCE,
            parameters={"user_id": "test_user"},
            user_id="test_user",
            format="json"
        )
        
        # Get report
        report = await dashboard_analytics.get_report(report_id)
        
        assert report is not None
        assert report.report_id == report_id
        assert report.name == "Test Report"
        assert report.user_id == "test_user"
    
    @pytest.mark.asyncio
    async def test_export_dashboard_data(self, dashboard_analytics):
        """Test exporting dashboard data"""
        # Create dashboard first
        dashboard_id = await dashboard_analytics.create_dashboard(
            name="Test Dashboard",
            description="Test description",
            user_id="test_user",
            widgets=[],
            layout={"columns": 12, "rows": 8},
            theme="default"
        )
        
        # Export data
        export_data = await dashboard_analytics.export_dashboard_data(
            dashboard_id=dashboard_id,
            format="json",
            time_range=TimeRange.MONTH
        )
        
        assert isinstance(export_data, dict)
        assert "format" in export_data
        assert export_data["format"] == "json"
    
    @pytest.mark.asyncio
    async def test_get_analytics_summary(self, dashboard_analytics):
        """Test getting analytics summary"""
        user_id = "test_user"
        time_range = TimeRange.MONTH
        
        summary = await dashboard_analytics.get_analytics_summary(
            user_id=user_id,
            time_range=time_range
        )
        
        assert isinstance(summary, dict)
        assert "user_id" in summary
        assert "time_range" in summary
        assert "generated_at" in summary
        assert "summary" in summary
        
        # Check summary structure
        assert isinstance(summary["summary"], dict)
        assert "performance" in summary["summary"]
        assert "risk" in summary["summary"]
        assert "portfolio" in summary["summary"]
    
    @pytest.mark.asyncio
    async def test_error_handling(self, dashboard_analytics):
        """Test error handling in dashboard analytics"""
        # Test getting non-existent dashboard
        dashboard = await dashboard_analytics.get_dashboard("non_existent")
        assert dashboard is None
        
        # Test updating non-existent dashboard
        success = await dashboard_analytics.update_dashboard("non_existent", {"name": "test"})
        assert success is False
        
        # Test deleting non-existent dashboard
        success = await dashboard_analytics.delete_dashboard("non_existent")
        assert success is False
        
        # Test getting non-existent report
        report = await dashboard_analytics.get_report("non_existent")
        assert report is None

class TestDashboardAnalyticsAPI:
    """Test suite for Dashboard Analytics API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        from fastapi.testclient import TestClient
        from .api.dashboard_analytics_api import router
        
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)
    
    def test_get_dashboard_data_endpoint(self, client):
        """Test get dashboard data endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock dashboard analytics
            with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_dashboard_analytics') as mock_analytics:
                mock_analytics_instance = AsyncMock()
                mock_analytics_instance.get_dashboard_data.return_value = {
                    "dashboard_id": None,
                    "user_id": "test_user",
                    "time_range": "1m",
                    "generated_at": "2025-01-01T00:00:00Z",
                    "metrics": {"performance": [], "risk": [], "portfolio": []},
                    "charts": {"performance": [], "risk": [], "portfolio": []},
                    "widgets": []
                }
                mock_analytics.return_value = mock_analytics_instance
                
                response = client.get(
                    "/api/v1/analytics/dashboard",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert "user_id" in data
                assert "metrics" in data
                assert "charts" in data
    
    def test_create_dashboard_endpoint(self, client):
        """Test create dashboard endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock dashboard analytics
            with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_dashboard_analytics') as mock_analytics:
                mock_analytics_instance = AsyncMock()
                mock_analytics_instance.create_dashboard.return_value = "test_dashboard_001"
                mock_analytics.return_value = mock_analytics_instance
                
                response = client.post(
                    "/api/v1/analytics/dashboard",
                    json={
                        "name": "Test Dashboard",
                        "description": "Test dashboard description",
                        "widgets": [],
                        "layout": {"columns": 12, "rows": 8},
                        "theme": "default"
                    },
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
                assert "dashboard_id" in data
    
    def test_get_dashboards_endpoint(self, client):
        """Test get dashboards endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock dashboard analytics
            with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_dashboard_analytics') as mock_analytics:
                mock_analytics_instance = AsyncMock()
                mock_dashboard = Mock()
                mock_dashboard.dashboard_id = "test_dashboard_001"
                mock_dashboard.name = "Test Dashboard"
                mock_dashboard.description = "Test description"
                mock_dashboard.user_id = "test_user"
                mock_dashboard.widgets = []
                mock_dashboard.layout = {"columns": 12, "rows": 8}
                mock_dashboard.theme = "default"
                mock_dashboard.created_at = datetime.now(datetime.UTC)
                mock_dashboard.updated_at = datetime.now(datetime.UTC)
                
                mock_analytics_instance.dashboards = {"test_dashboard_001": mock_dashboard}
                mock_analytics.return_value = mock_analytics_instance
                
                response = client.get(
                    "/api/v1/analytics/dashboards",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert "dashboards" in data
                assert "total_count" in data
    
    def test_get_dashboard_by_id_endpoint(self, client):
        """Test get dashboard by ID endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock dashboard analytics
            with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_dashboard_analytics') as mock_analytics:
                mock_analytics_instance = AsyncMock()
                mock_dashboard = Mock()
                mock_dashboard.dashboard_id = "test_dashboard_001"
                mock_dashboard.name = "Test Dashboard"
                mock_dashboard.description = "Test description"
                mock_dashboard.user_id = "test_user"
                mock_dashboard.widgets = []
                mock_dashboard.layout = {"columns": 12, "rows": 8}
                mock_dashboard.theme = "default"
                mock_dashboard.created_at = datetime.now(datetime.UTC)
                mock_dashboard.updated_at = datetime.now(datetime.UTC)
                
                mock_analytics_instance.get_dashboard.return_value = mock_dashboard
                mock_analytics.return_value = mock_analytics_instance
                
                response = client.get(
                    "/api/v1/analytics/dashboards/test_dashboard_001",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["dashboard_id"] == "test_dashboard_001"
                assert data["name"] == "Test Dashboard"
    
    def test_update_dashboard_endpoint(self, client):
        """Test update dashboard endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock dashboard analytics
            with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_dashboard_analytics') as mock_analytics:
                mock_analytics_instance = AsyncMock()
                mock_dashboard = Mock()
                mock_dashboard.user_id = "test_user"
                
                mock_analytics_instance.get_dashboard.return_value = mock_dashboard
                mock_analytics_instance.update_dashboard.return_value = True
                mock_analytics.return_value = mock_analytics_instance
                
                response = client.put(
                    "/api/v1/analytics/dashboards/test_dashboard_001",
                    json={
                        "name": "Updated Dashboard",
                        "description": "Updated description",
                        "theme": "dark"
                    },
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
    
    def test_delete_dashboard_endpoint(self, client):
        """Test delete dashboard endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock dashboard analytics
            with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_dashboard_analytics') as mock_analytics:
                mock_analytics_instance = AsyncMock()
                mock_dashboard = Mock()
                mock_dashboard.user_id = "test_user"
                
                mock_analytics_instance.get_dashboard.return_value = mock_dashboard
                mock_analytics_instance.delete_dashboard.return_value = True
                mock_analytics.return_value = mock_analytics_instance
                
                response = client.delete(
                    "/api/v1/analytics/dashboards/test_dashboard_001",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
    
    def test_generate_report_endpoint(self, client):
        """Test generate report endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock dashboard analytics
            with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_dashboard_analytics') as mock_analytics:
                mock_analytics_instance = AsyncMock()
                mock_analytics_instance.generate_report.return_value = "test_report_001"
                mock_analytics.return_value = mock_analytics_instance
                
                response = client.post(
                    "/api/v1/analytics/reports",
                    json={
                        "name": "Test Report",
                        "description": "Test report description",
                        "report_type": "performance",
                        "parameters": {"time_range": "1m"},
                        "format": "json"
                    },
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
                assert "report_id" in data
    
    def test_get_report_endpoint(self, client):
        """Test get report endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock dashboard analytics
            with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_dashboard_analytics') as mock_analytics:
                mock_analytics_instance = AsyncMock()
                mock_report = Mock()
                mock_report.report_id = "test_report_001"
                mock_report.name = "Test Report"
                mock_report.description = "Test description"
                mock_report.report_type = AnalyticsType.PERFORMANCE
                mock_report.parameters = {}
                mock_report.data = {}
                mock_report.format = "json"
                mock_report.generated_at = datetime.now(datetime.UTC)
                mock_report.expires_at = None
                mock_report.user_id = "test_user"
                
                mock_analytics_instance.get_report.return_value = mock_report
                mock_analytics.return_value = mock_analytics_instance
                
                response = client.get(
                    "/api/v1/analytics/reports/test_report_001",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["report_id"] == "test_report_001"
                assert data["name"] == "Test Report"
    
    def test_export_dashboard_data_endpoint(self, client):
        """Test export dashboard data endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock dashboard analytics
            with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_dashboard_analytics') as mock_analytics:
                mock_analytics_instance = AsyncMock()
                mock_dashboard = Mock()
                mock_dashboard.user_id = "test_user"
                
                mock_analytics_instance.get_dashboard.return_value = mock_dashboard
                mock_analytics_instance.export_dashboard_data.return_value = {"format": "json", "data": "export_data"}
                mock_analytics.return_value = mock_analytics_instance
                
                response = client.post(
                    "/api/v1/analytics/export/test_dashboard_001",
                    json={
                        "format": "json",
                        "time_range": "1m"
                    },
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
                assert "data" in data
    
    def test_get_analytics_summary_endpoint(self, client):
        """Test get analytics summary endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock dashboard analytics
            with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_dashboard_analytics') as mock_analytics:
                mock_analytics_instance = AsyncMock()
                mock_analytics_instance.get_analytics_summary.return_value = {
                    "user_id": "test_user",
                    "time_range": "1m",
                    "generated_at": "2025-01-01T00:00:00Z",
                    "summary": {"performance": {}, "risk": {}, "portfolio": {}}
                }
                mock_analytics.return_value = mock_analytics_instance
                
                response = client.get(
                    "/api/v1/analytics/summary",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert "user_id" in data
                assert "summary" in data
    
    def test_get_analytics_metrics_endpoint(self, client):
        """Test get analytics metrics endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock dashboard analytics
            with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_dashboard_analytics') as mock_analytics:
                mock_analytics_instance = AsyncMock()
                mock_engine = AsyncMock()
                mock_metric = Mock()
                mock_metric.metric_id = "test_metric"
                mock_metric.name = "Test Metric"
                mock_metric.value = 100.0
                mock_metric.metric_type = MetricType.VALUE
                mock_metric.unit = "$"
                mock_metric.trend = "up"
                mock_metric.timestamp = datetime.now(datetime.UTC)
                mock_metric.metadata = {}
                
                mock_engine.calculate_metrics.return_value = [mock_metric]
                mock_analytics_instance.analytics_engines = {AnalyticsType.PERFORMANCE: mock_engine}
                mock_analytics.return_value = mock_analytics_instance
                
                response = client.get(
                    "/api/v1/analytics/metrics/performance",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert isinstance(data, list)
                assert len(data) > 0
    
    def test_get_analytics_charts_endpoint(self, client):
        """Test get analytics charts endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock dashboard analytics
            with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_dashboard_analytics') as mock_analytics:
                mock_analytics_instance = AsyncMock()
                mock_engine = AsyncMock()
                mock_chart = Mock()
                mock_chart.chart_id = "test_chart"
                mock_chart.title = "Test Chart"
                mock_chart.chart_type = ChartType.LINE
                mock_chart.data = []
                mock_chart.x_axis = "date"
                mock_chart.y_axis = "value"
                mock_chart.series = ["series1"]
                mock_chart.colors = ["#1f77b4"]
                mock_chart.metadata = {}
                
                mock_engine.generate_charts.return_value = [mock_chart]
                mock_analytics_instance.analytics_engines = {AnalyticsType.PERFORMANCE: mock_engine}
                mock_analytics.return_value = mock_analytics_instance
                
                response = client.get(
                    "/api/v1/analytics/charts/performance",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert isinstance(data, list)
                assert len(data) > 0
    
    def test_unauthorized_access(self, client):
        """Test unauthorized access to endpoints"""
        # Test without authentication
        response = client.get("/api/v1/analytics/dashboard")
        assert response.status_code == 401
        
        # Test with invalid token
        response = client.get(
            "/api/v1/analytics/dashboard",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
    
    def test_invalid_input_validation(self, client):
        """Test input validation for API endpoints"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.dashboard_analytics_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Test with invalid time range
            response = client.get(
                "/api/v1/analytics/dashboard?time_range=invalid",
                headers={"Authorization": "Bearer test_token"}
            )
            assert response.status_code == 400
            
            # Test with invalid report type
            response = client.post(
                "/api/v1/analytics/reports",
                json={
                    "name": "Test Report",
                    "description": "Test description",
                    "report_type": "invalid_type",
                    "parameters": {},
                    "format": "json"
                },
                headers={"Authorization": "Bearer test_token"}
            )
            assert response.status_code == 400
            
            # Test with invalid export format
            response = client.post(
                "/api/v1/analytics/export/test_dashboard_001",
                json={
                    "format": "invalid_format",
                    "time_range": "1m"
                },
                headers={"Authorization": "Bearer test_token"}
            )
            assert response.status_code == 400

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
