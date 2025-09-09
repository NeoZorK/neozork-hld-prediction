"""
Revenue analytics and forecasting.
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from dataclasses import dataclass
import statistics

from src.saas.billing.models.payment import Payment, PaymentStatus
from src.saas.billing.models.invoice import Invoice, InvoiceStatus


@dataclass
class RevenueForecast:
    """Revenue forecast data structure."""
    forecast_id: str
    tenant_id: str
    forecast_period: str
    predicted_revenue: Decimal
    confidence_level: float
    forecast_date: datetime
    historical_data_points: int
    trend: str
    seasonal_adjustment: float
    created_at: datetime


@dataclass
class RevenueMetrics:
    """Revenue metrics data structure."""
    period: str
    total_revenue: Decimal
    monthly_recurring_revenue: Decimal
    annual_recurring_revenue: Decimal
    average_revenue_per_customer: Decimal
    revenue_growth_rate: float
    churn_rate: float
    customer_lifetime_value: Decimal
    revenue_per_employee: Decimal
    gross_margin: float


class RevenueAnalytics:
    """Service for revenue analytics and forecasting."""
    
    def __init__(self, payment_service, invoice_service):
        """
        Initialize revenue analytics service.
        
        Args:
            payment_service: Payment service instance
            invoice_service: Invoice service instance
        """
        self.payment_service = payment_service
        self.invoice_service = invoice_service
    
    async def calculate_mrr(self, tenant_id: str, date: datetime) -> Decimal:
        """
        Calculate Monthly Recurring Revenue (MRR) for a tenant.
        
        Args:
            tenant_id: Tenant identifier
            date: Date to calculate MRR for
            
        Returns:
            MRR amount
        """
        # Get all active subscriptions for the tenant
        subscriptions = await self._get_active_subscriptions(tenant_id, date)
        
        mrr = Decimal("0.00")
        for subscription in subscriptions:
            if subscription.get("billing_cycle") == "monthly":
                mrr += subscription.get("amount", Decimal("0.00"))
            elif subscription.get("billing_cycle") == "yearly":
                # Convert yearly to monthly
                mrr += subscription.get("amount", Decimal("0.00")) / 12
        
        return mrr
    
    async def calculate_arr(self, tenant_id: str, date: datetime) -> Decimal:
        """
        Calculate Annual Recurring Revenue (ARR) for a tenant.
        
        Args:
            tenant_id: Tenant identifier
            date: Date to calculate ARR for
            
        Returns:
            ARR amount
        """
        # Get all active subscriptions for the tenant
        subscriptions = await self._get_active_subscriptions(tenant_id, date)
        
        arr = Decimal("0.00")
        for subscription in subscriptions:
            if subscription.get("billing_cycle") == "yearly":
                arr += subscription.get("amount", Decimal("0.00"))
            elif subscription.get("billing_cycle") == "monthly":
                # Convert monthly to yearly
                arr += subscription.get("amount", Decimal("0.00")) * 12
        
        return arr
    
    async def calculate_revenue_growth_rate(self, tenant_id: str, months: int = 12) -> float:
        """
        Calculate revenue growth rate for a tenant.
        
        Args:
            tenant_id: Tenant identifier
            months: Number of months to analyze
            
        Returns:
            Growth rate percentage
        """
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=months * 30)
        
        # Get monthly revenue data
        monthly_revenue = await self._get_monthly_revenue(tenant_id, start_date, end_date)
        
        if len(monthly_revenue) < 2:
            return 0.0
        
        # Calculate growth rate using first and last month
        first_month_revenue = monthly_revenue[0]
        last_month_revenue = monthly_revenue[-1]
        
        if first_month_revenue == 0:
            return 0.0
        
        growth_rate = ((last_month_revenue - first_month_revenue) / first_month_revenue) * 100
        return growth_rate
    
    async def calculate_churn_rate(self, tenant_id: str, months: int = 12) -> float:
        """
        Calculate customer churn rate.
        
        Args:
            tenant_id: Tenant identifier
            months: Number of months to analyze
            
        Returns:
            Churn rate percentage
        """
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=months * 30)
        
        # Get customer data
        customers_at_start = await self._get_customers_at_date(tenant_id, start_date)
        customers_lost = await self._get_customers_lost_in_period(tenant_id, start_date, end_date)
        
        if customers_at_start == 0:
            return 0.0
        
        churn_rate = (customers_lost / customers_at_start) * 100
        return churn_rate
    
    async def calculate_customer_lifetime_value(self, tenant_id: str) -> Decimal:
        """
        Calculate Customer Lifetime Value (CLV).
        
        Args:
            tenant_id: Tenant identifier
            
        Returns:
            CLV amount
        """
        # Get average monthly revenue per customer
        avg_monthly_revenue = await self._get_average_monthly_revenue_per_customer(tenant_id)
        
        # Get average customer lifespan in months
        avg_lifespan_months = await self._get_average_customer_lifespan(tenant_id)
        
        # Calculate CLV
        clv = avg_monthly_revenue * avg_lifespan_months
        return clv
    
    async def generate_revenue_forecast(self, tenant_id: str, months: int = 6) -> RevenueForecast:
        """
        Generate revenue forecast for a tenant.
        
        Args:
            tenant_id: Tenant identifier
            months: Number of months to forecast
            
        Returns:
            Revenue forecast
        """
        # Get historical revenue data
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=12 * 30)  # 12 months of history
        
        historical_revenue = await self._get_monthly_revenue(tenant_id, start_date, end_date)
        
        if len(historical_revenue) < 3:
            # Not enough data for forecasting
            return RevenueForecast(
                forecast_id=f"forecast_{tenant_id}_{int(datetime.now().timestamp())}",
                tenant_id=tenant_id,
                forecast_period=f"{months}_months",
                predicted_revenue=Decimal("0.00"),
                confidence_level=0.0,
                forecast_date=datetime.now(timezone.utc),
                historical_data_points=len(historical_revenue),
                trend="insufficient_data",
                seasonal_adjustment=0.0,
                created_at=datetime.now(timezone.utc)
            )
        
        # Calculate trend
        trend = self._calculate_revenue_trend(historical_revenue)
        
        # Calculate seasonal adjustment
        seasonal_adjustment = self._calculate_seasonal_adjustment(historical_revenue)
        
        # Generate forecast
        predicted_revenue = self._predict_revenue(historical_revenue, months, trend, seasonal_adjustment)
        
        # Calculate confidence level
        confidence_level = self._calculate_forecast_confidence(historical_revenue, months)
        
        return RevenueForecast(
            forecast_id=f"forecast_{tenant_id}_{int(datetime.now().timestamp())}",
            tenant_id=tenant_id,
            forecast_period=f"{months}_months",
            predicted_revenue=predicted_revenue,
            confidence_level=confidence_level,
            forecast_date=datetime.now(timezone.utc),
            historical_data_points=len(historical_revenue),
            trend=trend,
            seasonal_adjustment=seasonal_adjustment,
            created_at=datetime.now(timezone.utc)
        )
    
    async def generate_revenue_metrics(self, tenant_id: str, period: str = "monthly") -> RevenueMetrics:
        """
        Generate comprehensive revenue metrics.
        
        Args:
            tenant_id: Tenant identifier
            period: Analysis period (monthly, quarterly, yearly)
            
        Returns:
            Revenue metrics
        """
        end_date = datetime.now(timezone.utc)
        
        if period == "monthly":
            start_date = end_date - timedelta(days=30)
        elif period == "quarterly":
            start_date = end_date - timedelta(days=90)
        else:  # yearly
            start_date = end_date - timedelta(days=365)
        
        # Get revenue data
        total_revenue = await self._get_total_revenue(tenant_id, start_date, end_date)
        mrr = await self.calculate_mrr(tenant_id, end_date)
        arr = await self.calculate_arr(tenant_id, end_date)
        
        # Get customer data
        customer_count = await self._get_customer_count(tenant_id, end_date)
        avg_revenue_per_customer = total_revenue / customer_count if customer_count > 0 else Decimal("0.00")
        
        # Calculate growth and churn rates
        growth_rate = await self.calculate_revenue_growth_rate(tenant_id)
        churn_rate = await self.calculate_churn_rate(tenant_id)
        
        # Calculate CLV
        clv = await self.calculate_customer_lifetime_value(tenant_id)
        
        # Calculate revenue per employee (placeholder)
        employee_count = await self._get_employee_count(tenant_id)
        revenue_per_employee = total_revenue / employee_count if employee_count > 0 else Decimal("0.00")
        
        # Calculate gross margin (placeholder)
        gross_margin = await self._calculate_gross_margin(tenant_id, start_date, end_date)
        
        return RevenueMetrics(
            period=period,
            total_revenue=total_revenue,
            monthly_recurring_revenue=mrr,
            annual_recurring_revenue=arr,
            average_revenue_per_customer=avg_revenue_per_customer,
            revenue_growth_rate=growth_rate,
            churn_rate=churn_rate,
            customer_lifetime_value=clv,
            revenue_per_employee=revenue_per_employee,
            gross_margin=gross_margin
        )
    
    async def _get_active_subscriptions(self, tenant_id: str, date: datetime) -> List[Dict[str, Any]]:
        """Get active subscriptions for a tenant at a specific date."""
        # This would typically query the database
        # For now, return empty list as placeholder
        return []
    
    async def _get_monthly_revenue(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Decimal]:
        """Get monthly revenue data for a tenant."""
        # This would typically query the database
        # For now, return empty list as placeholder
        return []
    
    async def _get_customers_at_date(self, tenant_id: str, date: datetime) -> int:
        """Get customer count at a specific date."""
        # This would typically query the database
        # For now, return 0 as placeholder
        return 0
    
    async def _get_customers_lost_in_period(self, tenant_id: str, start_date: datetime, end_date: datetime) -> int:
        """Get number of customers lost in a period."""
        # This would typically query the database
        # For now, return 0 as placeholder
        return 0
    
    async def _get_average_monthly_revenue_per_customer(self, tenant_id: str) -> Decimal:
        """Get average monthly revenue per customer."""
        # This would typically query the database
        # For now, return 0 as placeholder
        return Decimal("0.00")
    
    async def _get_average_customer_lifespan(self, tenant_id: str) -> int:
        """Get average customer lifespan in months."""
        # This would typically query the database
        # For now, return 12 as placeholder
        return 12
    
    async def _get_total_revenue(self, tenant_id: str, start_date: datetime, end_date: datetime) -> Decimal:
        """Get total revenue for a period."""
        # This would typically query the database
        # For now, return 0 as placeholder
        return Decimal("0.00")
    
    async def _get_customer_count(self, tenant_id: str, date: datetime) -> int:
        """Get customer count at a specific date."""
        # This would typically query the database
        # For now, return 0 as placeholder
        return 0
    
    async def _get_employee_count(self, tenant_id: str) -> int:
        """Get employee count for a tenant."""
        # This would typically query the database
        # For now, return 1 as placeholder
        return 1
    
    async def _calculate_gross_margin(self, tenant_id: str, start_date: datetime, end_date: datetime) -> float:
        """Calculate gross margin for a period."""
        # This would typically calculate based on revenue and costs
        # For now, return 0.8 as placeholder (80% margin)
        return 80.0
    
    def _calculate_revenue_trend(self, historical_revenue: List[Decimal]) -> str:
        """Calculate revenue trend from historical data."""
        if len(historical_revenue) < 2:
            return "stable"
        
        # Convert to float for trend calculation
        values = [float(revenue) for revenue in historical_revenue]
        
        # Simple linear regression
        n = len(values)
        x_sum = sum(range(n))
        y_sum = sum(values)
        xy_sum = sum(i * values[i] for i in range(n))
        x_squared_sum = sum(i * i for i in range(n))
        
        if n * x_squared_sum - x_sum * x_sum == 0:
            return "stable"
        
        slope = (n * xy_sum - x_sum * y_sum) / (n * x_squared_sum - x_sum * x_sum)
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_seasonal_adjustment(self, historical_revenue: List[Decimal]) -> float:
        """Calculate seasonal adjustment factor."""
        if len(historical_revenue) < 12:
            return 0.0
        
        # Simple seasonal adjustment based on month-over-month variation
        monthly_variations = []
        for i in range(1, len(historical_revenue)):
            if historical_revenue[i-1] > 0:
                variation = (historical_revenue[i] - historical_revenue[i-1]) / historical_revenue[i-1]
                monthly_variations.append(variation)
        
        if not monthly_variations:
            return 0.0
        
        # Calculate average variation
        avg_variation = statistics.mean(monthly_variations)
        return avg_variation
    
    def _predict_revenue(self, historical_revenue: List[Decimal], months: int, trend: str, seasonal_adjustment: float) -> Decimal:
        """Predict future revenue based on historical data."""
        if not historical_revenue:
            return Decimal("0.00")
        
        # Get the last known revenue
        last_revenue = historical_revenue[-1]
        
        # Apply trend and seasonal adjustment
        if trend == "increasing":
            growth_factor = 1.0 + abs(seasonal_adjustment)
        elif trend == "decreasing":
            growth_factor = 1.0 - abs(seasonal_adjustment)
        else:
            growth_factor = 1.0
        
        # Predict revenue for the specified number of months
        predicted_revenue = last_revenue * (growth_factor ** months)
        
        return predicted_revenue
    
    def _calculate_forecast_confidence(self, historical_revenue: List[Decimal], months: int) -> float:
        """Calculate forecast confidence level."""
        if len(historical_revenue) < 3:
            return 0.0
        
        # Calculate coefficient of variation
        values = [float(revenue) for revenue in historical_revenue]
        mean_value = statistics.mean(values)
        std_dev = statistics.stdev(values) if len(values) > 1 else 0
        
        if mean_value == 0:
            return 0.0
        
        coefficient_of_variation = std_dev / mean_value
        
        # Calculate confidence based on data stability and forecast horizon
        base_confidence = max(0.0, 1.0 - coefficient_of_variation)
        horizon_penalty = min(0.3, months * 0.05)  # Penalty for longer forecasts
        
        confidence = base_confidence - horizon_penalty
        return max(0.0, min(1.0, confidence))
