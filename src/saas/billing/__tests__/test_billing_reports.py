"""
Test cases for billing reports.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from decimal import Decimal
from datetime import datetime, timezone, timedelta

from src.saas.billing.reports.billing_reports import BillingReports, BillingReport
from src.saas.billing.models.payment import Payment, PaymentStatus, PaymentMethod
from src.saas.billing.models.invoice import Invoice, InvoiceStatus


class TestBillingReports:
    """Test cases for BillingReports."""
    
    @pytest.fixture
    def billing_reports(self):
        """Create BillingReports instance for testing."""
        payment_service = Mock()
        invoice_service = Mock()
        return BillingReports(payment_service, invoice_service)
    
    @pytest.fixture
    def mock_payments(self):
        """Create mock payments for testing."""
        return [
            Payment(
                id="pay_1",
                tenant_id="tenant_1",
                amount=Decimal("100.00"),
                currency="USD",
                status=PaymentStatus.COMPLETED,
                payment_method=PaymentMethod.CREDIT_CARD,
                created_at=datetime.now(timezone.utc)
            ),
            Payment(
                id="pay_2",
                tenant_id="tenant_1",
                amount=Decimal("50.00"),
                currency="USD",
                status=PaymentStatus.FAILED,
                payment_method=PaymentMethod.BANK_TRANSFER,
                created_at=datetime.now(timezone.utc)
            ),
            Payment(
                id="pay_3",
                tenant_id="tenant_1",
                amount=Decimal("75.00"),
                currency="USD",
                status=PaymentStatus.COMPLETED,
                payment_method=PaymentMethod.CREDIT_CARD,
                created_at=datetime.now(timezone.utc)
            )
        ]
    
    @pytest.fixture
    def mock_invoices(self):
        """Create mock invoices for testing."""
        return [
            Invoice(
                id="inv_1",
                tenant_id="tenant_1",
                amount=Decimal("200.00"),
                currency="USD",
                status=InvoiceStatus.PAID,
                due_date=datetime.now(timezone.utc)
            ),
            Invoice(
                id="inv_2",
                tenant_id="tenant_1",
                amount=Decimal("150.00"),
                currency="USD",
                status=InvoiceStatus.OVERDUE,
                due_date=datetime.now(timezone.utc)
            )
        ]
    
    @pytest.mark.asyncio
    async def test_generate_tenant_report(self, billing_reports, mock_payments, mock_invoices):
        """Test tenant report generation."""
        tenant_id = "tenant_1"
        start_date = datetime.now(timezone.utc) - timedelta(days=30)
        end_date = datetime.now(timezone.utc)
        
        with patch.object(billing_reports, '_get_payments_for_period', return_value=mock_payments):
            with patch.object(billing_reports, '_get_invoices_for_period', return_value=mock_invoices):
                report = await billing_reports.generate_tenant_report(tenant_id, start_date, end_date)
                
                assert report.tenant_id == tenant_id
                assert report.report_type == "tenant_billing"
                assert report.total_revenue == Decimal("175.00")  # 100 + 75
                assert report.total_payments == 3
                assert report.successful_payments == 2
                assert report.failed_payments == 1
                assert report.total_invoices == 2
                assert report.paid_invoices == 1
                assert report.overdue_invoices == 1
    
    @pytest.mark.asyncio
    async def test_generate_revenue_report(self, billing_reports, mock_payments, mock_invoices):
        """Test revenue report generation."""
        start_date = datetime.now(timezone.utc) - timedelta(days=30)
        end_date = datetime.now(timezone.utc)
        
        with patch.object(billing_reports, '_get_all_payments_for_period', return_value=mock_payments):
            with patch.object(billing_reports, '_get_all_invoices_for_period', return_value=mock_invoices):
                report = await billing_reports.generate_revenue_report(start_date, end_date)
                
                assert report.tenant_id == "all"
                assert report.report_type == "revenue"
                assert report.total_revenue == Decimal("175.00")
                assert report.total_payments == 3
                assert report.successful_payments == 2
                assert report.failed_payments == 1
    
    @pytest.mark.asyncio
    async def test_generate_payment_analytics(self, billing_reports, mock_payments):
        """Test payment analytics generation."""
        tenant_id = "tenant_1"
        days = 30
        
        with patch.object(billing_reports, '_get_payments_for_period', return_value=mock_payments):
            analytics = await billing_reports.generate_payment_analytics(tenant_id, days)
            
            assert analytics["total_payments"] == 3
            assert analytics["success_rate"] == 66.67  # 2/3 * 100
            assert analytics["average_payment_amount"] == Decimal("75.00")  # (100+50+75)/3
    
    def test_group_payments_by_status(self, billing_reports, mock_payments):
        """Test grouping payments by status."""
        result = billing_reports._group_payments_by_status(mock_payments)
        
        assert result["completed"] == 2
        assert result["failed"] == 1
    
    def test_group_payments_by_method(self, billing_reports, mock_payments):
        """Test grouping payments by method."""
        result = billing_reports._group_payments_by_method(mock_payments)
        
        assert result["credit_card"] == 2
        assert result["bank_transfer"] == 1
    
    def test_calculate_monthly_revenue(self, billing_reports, mock_payments):
        """Test monthly revenue calculation."""
        start_date = datetime.now(timezone.utc) - timedelta(days=30)
        end_date = datetime.now(timezone.utc)
        
        result = billing_reports._calculate_monthly_revenue(mock_payments, start_date, end_date)
        
        # Should have current month's revenue
        current_month = datetime.now(timezone.utc).strftime("%Y-%m")
        assert current_month in result
        assert result[current_month] == Decimal("175.00")  # 100 + 75
    
    def test_calculate_invoice_summary(self, billing_reports, mock_invoices):
        """Test invoice summary calculation."""
        result = billing_reports._calculate_invoice_summary(mock_invoices)
        
        assert result["total_amount"] == Decimal("350.00")  # 200 + 150
        assert result["paid_amount"] == Decimal("200.00")
        assert result["overdue_amount"] == Decimal("150.00")
        assert result["collection_rate"] == 57.14  # 200/350 * 100
    
    def test_calculate_payment_trends(self, billing_reports, mock_payments):
        """Test payment trends calculation."""
        start_date = datetime.now(timezone.utc) - timedelta(days=7)
        end_date = datetime.now(timezone.utc)
        
        result = billing_reports._calculate_payment_trends(mock_payments, start_date, end_date)
        
        assert "daily_payment_counts" in result
        assert "trend_direction" in result
        assert result["trend_direction"] in ["increasing", "decreasing", "stable"]
    
    def test_calculate_revenue_by_tenant(self, billing_reports, mock_payments):
        """Test revenue calculation by tenant."""
        result = billing_reports._calculate_revenue_by_tenant(mock_payments)
        
        assert "tenant_1" in result
        assert result["tenant_1"] == Decimal("175.00")  # 100 + 75
    
    def test_get_top_tenants_by_revenue(self, billing_reports, mock_payments):
        """Test getting top tenants by revenue."""
        result = billing_reports._get_top_tenants_by_revenue(mock_payments, limit=5)
        
        assert len(result) == 1
        assert result[0]["tenant_id"] == "tenant_1"
        assert result[0]["revenue"] == Decimal("175.00")
    
    def test_calculate_conversion_rates(self, billing_reports, mock_payments, mock_invoices):
        """Test conversion rates calculation."""
        result = billing_reports._calculate_conversion_rates(mock_payments, mock_invoices)
        
        assert result["payment_success_rate"] == 66.67  # 2/3 * 100
        assert result["invoice_payment_rate"] == 50.0  # 1/2 * 100
    
    def test_calculate_success_rate(self, billing_reports, mock_payments):
        """Test success rate calculation."""
        result = billing_reports._calculate_success_rate(mock_payments)
        
        assert result == 66.67  # 2/3 * 100
    
    def test_calculate_success_rate_no_payments(self, billing_reports):
        """Test success rate calculation with no payments."""
        result = billing_reports._calculate_success_rate([])
        
        assert result == 0.0
    
    def test_calculate_average_payment_amount(self, billing_reports, mock_payments):
        """Test average payment amount calculation."""
        result = billing_reports._calculate_average_payment_amount(mock_payments)
        
        assert result == Decimal("75.00")  # (100+50+75)/3
    
    def test_calculate_average_payment_amount_no_payments(self, billing_reports):
        """Test average payment amount calculation with no payments."""
        result = billing_reports._calculate_average_payment_amount([])
        
        assert result == Decimal("0.00")
    
    def test_calculate_daily_payment_volume(self, billing_reports, mock_payments):
        """Test daily payment volume calculation."""
        start_date = datetime.now(timezone.utc) - timedelta(days=7)
        end_date = datetime.now(timezone.utc)
        
        result = billing_reports._calculate_daily_payment_volume(mock_payments, start_date, end_date)
        
        assert len(result) == 8  # 7 days + 1
        assert all(isinstance(count, int) for count in result.values())
    
    def test_analyze_failed_payments(self, billing_reports, mock_payments):
        """Test failed payment analysis."""
        # Add failure reason to one payment
        mock_payments[1].failure_reason = "Insufficient funds"
        
        result = billing_reports._analyze_failed_payments(mock_payments)
        
        assert "Insufficient funds" in result
        assert result["Insufficient funds"] == 1
    
    def test_calculate_revenue_trend(self, billing_reports, mock_payments):
        """Test revenue trend calculation."""
        start_date = datetime.now(timezone.utc) - timedelta(days=7)
        end_date = datetime.now(timezone.utc)
        
        result = billing_reports._calculate_revenue_trend(mock_payments, start_date, end_date)
        
        assert "daily_revenue" in result
        assert "trend_direction" in result
        assert "total_revenue" in result
        assert result["trend_direction"] in ["increasing", "decreasing", "stable"]
    
    def test_calculate_trend_direction_increasing(self, billing_reports):
        """Test trend direction calculation for increasing trend."""
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = billing_reports._calculate_trend_direction(values)
        
        assert result == "increasing"
    
    def test_calculate_trend_direction_decreasing(self, billing_reports):
        """Test trend direction calculation for decreasing trend."""
        values = [5.0, 4.0, 3.0, 2.0, 1.0]
        result = billing_reports._calculate_trend_direction(values)
        
        assert result == "decreasing"
    
    def test_calculate_trend_direction_stable(self, billing_reports):
        """Test trend direction calculation for stable trend."""
        values = [1.0, 1.0, 1.0, 1.0, 1.0]
        result = billing_reports._calculate_trend_direction(values)
        
        assert result == "stable"
    
    def test_calculate_trend_direction_insufficient_data(self, billing_reports):
        """Test trend direction calculation with insufficient data."""
        values = [1.0]
        result = billing_reports._calculate_trend_direction(values)
        
        assert result == "stable"
