"""
Test cases for Stripe payment gateway integration.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from decimal import Decimal
from src.saas.billing.integrations.stripe_gateway import StripeGateway
from src.saas.billing.models.payment import Payment, PaymentStatus, PaymentMethod


class TestStripeGateway:
    """Test cases for StripeGateway."""
    
    @pytest.fixture
    def stripe_gateway(self):
        """Create StripeGateway instance for testing."""
        return StripeGateway(api_key="sk_test_123")
    
    @pytest.fixture
    def mock_payment(self):
        """Create mock payment for testing."""
        return Payment(
            id="pay_123",
            tenant_id="tenant_456",
            amount=Decimal("99.99"),
            currency="USD",
            status=PaymentStatus.PENDING,
            payment_method=PaymentMethod.CREDIT_CARD
        )
    
    @pytest.mark.asyncio
    async def test_create_payment_intent_success(self, stripe_gateway, mock_payment):
        """Test successful payment intent creation."""
        mock_intent = Mock()
        mock_intent.id = "pi_123"
        mock_intent.client_secret = "pi_123_secret"
        mock_intent.status = "requires_payment_method"
        
        with patch('stripe.PaymentIntent.create', return_value=mock_intent):
            result = await stripe_gateway.create_payment_intent(
                amount=Decimal("99.99"),
                currency="USD",
                tenant_id="tenant_456"
            )
            
            assert result["success"] is True
            assert result["payment_intent_id"] == "pi_123"
            assert result["client_secret"] == "pi_123_secret"
    
    @pytest.mark.asyncio
    async def test_create_payment_intent_failure(self, stripe_gateway):
        """Test failed payment intent creation."""
        with patch('stripe.PaymentIntent.create', side_effect=Exception("Stripe API error")):
            result = await stripe_gateway.create_payment_intent(
                amount=Decimal("99.99"),
                currency="USD",
                tenant_id="tenant_456"
            )
            
            assert result["success"] is False
            assert "error" in result
    
    @pytest.mark.asyncio
    async def test_confirm_payment_intent_success(self, stripe_gateway):
        """Test successful payment intent confirmation."""
        mock_intent = Mock()
        mock_intent.id = "pi_123"
        mock_intent.status = "succeeded"
        mock_intent.charges.data = [Mock(id="ch_123")]
        
        with patch('stripe.PaymentIntent.retrieve', return_value=mock_intent):
            with patch('stripe.PaymentIntent.confirm', return_value=mock_intent):
                result = await stripe_gateway.confirm_payment_intent(
                    payment_intent_id="pi_123",
                    payment_method_id="pm_123"
                )
                
                assert result["success"] is True
                assert result["status"] == "succeeded"
                assert result["transaction_id"] == "ch_123"
    
    @pytest.mark.asyncio
    async def test_confirm_payment_intent_failure(self, stripe_gateway):
        """Test failed payment intent confirmation."""
        with patch('stripe.PaymentIntent.confirm', side_effect=Exception("Payment failed")):
            result = await stripe_gateway.confirm_payment_intent(
                payment_intent_id="pi_123",
                payment_method_id="pm_123"
            )
            
            assert result["success"] is False
            assert "error" in result
    
    @pytest.mark.asyncio
    async def test_create_refund_success(self, stripe_gateway):
        """Test successful refund creation."""
        mock_refund = Mock()
        mock_refund.id = "re_123"
        mock_refund.status = "succeeded"
        mock_refund.amount = 5000  # $50.00 in cents
        
        with patch('stripe.Refund.create', return_value=mock_refund):
            result = await stripe_gateway.create_refund(
                charge_id="ch_123",
                amount=Decimal("50.00")
            )
            
            assert result["success"] is True
            assert result["refund_id"] == "re_123"
            assert result["status"] == "succeeded"
    
    @pytest.mark.asyncio
    async def test_create_refund_failure(self, stripe_gateway):
        """Test failed refund creation."""
        with patch('stripe.Refund.create', side_effect=Exception("Refund failed")):
            result = await stripe_gateway.create_refund(
                charge_id="ch_123",
                amount=Decimal("50.00")
            )
            
            assert result["success"] is False
            assert "error" in result
    
    @pytest.mark.asyncio
    async def test_get_payment_intent_success(self, stripe_gateway):
        """Test successful payment intent retrieval."""
        mock_intent = Mock()
        mock_intent.id = "pi_123"
        mock_intent.status = "succeeded"
        mock_intent.amount = 9999  # $99.99 in cents
        mock_intent.currency = "usd"
        
        with patch('stripe.PaymentIntent.retrieve', return_value=mock_intent):
            result = await stripe_gateway.get_payment_intent("pi_123")
            
            assert result["success"] is True
            assert result["payment_intent_id"] == "pi_123"
            assert result["status"] == "succeeded"
            assert result["amount"] == Decimal("99.99")
    
    @pytest.mark.asyncio
    async def test_get_payment_intent_not_found(self, stripe_gateway):
        """Test payment intent not found."""
        with patch('stripe.PaymentIntent.retrieve', side_effect=Exception("No such payment_intent")):
            result = await stripe_gateway.get_payment_intent("pi_nonexistent")
            
            assert result["success"] is False
            assert "error" in result
    
    @pytest.mark.asyncio
    async def test_create_customer_success(self, stripe_gateway):
        """Test successful customer creation."""
        mock_customer = Mock()
        mock_customer.id = "cus_123"
        mock_customer.email = "test@example.com"
        
        with patch('stripe.Customer.create', return_value=mock_customer):
            result = await stripe_gateway.create_customer(
                email="test@example.com",
                name="Test User",
                tenant_id="tenant_456"
            )
            
            assert result["success"] is True
            assert result["customer_id"] == "cus_123"
            assert result["email"] == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_create_customer_failure(self, stripe_gateway):
        """Test failed customer creation."""
        with patch('stripe.Customer.create', side_effect=Exception("Invalid email")):
            result = await stripe_gateway.create_customer(
                email="invalid-email",
                name="Test User",
                tenant_id="tenant_456"
            )
            
            assert result["success"] is False
            assert "error" in result
    
    def test_convert_amount_to_cents(self, stripe_gateway):
        """Test amount conversion to cents."""
        assert stripe_gateway._convert_amount_to_cents(Decimal("99.99")) == 9999
        assert stripe_gateway._convert_amount_to_cents(Decimal("0.01")) == 1
        assert stripe_gateway._convert_amount_to_cents(Decimal("100.00")) == 10000
    
    def test_convert_cents_to_amount(self, stripe_gateway):
        """Test cents conversion to amount."""
        assert stripe_gateway._convert_cents_to_amount(9999) == Decimal("99.99")
        assert stripe_gateway._convert_cents_to_amount(1) == Decimal("0.01")
        assert stripe_gateway._convert_cents_to_amount(10000) == Decimal("100.00")
    
    def test_validate_currency(self, stripe_gateway):
        """Test currency validation."""
        assert stripe_gateway._validate_currency("USD") is True
        assert stripe_gateway._validate_currency("EUR") is True
        assert stripe_gateway._validate_currency("GBP") is True
        
        with pytest.raises(ValueError, match="Unsupported currency"):
            stripe_gateway._validate_currency("INVALID")
    
    def test_validate_amount(self, stripe_gateway):
        """Test amount validation."""
        assert stripe_gateway._validate_amount(Decimal("0.50")) is True
        assert stripe_gateway._validate_amount(Decimal("999999.99")) is True
        
        with pytest.raises(ValueError, match="Amount must be at least"):
            stripe_gateway._validate_amount(Decimal("0.30"))
        
        with pytest.raises(ValueError, match="Amount must be at most"):
            stripe_gateway._validate_amount(Decimal("1000000.00"))
