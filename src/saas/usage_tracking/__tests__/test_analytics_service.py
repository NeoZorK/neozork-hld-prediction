"""
Analytics Service Tests

Unit tests for the analytics service.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock

from ..models import UsageMetric, MetricType, MetricValue
from ..services import AnalyticsService


class TestAnalyticsService:
    """Test cases for AnalyticsService."""
    
    @pytest.fixture
    def mock_storage_backend(self):
        """Mock storage backend."""
        backend = Mock()
        backend.get_events = AsyncMock(return_value=[])
        return backend
    
    @pytest.fixture
    def mock_usage_tracker(self):
        """Mock usage tracker."""
        tracker = Mock()
        tracker.get_usage_metrics = AsyncMock(return_value=[])
        return tracker
    
    @pytest.fixture
    def analytics_service(self, mock_storage_backend, mock_usage_tracker):
        """Analytics service instance with mocked dependencies."""
        return AnalyticsService(
            storage_backend=mock_storage_backend,
            usage_tracker=mock_usage_tracker
        )
    
    @pytest.fixture
    def sample_metrics(self):
        """Sample usage metrics for testing."""
        base_time = datetime.utcnow() - timedelta(days=7)
        metrics = []
        
        for i in range(7):
            metric = UsageMetric(
                tenant_id="tenant-1",
                resource_type="api_calls",
                metric_name="api_calls_usage",
                period_start=base_time + timedelta(days=i),
                period_end=base_time + timedelta(days=i+1),
                values={MetricValue.SUM.value: 100.0 + i * 10},
                total_cost=10.0 + i
            )
            metrics.append(metric)
        
        return metrics
    
    @pytest.mark.asyncio
    async def test_get_usage_analytics_empty_metrics(self, analytics_service):
        """Test analytics with empty metrics."""
        start_date = datetime.utcnow() - timedelta(days=7)
        end_date = datetime.utcnow()
        
        analytics = await analytics_service.get_usage_analytics(
            tenant_id="tenant-1",
            resource_type="api_calls",
            period_start=start_date,
            period_end=end_date
        )
        
        assert analytics["total_usage"] == 0.0
        assert analytics["average_usage"] == 0.0
        assert analytics["peak_usage"] == 0.0
        assert analytics["usage_distribution"] == []
    
    @pytest.mark.asyncio
    async def test_get_usage_analytics_with_metrics(self, analytics_service, sample_metrics):
        """Test analytics with sample metrics."""
        analytics_service.usage_tracker.get_usage_metrics.return_value = sample_metrics
        
        start_date = datetime.utcnow() - timedelta(days=7)
        end_date = datetime.utcnow()
        
        analytics = await analytics_service.get_usage_analytics(
            tenant_id="tenant-1",
            resource_type="api_calls",
            period_start=start_date,
            period_end=end_date
        )
        
        assert analytics["total_usage"] == 700.0  # Sum of all metrics
        assert analytics["average_usage"] == 100.0  # Average
        assert analytics["peak_usage"] == 160.0  # Maximum
        assert len(analytics["usage_distribution"]) == 7
        assert "cost_analysis" in analytics
        assert "efficiency_metrics" in analytics
    
    @pytest.mark.asyncio
    async def test_get_usage_trends_increasing(self, analytics_service):
        """Test trend detection for increasing usage."""
        # Create metrics with increasing trend
        base_time = datetime.utcnow() - timedelta(days=6)
        metrics = []
        
        for i in range(7):
            metric = UsageMetric(
                tenant_id="tenant-1",
                resource_type="api_calls",
                metric_name="api_calls_usage",
                period_start=base_time + timedelta(days=i),
                period_end=base_time + timedelta(days=i+1),
                values={MetricValue.SUM.value: 100.0 + i * 20}  # Increasing trend
            )
            metrics.append(metric)
        
        analytics_service.usage_tracker.get_usage_metrics.return_value = metrics
        
        start_date = datetime.utcnow() - timedelta(days=7)
        end_date = datetime.utcnow()
        
        trends = await analytics_service.get_usage_trends(
            tenant_id="tenant-1",
            resource_type="api_calls",
            period_start=start_date,
            period_end=end_date
        )
        
        assert trends["trend"] == "increasing"
        assert trends["growth_rate"] > 0
        assert "volatility" in trends
        assert "seasonality" in trends
        assert "anomalies" in trends
    
    @pytest.mark.asyncio
    async def test_get_usage_trends_decreasing(self, analytics_service):
        """Test trend detection for decreasing usage."""
        # Create metrics with decreasing trend
        base_time = datetime.utcnow() - timedelta(days=6)
        metrics = []
        
        for i in range(7):
            metric = UsageMetric(
                tenant_id="tenant-1",
                resource_type="api_calls",
                metric_name="api_calls_usage",
                period_start=base_time + timedelta(days=i),
                period_end=base_time + timedelta(days=i+1),
                values={MetricValue.SUM.value: 200.0 - i * 20}  # Decreasing trend
            )
            metrics.append(metric)
        
        analytics_service.usage_tracker.get_usage_metrics.return_value = metrics
        
        start_date = datetime.utcnow() - timedelta(days=7)
        end_date = datetime.utcnow()
        
        trends = await analytics_service.get_usage_trends(
            tenant_id="tenant-1",
            resource_type="api_calls",
            period_start=start_date,
            period_end=end_date
        )
        
        assert trends["trend"] == "decreasing"
        assert trends["growth_rate"] < 0
    
    @pytest.mark.asyncio
    async def test_get_usage_trends_stable(self, analytics_service):
        """Test trend detection for stable usage."""
        # Create metrics with stable trend
        base_time = datetime.utcnow() - timedelta(days=6)
        metrics = []
        
        for i in range(7):
            metric = UsageMetric(
                tenant_id="tenant-1",
                resource_type="api_calls",
                metric_name="api_calls_usage",
                period_start=base_time + timedelta(days=i),
                period_end=base_time + timedelta(days=i+1),
                values={MetricValue.SUM.value: 100.0}  # Stable trend
            )
            metrics.append(metric)
        
        analytics_service.usage_tracker.get_usage_metrics.return_value = metrics
        
        start_date = datetime.utcnow() - timedelta(days=7)
        end_date = datetime.utcnow()
        
        trends = await analytics_service.get_usage_trends(
            tenant_id="tenant-1",
            resource_type="api_calls",
            period_start=start_date,
            period_end=end_date
        )
        
        assert trends["trend"] == "stable"
        assert abs(trends["growth_rate"]) < 0.1
    
    @pytest.mark.asyncio
    async def test_get_usage_forecast_insufficient_data(self, analytics_service):
        """Test forecast with insufficient data."""
        analytics_service.usage_tracker.get_usage_metrics.return_value = []
        
        forecast = await analytics_service.get_usage_forecast(
            tenant_id="tenant-1",
            resource_type="api_calls",
            forecast_days=30
        )
        
        assert forecast["method"] == "insufficient_data"
        assert forecast["confidence"] == 0.0
        assert forecast["forecast"] == []
    
    @pytest.mark.asyncio
    async def test_get_usage_forecast_sufficient_data(self, analytics_service):
        """Test forecast with sufficient data."""
        # Create 30 days of historical data
        base_time = datetime.utcnow() - timedelta(days=30)
        metrics = []
        
        for i in range(30):
            metric = UsageMetric(
                tenant_id="tenant-1",
                resource_type="api_calls",
                metric_name="api_calls_usage",
                period_start=base_time + timedelta(days=i),
                period_end=base_time + timedelta(days=i+1),
                values={MetricValue.SUM.value: 100.0 + i * 2}  # Slight upward trend
            )
            metrics.append(metric)
        
        analytics_service.usage_tracker.get_usage_metrics.return_value = metrics
        
        forecast = await analytics_service.get_usage_forecast(
            tenant_id="tenant-1",
            resource_type="api_calls",
            forecast_days=7
        )
        
        assert forecast["method"] == "linear_regression"
        assert forecast["confidence"] > 0
        assert len(forecast["forecast"]) == 7
    
    @pytest.mark.asyncio
    async def test_get_usage_insights(self, analytics_service, sample_metrics):
        """Test getting usage insights."""
        analytics_service.usage_tracker.get_usage_metrics.return_value = sample_metrics
        
        start_date = datetime.utcnow() - timedelta(days=7)
        end_date = datetime.utcnow()
        
        insights = await analytics_service.get_usage_insights(
            tenant_id="tenant-1",
            resource_type="api_calls",
            period_start=start_date,
            period_end=end_date
        )
        
        assert isinstance(insights, list)
        # Should have at least one insight (peak usage)
        assert len(insights) > 0
        assert all("type" in insight for insight in insights)
        assert all("title" in insight for insight in insights)
        assert all("description" in insight for insight in insights)
    
    @pytest.mark.asyncio
    async def test_get_usage_comparison(self, analytics_service):
        """Test usage comparison between periods."""
        # Create current period metrics
        current_metrics = [
            UsageMetric(
                tenant_id="tenant-1",
                resource_type="api_calls",
                values={MetricValue.SUM.value: 150.0}
            )
        ]
        
        # Create previous period metrics
        previous_metrics = [
            UsageMetric(
                tenant_id="tenant-1",
                resource_type="api_calls",
                values={MetricValue.SUM.value: 100.0}
            )
        ]
        
        analytics_service.usage_tracker.get_usage_metrics.side_effect = [
            current_metrics,  # First call for current period
            previous_metrics  # Second call for previous period
        ]
        
        current_start = datetime.utcnow() - timedelta(days=7)
        current_end = datetime.utcnow()
        previous_start = current_start - timedelta(days=7)
        previous_end = current_start
        
        comparison = await analytics_service.get_usage_comparison(
            tenant_id="tenant-1",
            resource_type="api_calls",
            current_period_start=current_start,
            current_period_end=current_end,
            previous_period_start=previous_start,
            previous_period_end=previous_end
        )
        
        assert comparison["change_percentage"] == 50.0  # 50% increase
        assert comparison["change_absolute"] == 50.0
        assert comparison["trend"] == "increasing"
        assert comparison["current_total"] == 150.0
        assert comparison["previous_total"] == 100.0
    
    @pytest.mark.asyncio
    async def test_calculate_trend_increasing(self, analytics_service):
        """Test trend calculation for increasing data."""
        metrics = [
            UsageMetric(values={MetricValue.SUM.value: 100.0}),
            UsageMetric(values={MetricValue.SUM.value: 120.0}),
            UsageMetric(values={MetricValue.SUM.value: 140.0}),
            UsageMetric(values={MetricValue.SUM.value: 160.0}),
            UsageMetric(values={MetricValue.SUM.value: 180.0})
        ]
        
        trend = await analytics_service._calculate_trend(metrics)
        assert trend == "increasing"
    
    @pytest.mark.asyncio
    async def test_calculate_trend_decreasing(self, analytics_service):
        """Test trend calculation for decreasing data."""
        metrics = [
            UsageMetric(values={MetricValue.SUM.value: 180.0}),
            UsageMetric(values={MetricValue.SUM.value: 160.0}),
            UsageMetric(values={MetricValue.SUM.value: 140.0}),
            UsageMetric(values={MetricValue.SUM.value: 120.0}),
            UsageMetric(values={MetricValue.SUM.value: 100.0})
        ]
        
        trend = await analytics_service._calculate_trend(metrics)
        assert trend == "decreasing"
    
    @pytest.mark.asyncio
    async def test_calculate_trend_stable(self, analytics_service):
        """Test trend calculation for stable data."""
        metrics = [
            UsageMetric(values={MetricValue.SUM.value: 100.0}),
            UsageMetric(values={MetricValue.SUM.value: 105.0}),
            UsageMetric(values={MetricValue.SUM.value: 95.0}),
            UsageMetric(values={MetricValue.SUM.value: 102.0}),
            UsageMetric(values={MetricValue.SUM.value: 98.0})
        ]
        
        trend = await analytics_service._calculate_trend(metrics)
        assert trend == "stable"
    
    @pytest.mark.asyncio
    async def test_calculate_growth_rate(self, analytics_service):
        """Test growth rate calculation."""
        metrics = [
            UsageMetric(values={MetricValue.SUM.value: 100.0}),
            UsageMetric(values={MetricValue.SUM.value: 150.0})
        ]
        
        growth_rate = await analytics_service._calculate_growth_rate(metrics)
        assert growth_rate == 50.0  # 50% growth
    
    @pytest.mark.asyncio
    async def test_calculate_volatility(self, analytics_service):
        """Test volatility calculation."""
        metrics = [
            UsageMetric(values={MetricValue.SUM.value: 100.0}),
            UsageMetric(values={MetricValue.SUM.value: 120.0}),
            UsageMetric(values={MetricValue.SUM.value: 80.0}),
            UsageMetric(values={MetricValue.SUM.value: 110.0}),
            UsageMetric(values={MetricValue.SUM.value: 90.0})
        ]
        
        volatility = await analytics_service._calculate_volatility(metrics)
        assert volatility > 0  # Should have some volatility
    
    @pytest.mark.asyncio
    async def test_detect_anomalies(self, analytics_service):
        """Test anomaly detection."""
        metrics = [
            UsageMetric(values={MetricValue.SUM.value: 100.0}),
            UsageMetric(values={MetricValue.SUM.value: 105.0}),
            UsageMetric(values={MetricValue.SUM.value: 200.0}),  # Anomaly
            UsageMetric(values={MetricValue.SUM.value: 102.0}),
            UsageMetric(values={MetricValue.SUM.value: 98.0})
        ]
        
        anomalies = await analytics_service._detect_anomalies(metrics)
        assert len(anomalies) > 0  # Should detect the anomaly
        assert all("timestamp" in anomaly for anomaly in anomalies)
        assert all("value" in anomaly for anomaly in anomalies)
        assert all("severity" in anomaly for anomaly in anomalies)
