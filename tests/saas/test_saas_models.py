"""
Tests for SaaS Models

This module contains tests for all SaaS data models including:
- Tenant model tests
- Subscription model tests
- Billing model tests
- Customer model tests
- Usage model tests
- Plan model tests
- Feature model tests
"""

import pytest
from datetime import datetime, timedelta, timezone
from src.saas.models.tenant import Tenant, TenantStatus, TenantType
from src.saas.models.subscription import Subscription, SubscriptionStatus, SubscriptionTier
from src.saas.models.billing import Billing, BillingStatus, PaymentMethod
from src.saas.models.customer import Customer, CustomerStatus, CustomerType
from src.saas.models.usage import Usage, UsageType, UsageMetric
from src.saas.models.plan import Plan, PlanType, PlanStatus
from src.saas.models.feature import Feature, FeatureType, FeatureAccess


class TestTenantModel:
    """Test cases for Tenant model."""
    
    def test_tenant_creation(self):
        """Test tenant creation with default values."""
        tenant = Tenant(
            name="Test Company",
            email="test@example.com",
            tenant_type=TenantType.SMALL_BUSINESS
        )
        
        assert tenant.name == "Test Company"
        assert tenant.email == "test@example.com"
        assert tenant.tenant_type == TenantType.SMALL_BUSINESS
        assert tenant.status == TenantStatus.PENDING
        assert tenant.tenant_id is not None
        assert tenant.tenant_slug is not None
    
    def test_tenant_active_status(self):
        """Test tenant active status check."""
        tenant = Tenant(
            name="Test Company",
            email="test@example.com",
            status=TenantStatus.ACTIVE
        )
        
        assert tenant.is_active() is True
        
        tenant.status = TenantStatus.SUSPENDED
        assert tenant.is_active() is False
    
    def test_tenant_trial_period(self):
        """Test tenant trial period functionality."""
        tenant = Tenant(
            name="Test Company",
            email="test@example.com",
            status=TenantStatus.TRIAL,
            trial_ends_at=datetime.now(timezone.utc) + timedelta(days=14)
        )
        
        assert tenant.is_trial() is True
        assert tenant.get_trial_days_remaining() > 0
        
        # Test expired trial
        tenant.trial_ends_at = datetime.now(timezone.utc) - timedelta(days=1)
        assert tenant.is_trial_expired() is True
    
    def test_tenant_usage_tracking(self):
        """Test tenant usage tracking."""
        tenant = Tenant(
            name="Test Company",
            email="test@example.com",
            limits={"api_calls": 10000, "storage": 1000}
        )
        
        # Test usage update
        tenant.update_usage("api_calls", 100)
        assert tenant.api_calls_this_month == 100
        
        # Test usage percentage
        percentage = tenant.get_usage_percentage("api_calls", 5000)
        assert percentage == 50.0
        
        # Test within limits
        assert tenant.is_within_limits("api_calls", 5000) is True
        assert tenant.is_within_limits("api_calls", 15000) is False
    
    def test_tenant_feature_management(self):
        """Test tenant feature management."""
        tenant = Tenant(
            name="Test Company",
            email="test@example.com",
            features=["basic_trading", "data_export"]
        )
        
        assert tenant.has_feature("basic_trading") is True
        assert tenant.has_feature("live_trading") is False
        
        tenant.add_feature("live_trading")
        assert tenant.has_feature("live_trading") is True
        
        tenant.remove_feature("basic_trading")
        assert tenant.has_feature("basic_trading") is False


class TestSubscriptionModel:
    """Test cases for Subscription model."""
    
    def test_subscription_creation(self):
        """Test subscription creation."""
        subscription = Subscription(
            tenant_id="tenant-123",
            plan_id="professional",
            tier=SubscriptionTier.PROFESSIONAL,
            monthly_price=199.0,
            annual_price=1990.0
        )
        
        assert subscription.tenant_id == "tenant-123"
        assert subscription.plan_id == "professional"
        assert subscription.tier == SubscriptionTier.PROFESSIONAL
        assert subscription.monthly_price == 199.0
        assert subscription.annual_price == 1990.0
    
    def test_subscription_status(self):
        """Test subscription status checks."""
        subscription = Subscription(
            tenant_id="tenant-123",
            plan_id="professional",
            status=SubscriptionStatus.ACTIVE
        )
        
        assert subscription.is_active() is True
        assert subscription.is_cancelled() is False
        
        subscription.status = SubscriptionStatus.CANCELLED
        assert subscription.is_active() is False
        assert subscription.is_cancelled() is True
    
    def test_subscription_trial(self):
        """Test subscription trial functionality."""
        subscription = Subscription(
            tenant_id="tenant-123",
            plan_id="professional",
            status=SubscriptionStatus.TRIALING,
            trial_start=datetime.now(timezone.utc),
            trial_end=datetime.now(timezone.utc) + timedelta(days=14)
        )
        
        assert subscription.is_trial() is True
        assert subscription.get_trial_days_remaining() > 0
        
        # Test expired trial
        subscription.trial_end = datetime.now(timezone.utc) - timedelta(days=1)
        assert subscription.is_trial_expired() is True
    
    def test_subscription_pricing(self):
        """Test subscription pricing calculations."""
        subscription = Subscription(
            tenant_id="tenant-123",
            plan_id="professional",
            monthly_price=199.0,
            annual_price=1990.0,
            billing_cycle="monthly"
        )
        
        assert subscription.get_effective_price() == 199.0
        
        subscription.billing_cycle = "annual"
        assert subscription.get_effective_price() == 1990.0
        
        # Test with discount
        subscription.discount_percentage = 10.0
        effective_price = subscription.get_effective_price()
        assert effective_price < 1990.0
    
    def test_subscription_usage_tracking(self):
        """Test subscription usage tracking."""
        subscription = Subscription(
            tenant_id="tenant-123",
            plan_id="professional",
            limits={"api_calls": 100000, "storage": 10000}
        )
        
        # Test usage update
        subscription.update_usage("api_calls", 1000)
        assert subscription.usage_this_period["api_calls"] == 1000
        
        # Test within limits
        assert subscription.is_within_limit("api_calls", 50000) is True
        assert subscription.is_within_limit("api_calls", 150000) is False


class TestBillingModel:
    """Test cases for Billing model."""
    
    def test_billing_creation(self):
        """Test billing creation."""
        billing = Billing(
            tenant_id="tenant-123",
            subscription_id="sub-123",
            subtotal=199.0,
            tax_amount=19.9,
            total_amount=218.9
        )
        
        assert billing.tenant_id == "tenant-123"
        assert billing.subscription_id == "sub-123"
        assert billing.subtotal == 199.0
        assert billing.total_amount == 218.9
        assert billing.invoice_number is not None
    
    def test_billing_status(self):
        """Test billing status checks."""
        billing = Billing(
            tenant_id="tenant-123",
            subscription_id="sub-123",
            status=BillingStatus.PENDING
        )
        
        assert billing.is_pending() is True
        assert billing.is_paid() is False
        
        billing.status = BillingStatus.PAID
        assert billing.is_pending() is False
        assert billing.is_paid() is True
    
    def test_billing_payment_processing(self):
        """Test billing payment processing."""
        billing = Billing(
            tenant_id="tenant-123",
            subscription_id="sub-123",
            total_amount=199.0
        )
        
        # Process payment
        billing.process_payment(
            amount=199.0,
            payment_method=PaymentMethod.CREDIT_CARD,
            processor_transaction_id="txn-123"
        )
        
        assert billing.paid_amount == 199.0
        assert billing.status == BillingStatus.PAID
        assert billing.payment_method == PaymentMethod.CREDIT_CARD
        assert billing.paid_at is not None
    
    def test_billing_line_items(self):
        """Test billing line items management."""
        billing = Billing(
            tenant_id="tenant-123",
            subscription_id="sub-123"
        )
        
        # Add line item
        billing.add_line_item(
            description="Professional Plan",
            quantity=1,
            unit_price=199.0,
            tax_rate=10.0
        )
        
        assert len(billing.line_items) == 1
        assert billing.subtotal == 199.0
        assert abs(billing.tax_amount - 19.9) < 0.01
        assert abs(billing.total_amount - 218.9) < 0.01


class TestCustomerModel:
    """Test cases for Customer model."""
    
    def test_customer_creation(self):
        """Test customer creation."""
        customer = Customer(
            tenant_id="tenant-123",
            user_id="user-123",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            customer_type=CustomerType.TRADER
        )
        
        assert customer.tenant_id == "tenant-123"
        assert customer.user_id == "user-123"
        assert customer.get_full_name() == "John Doe"
        assert customer.customer_type == CustomerType.TRADER
        assert customer.status == CustomerStatus.PENDING
    
    def test_customer_status(self):
        """Test customer status checks."""
        customer = Customer(
            tenant_id="tenant-123",
            user_id="user-123",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            status=CustomerStatus.ACTIVE,
            locked_until=None
        )
        
        assert customer.is_active() is True
        assert customer.is_locked() is False
        
        customer.status = CustomerStatus.LOCKED
        assert customer.is_active() is False
        assert customer.is_locked() is True
    
    def test_customer_login_tracking(self):
        """Test customer login tracking."""
        customer = Customer(
            tenant_id="tenant-123",
            user_id="user-123",
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )
        
        # Record login
        customer.record_login("192.168.1.1")
        assert customer.last_login is not None
        assert customer.login_count == 1
        assert customer.failed_login_attempts == 0
        
        # Record failed login
        customer.record_failed_login()
        assert customer.failed_login_attempts == 1
    
    def test_customer_preferences(self):
        """Test customer preferences management."""
        customer = Customer(
            tenant_id="tenant-123",
            user_id="user-123",
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )
        
        # Update preference
        customer.update_preference("theme", "dark")
        assert customer.get_preference("theme") == "dark"
        assert customer.get_preference("language", "en") == "en"


class TestUsageModel:
    """Test cases for Usage model."""
    
    def test_usage_creation(self):
        """Test usage creation."""
        usage = Usage(
            tenant_id="tenant-123",
            customer_id="customer-123",
            usage_type=UsageType.API_CALL,
            amount=100.0,
            cost_per_unit=0.01
        )
        
        assert usage.tenant_id == "tenant-123"
        assert usage.customer_id == "customer-123"
        assert usage.usage_type == UsageType.API_CALL
        assert usage.amount == 100.0
        assert usage.total_cost == 1.0  # 100 * 0.01
    
    def test_usage_billable_check(self):
        """Test usage billable check."""
        usage = Usage(
            tenant_id="tenant-123",
            usage_type=UsageType.API_CALL,
            amount=100.0,
            cost_per_unit=0.01,
            billable=True
        )
        
        assert usage.is_billable() is True
        
        usage.billable = False
        assert usage.is_billable() is False
    
    def test_usage_metadata(self):
        """Test usage metadata management."""
        usage = Usage(
            tenant_id="tenant-123",
            usage_type=UsageType.API_CALL,
            amount=100.0
        )
        
        # Add metadata
        usage.add_metadata("endpoint", "/api/v1/trades")
        usage.add_metadata("response_time", 150)
        
        assert usage.get_metadata("endpoint") == "/api/v1/trades"
        assert usage.get_metadata("response_time") == 150
        assert usage.get_metadata("nonexistent", "default") == "default"


class TestPlanModel:
    """Test cases for Plan model."""
    
    def test_plan_creation(self):
        """Test plan creation."""
        plan = Plan(
            name="professional",
            display_name="Professional Plan",
            description="Advanced features for serious traders",
            plan_type=PlanType.PROFESSIONAL,
            monthly_price=199.0,
            annual_price=1990.0
        )
        
        assert plan.name == "professional"
        assert plan.display_name == "Professional Plan"
        assert plan.plan_type == PlanType.PROFESSIONAL
        assert plan.monthly_price == 199.0
        assert plan.annual_price == 1990.0
    
    def test_plan_status(self):
        """Test plan status checks."""
        plan = Plan(
            name="professional",
            plan_type=PlanType.PROFESSIONAL,
            status=PlanStatus.ACTIVE
        )
        
        assert plan.is_active() is True
        assert plan.is_publicly_available() is True
        
        plan.status = PlanStatus.INACTIVE
        assert plan.is_active() is False
    
    def test_plan_pricing(self):
        """Test plan pricing calculations."""
        plan = Plan(
            name="professional",
            plan_type=PlanType.PROFESSIONAL,
            monthly_price=199.0,
            annual_price=1990.0
        )
        
        assert plan.get_effective_price("monthly") == 199.0
        assert plan.get_effective_price("annual") == 1990.0
        
        # Test annual savings
        savings = plan.get_annual_savings()
        assert savings > 0  # Should be positive savings
    
    def test_plan_feature_management(self):
        """Test plan feature management."""
        plan = Plan(
            name="professional",
            plan_type=PlanType.PROFESSIONAL,
            features=["basic_trading", "live_trading"]
        )
        
        assert plan.has_feature("basic_trading") is True
        assert plan.has_feature("ml_models") is False
        
        plan.add_feature("ml_models")
        assert plan.has_feature("ml_models") is True
        
        plan.remove_feature("basic_trading")
        assert plan.has_feature("basic_trading") is False


class TestFeatureModel:
    """Test cases for Feature model."""
    
    def test_feature_creation(self):
        """Test feature creation."""
        feature = Feature(
            name="live_trading",
            display_name="Live Trading",
            description="Execute live trades on real markets",
            feature_type=FeatureType.PREMIUM,
            access_level=FeatureAccess.PAID,
            price=50.0
        )
        
        assert feature.name == "live_trading"
        assert feature.display_name == "Live Trading"
        assert feature.feature_type == FeatureType.PREMIUM
        assert feature.access_level == FeatureAccess.PAID
        assert feature.price == 50.0
    
    def test_feature_access_levels(self):
        """Test feature access level checks."""
        # Free feature
        free_feature = Feature(
            name="basic_trading",
            access_level=FeatureAccess.FREE
        )
        assert free_feature.is_free() is True
        assert free_feature.is_paid() is False
        
        # Paid feature
        paid_feature = Feature(
            name="live_trading",
            access_level=FeatureAccess.PAID
        )
        assert paid_feature.is_free() is False
        assert paid_feature.is_paid() is True
    
    def test_feature_availability(self):
        """Test feature availability checks."""
        feature = Feature(
            name="live_trading",
            is_active=True,
            is_public=True,
            is_beta=False
        )
        
        assert feature.is_available() is True
        assert feature.is_publicly_available() is True
        assert feature.is_beta_feature() is False
        
        feature.is_active = False
        assert feature.is_available() is False
    
    def test_feature_usage_tracking(self):
        """Test feature usage tracking."""
        feature = Feature(
            name="live_trading",
            usage_count=0
        )
        
        # Record usage
        feature.record_usage()
        assert feature.usage_count == 1
        assert feature.last_used is not None
        
        # Record more usage
        feature.record_usage()
        assert feature.usage_count == 2


if __name__ == "__main__":
    pytest.main([__file__])
