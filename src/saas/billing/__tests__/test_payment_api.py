"""
Test cases for payment API endpoints.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from decimal import Decimal
from aiohttp import web
from aiohttp.test_utils import make_mocked_request
from src.saas.billing.api.payment_api import PaymentAPI
from src.saas.billing.models.payment import Payment, PaymentStatus, PaymentMethod
from src.saas.billing.models.invoice import Invoice, InvoiceStatus


class TestPaymentAPI:
    """Test cases for PaymentAPI."""
    
    @pytest.fixture
    def payment_api(self):
        """Create PaymentAPI instance for testing."""
        return PaymentAPI()
    
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
    
    @pytest.fixture
    def mock_invoice(self):
        """Create mock invoice for testing."""
        return Invoice(
            id="inv_123",
            tenant_id="tenant_456",
            amount=Decimal("199.99"),
            currency="USD",
            status=InvoiceStatus.DRAFT,
            due_date=None
        )
    
    @pytest.mark.asyncio
    async def test_create_payment_success(self, payment_api, mock_payment):
        """Test successful payment creation via API."""
        request_data = {
            "tenant_id": "tenant_456",
            "amount": "99.99",
            "currency": "USD",
            "payment_method": "credit_card"
        }
        
        with patch.object(payment_api.payment_service, 'create_payment', return_value=mock_payment):
            request = make_mocked_request('POST', '/payments', json=request_data)
            response = await payment_api.create_payment(request)
            
            assert response.status == 201
            data = await response.json()
            assert data["id"] == "pay_123"
            assert data["tenant_id"] == "tenant_456"
            assert data["amount"] == "99.99"
    
    @pytest.mark.asyncio
    async def test_create_payment_validation_error(self, payment_api):
        """Test payment creation with validation error."""
        request_data = {
            "tenant_id": "tenant_456",
            "amount": "-10.00",  # Invalid negative amount
            "currency": "USD",
            "payment_method": "credit_card"
        }
        
        with patch.object(payment_api.payment_service, 'create_payment', 
                         side_effect=ValueError("Amount must be positive")):
            request = make_mocked_request('POST', '/payments', json=request_data)
            response = await payment_api.create_payment(request)
            
            assert response.status == 400
            data = await response.json()
            assert "error" in data
    
    @pytest.mark.asyncio
    async def test_get_payment_success(self, payment_api, mock_payment):
        """Test successful payment retrieval via API."""
        with patch.object(payment_api.payment_service, 'get_payment_by_id', return_value=mock_payment):
            request = make_mocked_request('GET', '/payments/pay_123')
            response = await payment_api.get_payment(request)
            
            assert response.status == 200
            data = await response.json()
            assert data["id"] == "pay_123"
            assert data["tenant_id"] == "tenant_456"
    
    @pytest.mark.asyncio
    async def test_get_payment_not_found(self, payment_api):
        """Test payment not found via API."""
        with patch.object(payment_api.payment_service, 'get_payment_by_id', return_value=None):
            request = make_mocked_request('GET', '/payments/pay_nonexistent')
            response = await payment_api.get_payment(request)
            
            assert response.status == 404
            data = await response.json()
            assert "error" in data
    
    @pytest.mark.asyncio
    async def test_process_payment_success(self, payment_api, mock_payment):
        """Test successful payment processing via API."""
        mock_payment.status = PaymentStatus.COMPLETED
        
        with patch.object(payment_api.payment_service, 'get_payment_by_id', return_value=mock_payment):
            with patch.object(payment_api.payment_service, 'process_payment', return_value=mock_payment):
                request = make_mocked_request('POST', '/payments/pay_123/process')
                response = await payment_api.process_payment(request)
                
                assert response.status == 200
                data = await response.json()
                assert data["status"] == "completed"
    
    @pytest.mark.asyncio
    async def test_refund_payment_success(self, payment_api, mock_payment):
        """Test successful payment refund via API."""
        mock_payment.status = PaymentStatus.REFUNDED
        mock_payment.refund_id = "ref_123"
        
        request_data = {
            "amount": "50.00",
            "reason": "Customer request"
        }
        
        with patch.object(payment_api.payment_service, 'get_payment_by_id', return_value=mock_payment):
            with patch.object(payment_api.payment_service, 'refund_payment', return_value=mock_payment):
                request = make_mocked_request('POST', '/payments/pay_123/refund', json=request_data)
                response = await payment_api.refund_payment(request)
                
                assert response.status == 200
                data = await response.json()
                assert data["status"] == "refunded"
                assert data["refund_id"] == "ref_123"
    
    @pytest.mark.asyncio
    async def test_create_invoice_success(self, payment_api, mock_invoice):
        """Test successful invoice creation via API."""
        request_data = {
            "tenant_id": "tenant_456",
            "amount": "199.99",
            "currency": "USD",
            "due_date": "2024-12-31T23:59:59Z"
        }
        
        with patch.object(payment_api.payment_service, 'create_invoice', return_value=mock_invoice):
            request = make_mocked_request('POST', '/invoices', json=request_data)
            response = await payment_api.create_invoice(request)
            
            assert response.status == 201
            data = await response.json()
            assert data["id"] == "inv_123"
            assert data["tenant_id"] == "tenant_456"
            assert data["amount"] == "199.99"
    
    @pytest.mark.asyncio
    async def test_send_invoice_success(self, payment_api, mock_invoice):
        """Test successful invoice sending via API."""
        mock_invoice.status = InvoiceStatus.SENT
        
        with patch.object(payment_api.payment_service, 'get_invoice_by_id', return_value=mock_invoice):
            with patch.object(payment_api.payment_service, 'send_invoice', return_value=mock_invoice):
                request = make_mocked_request('POST', '/invoices/inv_123/send')
                response = await payment_api.send_invoice(request)
                
                assert response.status == 200
                data = await response.json()
                assert data["status"] == "sent"
    
    @pytest.mark.asyncio
    async def test_get_invoice_success(self, payment_api, mock_invoice):
        """Test successful invoice retrieval via API."""
        with patch.object(payment_api.payment_service, 'get_invoice_by_id', return_value=mock_invoice):
            request = make_mocked_request('GET', '/invoices/inv_123')
            response = await payment_api.get_invoice(request)
            
            assert response.status == 200
            data = await response.json()
            assert data["id"] == "inv_123"
            assert data["tenant_id"] == "tenant_456"
    
    @pytest.mark.asyncio
    async def test_get_payments_by_tenant_success(self, payment_api):
        """Test successful payments retrieval by tenant via API."""
        payments = [mock_payment, mock_payment]
        
        with patch.object(payment_api.payment_service, 'get_payments_by_tenant', return_value=payments):
            request = make_mocked_request('GET', '/tenants/tenant_456/payments')
            response = await payment_api.get_payments_by_tenant(request)
            
            assert response.status == 200
            data = await response.json()
            assert len(data["payments"]) == 2
            assert all(p["tenant_id"] == "tenant_456" for p in data["payments"])
    
    @pytest.mark.asyncio
    async def test_webhook_stripe_success(self, payment_api):
        """Test successful Stripe webhook processing."""
        webhook_data = {
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_123",
                    "status": "succeeded",
                    "amount": 9999
                }
            }
        }
        
        with patch.object(payment_api.payment_service, 'handle_stripe_webhook', return_value={"success": True}):
            request = make_mocked_request('POST', '/webhooks/stripe', json=webhook_data)
            response = await payment_api.stripe_webhook(request)
            
            assert response.status == 200
            data = await response.json()
            assert data["success"] is True
    
    @pytest.mark.asyncio
    async def test_webhook_stripe_invalid_signature(self, payment_api):
        """Test Stripe webhook with invalid signature."""
        with patch.object(payment_api.payment_service, 'handle_stripe_webhook', 
                         side_effect=ValueError("Invalid signature")):
            request = make_mocked_request('POST', '/webhooks/stripe', json={})
            response = await payment_api.stripe_webhook(request)
            
            assert response.status == 400
            data = await response.json()
            assert "error" in data
    
    def test_validate_tenant_id(self, payment_api):
        """Test tenant ID validation."""
        assert payment_api._validate_tenant_id("tenant_123") is True
        assert payment_api._validate_tenant_id("tenant_456") is True
        
        with pytest.raises(ValueError, match="Invalid tenant ID"):
            payment_api._validate_tenant_id("")
        
        with pytest.raises(ValueError, match="Invalid tenant ID"):
            payment_api._validate_tenant_id(None)
    
    def test_validate_amount(self, payment_api):
        """Test amount validation."""
        assert payment_api._validate_amount("99.99") == Decimal("99.99")
        assert payment_api._validate_amount("0.01") == Decimal("0.01")
        
        with pytest.raises(ValueError, match="Invalid amount"):
            payment_api._validate_amount("invalid")
        
        with pytest.raises(ValueError, match="Amount must be positive"):
            payment_api._validate_amount("-10.00")
    
    def test_validate_currency(self, payment_api):
        """Test currency validation."""
        assert payment_api._validate_currency("USD") is True
        assert payment_api._validate_currency("EUR") is True
        
        with pytest.raises(ValueError, match="Invalid currency"):
            payment_api._validate_currency("INVALID")
    
    def test_validate_payment_method(self, payment_api):
        """Test payment method validation."""
        assert payment_api._validate_payment_method("credit_card") is True
        assert payment_api._validate_payment_method("bank_transfer") is True
        
        with pytest.raises(ValueError, match="Invalid payment method"):
            payment_api._validate_payment_method("invalid_method")
