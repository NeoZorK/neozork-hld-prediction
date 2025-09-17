"""
Billing reports generation and management.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from dataclasses import dataclass

from src.saas.billing.models.payment import Payment, PaymentStatus
from src.saas.billing.models.invoice import Invoice, InvoiceStatus


@dataclass
class BillingReport:
    """Billing report data structure."""
    report_id: str
    tenant_id: str
    report_type: str
    period_start: datetime
    period_end: datetime
    total_revenue: Decimal
    total_payments: int
    successful_payments: int
    failed_payments: int
    total_invoices: int
    paid_invoices: int
    overdue_invoices: int
    created_at: datetime
    data: Dict[str, Any]


class BillingReports:
    """Service for generating billing reports."""
    
    def __init__(self, payment_service, invoice_service):
        """
        Initialize billing reports service.
        
        Args:
            payment_service: Payment service instance
            invoice_service: Invoice service instance
        """
        self.payment_service = payment_service
        self.invoice_service = invoice_service
    
    async def generate_tenant_report(self, tenant_id: str, start_date: datetime, end_date: datetime) -> BillingReport:
        """
        Generate billing report for a specific tenant.
        
        Args:
            tenant_id: Tenant identifier
            start_date: Report start date
            end_date: Report end date
            
        Returns:
            Billing report
        """
        # Get payments for the period
        payments = await self._get_payments_for_period(tenant_id, start_date, end_date)
        
        # Get invoices for the period
        invoices = await self._get_invoices_for_period(tenant_id, start_date, end_date)
        
        # Calculate metrics
        total_revenue = sum(p.amount for p in payments if p.status == PaymentStatus.COMPLETED)
        total_payments = len(payments)
        successful_payments = len([p for p in payments if p.status == PaymentStatus.COMPLETED])
        failed_payments = len([p for p in payments if p.status == PaymentStatus.FAILED])
        
        total_invoices = len(invoices)
        paid_invoices = len([i for i in invoices if i.status == InvoiceStatus.PAID])
        overdue_invoices = len([i for i in invoices if i.status == InvoiceStatus.OVERDUE])
        
        # Generate report data
        report_data = {
            "payments_by_status": self._group_payments_by_status(payments),
            "payments_by_method": self._group_payments_by_method(payments),
            "monthly_revenue": self._calculate_monthly_revenue(payments, start_date, end_date),
            "invoice_summary": self._calculate_invoice_summary(invoices),
            "payment_trends": self._calculate_payment_trends(payments, start_date, end_date)
        }
        
        return BillingReport(
            report_id=f"report_{tenant_id}_{int(start_date.timestamp())}",
            tenant_id=tenant_id,
            report_type="tenant_billing",
            period_start=start_date,
            period_end=end_date,
            total_revenue=total_revenue,
            total_payments=total_payments,
            successful_payments=successful_payments,
            failed_payments=failed_payments,
            total_invoices=total_invoices,
            paid_invoices=paid_invoices,
            overdue_invoices=overdue_invoices,
            created_at=datetime.now(timezone.utc),
            data=report_data
        )
    
    async def generate_revenue_report(self, start_date: datetime, end_date: datetime) -> BillingReport:
        """
        Generate revenue report for all tenants.
        
        Args:
            start_date: Report start date
            end_date: Report end date
            
        Returns:
            Revenue report
        """
        # Get all payments for the period
        all_payments = await self._get_all_payments_for_period(start_date, end_date)
        all_invoices = await self._get_all_invoices_for_period(start_date, end_date)
        
        # Calculate metrics
        total_revenue = sum(p.amount for p in all_payments if p.status == PaymentStatus.COMPLETED)
        total_payments = len(all_payments)
        successful_payments = len([p for p in all_payments if p.status == PaymentStatus.COMPLETED])
        failed_payments = len([p for p in all_payments if p.status == PaymentStatus.FAILED])
        
        total_invoices = len(all_invoices)
        paid_invoices = len([i for i in all_invoices if i.status == InvoiceStatus.PAID])
        overdue_invoices = len([i for i in all_invoices if i.status == InvoiceStatus.OVERDUE])
        
        # Generate report data
        report_data = {
            "revenue_by_tenant": self._calculate_revenue_by_tenant(all_payments),
            "revenue_by_month": self._calculate_monthly_revenue(all_payments, start_date, end_date),
            "payment_methods": self._group_payments_by_method(all_payments),
            "top_tenants": self._get_top_tenants_by_revenue(all_payments),
            "conversion_rates": self._calculate_conversion_rates(all_payments, all_invoices)
        }
        
        return BillingReport(
            report_id=f"revenue_report_{int(start_date.timestamp())}",
            tenant_id="all",
            report_type="revenue",
            period_start=start_date,
            period_end=end_date,
            total_revenue=total_revenue,
            total_payments=total_payments,
            successful_payments=successful_payments,
            failed_payments=failed_payments,
            total_invoices=total_invoices,
            paid_invoices=paid_invoices,
            overdue_invoices=overdue_invoices,
            created_at=datetime.now(timezone.utc),
            data=report_data
        )
    
    async def generate_payment_analytics(self, tenant_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Generate payment analytics for a tenant.
        
        Args:
            tenant_id: Tenant identifier
            days: Number of days to analyze
            
        Returns:
            Analytics data
        """
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)
        
        payments = await self._get_payments_for_period(tenant_id, start_date, end_date)
        
        return {
            "total_payments": len(payments),
            "success_rate": self._calculate_success_rate(payments),
            "average_payment_amount": self._calculate_average_payment_amount(payments),
            "payment_volume_by_day": self._calculate_daily_payment_volume(payments, start_date, end_date),
            "failed_payment_reasons": self._analyze_failed_payments(payments),
            "payment_method_distribution": self._group_payments_by_method(payments),
            "revenue_trend": self._calculate_revenue_trend(payments, start_date, end_date)
        }
    
    async def _get_payments_for_period(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Payment]:
        """Get payments for a specific tenant and period."""
        # This would typically query the database
        # For now, return empty list as placeholder
        return []
    
    async def _get_invoices_for_period(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Invoice]:
        """Get invoices for a specific tenant and period."""
        # This would typically query the database
        # For now, return empty list as placeholder
        return []
    
    async def _get_all_payments_for_period(self, start_date: datetime, end_date: datetime) -> List[Payment]:
        """Get all payments for a period."""
        # This would typically query the database
        # For now, return empty list as placeholder
        return []
    
    async def _get_all_invoices_for_period(self, start_date: datetime, end_date: datetime) -> List[Invoice]:
        """Get all invoices for a period."""
        # This would typically query the database
        # For now, return empty list as placeholder
        return []
    
    def _group_payments_by_status(self, payments: List[Payment]) -> Dict[str, int]:
        """Group payments by status."""
        status_counts = {}
        for payment in payments:
            status = payment.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        return status_counts
    
    def _group_payments_by_method(self, payments: List[Payment]) -> Dict[str, int]:
        """Group payments by payment method."""
        method_counts = {}
        for payment in payments:
            method = payment.payment_method.value
            method_counts[method] = method_counts.get(method, 0) + 1
        return method_counts
    
    def _calculate_monthly_revenue(self, payments: List[Payment], start_date: datetime, end_date: datetime) -> Dict[str, Decimal]:
        """Calculate monthly revenue breakdown."""
        monthly_revenue = {}
        current_date = start_date.replace(day=1)
        
        while current_date <= end_date:
            month_key = current_date.strftime("%Y-%m")
            monthly_revenue[month_key] = Decimal("0.00")
            current_date = current_date.replace(day=1) + timedelta(days=32)
            current_date = current_date.replace(day=1)
        
        for payment in payments:
            if payment.status == PaymentStatus.COMPLETED:
                month_key = payment.created_at.strftime("%Y-%m")
                if month_key in monthly_revenue:
                    monthly_revenue[month_key] += payment.amount
        
        return monthly_revenue
    
    def _calculate_invoice_summary(self, invoices: List[Invoice]) -> Dict[str, Any]:
        """Calculate invoice summary statistics."""
        total_amount = sum(i.amount for i in invoices)
        paid_amount = sum(i.amount for i in invoices if i.status == InvoiceStatus.PAID)
        overdue_amount = sum(i.amount for i in invoices if i.status == InvoiceStatus.OVERDUE)
        
        return {
            "total_amount": total_amount,
            "paid_amount": paid_amount,
            "overdue_amount": overdue_amount,
            "collection_rate": (paid_amount / total_amount * 100) if total_amount > 0 else 0
        }
    
    def _calculate_payment_trends(self, payments: List[Payment], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Calculate payment trends."""
        daily_payments = {}
        current_date = start_date
        
        while current_date <= end_date:
            date_key = current_date.strftime("%Y-%m-%d")
            daily_payments[date_key] = 0
            current_date += timedelta(days=1)
        
        for payment in payments:
            if payment.status == PaymentStatus.COMPLETED:
                date_key = payment.created_at.strftime("%Y-%m-%d")
                if date_key in daily_payments:
                    daily_payments[date_key] += 1
        
        return {
            "daily_payment_counts": daily_payments,
            "trend_direction": self._calculate_trend_direction(list(daily_payments.values()))
        }
    
    def _calculate_revenue_by_tenant(self, payments: List[Payment]) -> Dict[str, Decimal]:
        """Calculate revenue by tenant."""
        tenant_revenue = {}
        for payment in payments:
            if payment.status == PaymentStatus.COMPLETED:
                tenant_id = payment.tenant_id
                tenant_revenue[tenant_id] = tenant_revenue.get(tenant_id, Decimal("0.00")) + payment.amount
        return tenant_revenue
    
    def _get_top_tenants_by_revenue(self, payments: List[Payment], limit: int = 10) -> List[Dict[str, Any]]:
        """Get top tenants by revenue."""
        tenant_revenue = self._calculate_revenue_by_tenant(payments)
        sorted_tenants = sorted(tenant_revenue.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {"tenant_id": tenant_id, "revenue": revenue}
            for tenant_id, revenue in sorted_tenants[:limit]
        ]
    
    def _calculate_conversion_rates(self, payments: List[Payment], invoices: List[Invoice]) -> Dict[str, float]:
        """Calculate conversion rates."""
        total_payments = len(payments)
        successful_payments = len([p for p in payments if p.status == PaymentStatus.COMPLETED])
        
        total_invoices = len(invoices)
        paid_invoices = len([i for i in invoices if i.status == InvoiceStatus.PAID])
        
        return {
            "payment_success_rate": (successful_payments / total_payments * 100) if total_payments > 0 else 0,
            "invoice_payment_rate": (paid_invoices / total_invoices * 100) if total_invoices > 0 else 0
        }
    
    def _calculate_success_rate(self, payments: List[Payment]) -> float:
        """Calculate payment success rate."""
        if not payments:
            return 0.0
        successful = len([p for p in payments if p.status == PaymentStatus.COMPLETED])
        return (successful / len(payments)) * 100
    
    def _calculate_average_payment_amount(self, payments: List[Payment]) -> Decimal:
        """Calculate average payment amount."""
        if not payments:
            return Decimal("0.00")
        total_amount = sum(p.amount for p in payments)
        return total_amount / len(payments)
    
    def _calculate_daily_payment_volume(self, payments: List[Payment], start_date: datetime, end_date: datetime) -> Dict[str, int]:
        """Calculate daily payment volume."""
        daily_volume = {}
        current_date = start_date
        
        while current_date <= end_date:
            date_key = current_date.strftime("%Y-%m-%d")
            daily_volume[date_key] = 0
            current_date += timedelta(days=1)
        
        for payment in payments:
            date_key = payment.created_at.strftime("%Y-%m-%d")
            if date_key in daily_volume:
                daily_volume[date_key] += 1
        
        return daily_volume
    
    def _analyze_failed_payments(self, payments: List[Payment]) -> Dict[str, int]:
        """Analyze failed payment reasons."""
        failed_reasons = {}
        for payment in payments:
            if payment.status == PaymentStatus.FAILED and payment.failure_reason:
                reason = payment.failure_reason
                failed_reasons[reason] = failed_reasons.get(reason, 0) + 1
        return failed_reasons
    
    def _calculate_revenue_trend(self, payments: List[Payment], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Calculate revenue trend over time."""
        daily_revenue = {}
        current_date = start_date
        
        while current_date <= end_date:
            date_key = current_date.strftime("%Y-%m-%d")
            daily_revenue[date_key] = Decimal("0.00")
            current_date += timedelta(days=1)
        
        for payment in payments:
            if payment.status == PaymentStatus.COMPLETED:
                date_key = payment.created_at.strftime("%Y-%m-%d")
                if date_key in daily_revenue:
                    daily_revenue[date_key] += payment.amount
        
        revenue_values = list(daily_revenue.values())
        trend_direction = self._calculate_trend_direction(revenue_values)
        
        return {
            "daily_revenue": daily_revenue,
            "trend_direction": trend_direction,
            "total_revenue": sum(revenue_values)
        }
    
    def _calculate_trend_direction(self, values: List[float]) -> str:
        """Calculate trend direction from a list of values."""
        if len(values) < 2:
            return "stable"
        
        # Simple linear trend calculation
        n = len(values)
        x_sum = sum(range(n))
        y_sum = sum(values)
        xy_sum = sum(i * values[i] for i in range(n))
        x_squared_sum = sum(i * i for i in range(n))
        
        slope = (n * xy_sum - x_sum * y_sum) / (n * x_squared_sum - x_sum * x_sum)
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"
