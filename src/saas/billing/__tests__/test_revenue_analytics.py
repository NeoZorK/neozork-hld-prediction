"""
Test cases for revenue analytics.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from decimal import Decimal
from datetime import datetime, timezone, timedelta

from src.saas.billing.reports.revenue_analytics import RevenueAnalytics, RevenueForecast, RevenueMetrics


class TestRevenueAnalytics:
    """Test cases for RevenueAnalytics."""
    
    @pytest.fixture
    def revenue_analytics(self):
        """Create RevenueAnalytics instance for testing."""
        payment_service = Mock()
        invoice_service = Mock()
        return RevenueAnalytics(payment_service, invoice_service)
    
    @pytest.fixture
    def mock_subscriptions(self):
        """Create mock subscriptions for testing."""
        return [
            {
                "id": "sub_1",
                "tenant_id": "tenant_1",
                "amount": Decimal("100.00"),
                "billing_cycle": "monthly",
                "status": "active"
            },
            {
                "id": "sub_2",
                "tenant_id": "tenant_1",
                "amount": Decimal("1200.00"),
                "billing_cycle": "yearly",
                "status": "active"
            }
        ]
    
    @pytest.fixture
    def mock_monthly_revenue(self):
        """Create mock monthly revenue data for testing."""
        return [
            Decimal("1000.00"),
            Decimal("1100.00"),
            Decimal("1200.00"),
            Decimal("1300.00"),
            Decimal("1400.00"),
            Decimal("1500.00")
        ]
    
    @pytest.mark.asyncio
    async def test_calculate_mrr(self, revenue_analytics, mock_subscriptions):
        """Test MRR calculation."""
        tenant_id = "tenant_1"
        date = datetime.now(timezone.utc)
        
        with patch.object(revenue_analytics, '_get_active_subscriptions', return_value=mock_subscriptions):
            mrr = await revenue_analytics.calculate_mrr(tenant_id, date)
            
            # 100.00 (monthly) + 1200.00/12 (yearly converted to monthly)
            expected_mrr = Decimal("100.00") + Decimal("100.00")
            assert mrr == expected_mrr
    
    @pytest.mark.asyncio
    async def test_calculate_arr(self, revenue_analytics, mock_subscriptions):
        """Test ARR calculation."""
        tenant_id = "tenant_1"
        date = datetime.now(timezone.utc)
        
        with patch.object(revenue_analytics, '_get_active_subscriptions', return_value=mock_subscriptions):
            arr = await revenue_analytics.calculate_arr(tenant_id, date)
            
            # 100.00*12 (monthly converted to yearly) + 1200.00 (yearly)
            expected_arr = Decimal("1200.00") + Decimal("1200.00")
            assert arr == expected_arr
    
    @pytest.mark.asyncio
    async def test_calculate_revenue_growth_rate(self, revenue_analytics, mock_monthly_revenue):
        """Test revenue growth rate calculation."""
        tenant_id = "tenant_1"
        months = 6
        
        with patch.object(revenue_analytics, '_get_monthly_revenue', return_value=mock_monthly_revenue):
            growth_rate = await revenue_analytics.calculate_revenue_growth_rate(tenant_id, months)
            
            # Growth from 1000 to 1500 = 50%
            assert growth_rate == 50.0
    
    @pytest.mark.asyncio
    async def test_calculate_revenue_growth_rate_no_data(self, revenue_analytics):
        """Test revenue growth rate calculation with no data."""
        tenant_id = "tenant_1"
        months = 6
        
        with patch.object(revenue_analytics, '_get_monthly_revenue', return_value=[]):
            growth_rate = await revenue_analytics.calculate_revenue_growth_rate(tenant_id, months)
            
            assert growth_rate == 0.0
    
    @pytest.mark.asyncio
    async def test_calculate_revenue_growth_rate_zero_start(self, revenue_analytics):
        """Test revenue growth rate calculation with zero starting revenue."""
        tenant_id = "tenant_1"
        months = 6
        monthly_revenue = [Decimal("0.00"), Decimal("100.00")]
        
        with patch.object(revenue_analytics, '_get_monthly_revenue', return_value=monthly_revenue):
            growth_rate = await revenue_analytics.calculate_revenue_growth_rate(tenant_id, months)
            
            assert growth_rate == 0.0
    
    @pytest.mark.asyncio
    async def test_calculate_churn_rate(self, revenue_analytics):
        """Test churn rate calculation."""
        tenant_id = "tenant_1"
        months = 12
        
        with patch.object(revenue_analytics, '_get_customers_at_date', return_value=100):
            with patch.object(revenue_analytics, '_get_customers_lost_in_period', return_value=10):
                churn_rate = await revenue_analytics.calculate_churn_rate(tenant_id, months)
                
                # 10/100 * 100 = 10%
                assert churn_rate == 10.0
    
    @pytest.mark.asyncio
    async def test_calculate_churn_rate_no_customers(self, revenue_analytics):
        """Test churn rate calculation with no customers."""
        tenant_id = "tenant_1"
        months = 12
        
        with patch.object(revenue_analytics, '_get_customers_at_date', return_value=0):
            with patch.object(revenue_analytics, '_get_customers_lost_in_period', return_value=0):
                churn_rate = await revenue_analytics.calculate_churn_rate(tenant_id, months)
                
                assert churn_rate == 0.0
    
    @pytest.mark.asyncio
    async def test_calculate_customer_lifetime_value(self, revenue_analytics):
        """Test CLV calculation."""
        tenant_id = "tenant_1"
        
        with patch.object(revenue_analytics, '_get_average_monthly_revenue_per_customer', return_value=Decimal("100.00")):
            with patch.object(revenue_analytics, '_get_average_customer_lifespan', return_value=24):
                clv = await revenue_analytics.calculate_customer_lifetime_value(tenant_id)
                
                # 100.00 * 24 = 2400.00
                assert clv == Decimal("2400.00")
    
    @pytest.mark.asyncio
    async def test_generate_revenue_forecast(self, revenue_analytics, mock_monthly_revenue):
        """Test revenue forecast generation."""
        tenant_id = "tenant_1"
        months = 6
        
        with patch.object(revenue_analytics, '_get_monthly_revenue', return_value=mock_monthly_revenue):
            forecast = await revenue_analytics.generate_revenue_forecast(tenant_id, months)
            
            assert forecast.tenant_id == tenant_id
            assert forecast.forecast_period == f"{months}_months"
            assert forecast.predicted_revenue > Decimal("0.00")
            assert 0.0 <= forecast.confidence_level <= 1.0
            assert forecast.trend in ["increasing", "decreasing", "stable"]
    
    @pytest.mark.asyncio
    async def test_generate_revenue_forecast_insufficient_data(self, revenue_analytics):
        """Test revenue forecast generation with insufficient data."""
        tenant_id = "tenant_1"
        months = 6
        
        with patch.object(revenue_analytics, '_get_monthly_revenue', return_value=[]):
            forecast = await revenue_analytics.generate_revenue_forecast(tenant_id, months)
            
            assert forecast.tenant_id == tenant_id
            assert forecast.predicted_revenue == Decimal("0.00")
            assert forecast.confidence_level == 0.0
            assert forecast.trend == "insufficient_data"
    
    @pytest.mark.asyncio
    async def test_generate_revenue_metrics(self, revenue_analytics):
        """Test revenue metrics generation."""
        tenant_id = "tenant_1"
        period = "monthly"
        
        with patch.object(revenue_analytics, '_get_total_revenue', return_value=Decimal("10000.00")):
            with patch.object(revenue_analytics, 'calculate_mrr', return_value=Decimal("1000.00")):
                with patch.object(revenue_analytics, 'calculate_arr', return_value=Decimal("12000.00")):
                    with patch.object(revenue_analytics, '_get_customer_count', return_value=50):
                        with patch.object(revenue_analytics, 'calculate_revenue_growth_rate', return_value=15.0):
                            with patch.object(revenue_analytics, 'calculate_churn_rate', return_value=5.0):
                                with patch.object(revenue_analytics, 'calculate_customer_lifetime_value', return_value=Decimal("2000.00")):
                                    with patch.object(revenue_analytics, '_get_employee_count', return_value=10):
                                        with patch.object(revenue_analytics, '_calculate_gross_margin', return_value=80.0):
                                            metrics = await revenue_analytics.generate_revenue_metrics(tenant_id, period)
                                            
                                            assert metrics.period == period
                                            assert metrics.total_revenue == Decimal("10000.00")
                                            assert metrics.monthly_recurring_revenue == Decimal("1000.00")
                                            assert metrics.annual_recurring_revenue == Decimal("12000.00")
                                            assert metrics.average_revenue_per_customer == Decimal("200.00")  # 10000/50
                                            assert metrics.revenue_growth_rate == 15.0
                                            assert metrics.churn_rate == 5.0
                                            assert metrics.customer_lifetime_value == Decimal("2000.00")
                                            assert metrics.revenue_per_employee == Decimal("1000.00")  # 10000/10
                                            assert metrics.gross_margin == 80.0
    
    def test_calculate_revenue_trend_increasing(self, revenue_analytics):
        """Test revenue trend calculation for increasing trend."""
        historical_revenue = [
            Decimal("1000.00"),
            Decimal("1100.00"),
            Decimal("1200.00"),
            Decimal("1300.00"),
            Decimal("1400.00")
        ]
        
        trend = revenue_analytics._calculate_revenue_trend(historical_revenue)
        
        assert trend == "increasing"
    
    def test_calculate_revenue_trend_decreasing(self, revenue_analytics):
        """Test revenue trend calculation for decreasing trend."""
        historical_revenue = [
            Decimal("1400.00"),
            Decimal("1300.00"),
            Decimal("1200.00"),
            Decimal("1100.00"),
            Decimal("1000.00")
        ]
        
        trend = revenue_analytics._calculate_revenue_trend(historical_revenue)
        
        assert trend == "decreasing"
    
    def test_calculate_revenue_trend_stable(self, revenue_analytics):
        """Test revenue trend calculation for stable trend."""
        historical_revenue = [
            Decimal("1000.00"),
            Decimal("1000.00"),
            Decimal("1000.00"),
            Decimal("1000.00"),
            Decimal("1000.00")
        ]
        
        trend = revenue_analytics._calculate_revenue_trend(historical_revenue)
        
        assert trend == "stable"
    
    def test_calculate_revenue_trend_insufficient_data(self, revenue_analytics):
        """Test revenue trend calculation with insufficient data."""
        historical_revenue = [Decimal("1000.00")]
        
        trend = revenue_analytics._calculate_revenue_trend(historical_revenue)
        
        assert trend == "stable"
    
    def test_calculate_seasonal_adjustment(self, revenue_analytics):
        """Test seasonal adjustment calculation."""
        historical_revenue = [
            Decimal("1000.00"),
            Decimal("1100.00"),
            Decimal("1200.00"),
            Decimal("1300.00"),
            Decimal("1400.00")
        ]
        
        adjustment = revenue_analytics._calculate_seasonal_adjustment(historical_revenue)
        
        assert isinstance(adjustment, float)
        assert adjustment > 0  # Should be positive for increasing trend
    
    def test_calculate_seasonal_adjustment_insufficient_data(self, revenue_analytics):
        """Test seasonal adjustment calculation with insufficient data."""
        historical_revenue = [Decimal("1000.00")]
        
        adjustment = revenue_analytics._calculate_seasonal_adjustment(historical_revenue)
        
        assert adjustment == 0.0
    
    def test_predict_revenue(self, revenue_analytics):
        """Test revenue prediction."""
        historical_revenue = [
            Decimal("1000.00"),
            Decimal("1100.00"),
            Decimal("1200.00"),
            Decimal("1300.00"),
            Decimal("1400.00")
        ]
        months = 3
        trend = "increasing"
        seasonal_adjustment = 0.1
        
        predicted = revenue_analytics._predict_revenue(historical_revenue, months, trend, seasonal_adjustment)
        
        assert predicted > Decimal("1400.00")  # Should be higher than last known value
    
    def test_predict_revenue_decreasing_trend(self, revenue_analytics):
        """Test revenue prediction with decreasing trend."""
        historical_revenue = [
            Decimal("1400.00"),
            Decimal("1300.00"),
            Decimal("1200.00"),
            Decimal("1100.00"),
            Decimal("1000.00")
        ]
        months = 3
        trend = "decreasing"
        seasonal_adjustment = 0.1
        
        predicted = revenue_analytics._predict_revenue(historical_revenue, months, trend, seasonal_adjustment)
        
        assert predicted < Decimal("1000.00")  # Should be lower than last known value
    
    def test_predict_revenue_stable_trend(self, revenue_analytics):
        """Test revenue prediction with stable trend."""
        historical_revenue = [
            Decimal("1000.00"),
            Decimal("1000.00"),
            Decimal("1000.00"),
            Decimal("1000.00"),
            Decimal("1000.00")
        ]
        months = 3
        trend = "stable"
        seasonal_adjustment = 0.0
        
        predicted = revenue_analytics._predict_revenue(historical_revenue, months, trend, seasonal_adjustment)
        
        assert predicted == Decimal("1000.00")  # Should be same as last known value
    
    def test_calculate_forecast_confidence(self, revenue_analytics):
        """Test forecast confidence calculation."""
        historical_revenue = [
            Decimal("1000.00"),
            Decimal("1100.00"),
            Decimal("1200.00"),
            Decimal("1300.00"),
            Decimal("1400.00")
        ]
        months = 3
        
        confidence = revenue_analytics._calculate_forecast_confidence(historical_revenue, months)
        
        assert 0.0 <= confidence <= 1.0
        assert confidence > 0.5  # Should have reasonable confidence for stable data
    
    def test_calculate_forecast_confidence_insufficient_data(self, revenue_analytics):
        """Test forecast confidence calculation with insufficient data."""
        historical_revenue = [Decimal("1000.00")]
        months = 3
        
        confidence = revenue_analytics._calculate_forecast_confidence(historical_revenue, months)
        
        assert confidence == 0.0
    
    def test_calculate_forecast_confidence_zero_mean(self, revenue_analytics):
        """Test forecast confidence calculation with zero mean."""
        historical_revenue = [Decimal("0.00"), Decimal("0.00"), Decimal("0.00")]
        months = 3
        
        confidence = revenue_analytics._calculate_forecast_confidence(historical_revenue, months)
        
        assert confidence == 0.0
