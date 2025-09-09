"""
Test cases for Stripe webhook handler.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
import json
from decimal import Decimal
from datetime import datetime, timezone

from src.saas.billing.webhooks.stripe_webhook import StripeWebhookHandler
from src.saas.billing.models.payment import Payment, PaymentStatus
from src.saas.billing.models.invoice import Invoice, InvoiceStatus


class TestStripeWebhookHandler:
    """Test cases for StripeWebhookHandler."""
    
    @pytest.fixture
    def webhook_handler(self):
        """Create StripeWebhookHandler instance for testing."""
        payment_service = Mock()
        return StripeWebhookHandler("whsec_test_secret", payment_service)
    
    @pytest.fixture
    def mock_payment(self):
        """Create mock payment for testing."""
        return Payment(
            id="pay_123",
            tenant_id="tenant_456",
            amount=Decimal("99.99"),
            currency="USD",
            status=PaymentStatus.PENDING,
            payment_method=None
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
    
    def test_webhook_handler_initialization(self, webhook_handler):
        """Test webhook handler initialization."""
        assert webhook_handler.webhook_secret == "whsec_test_secret"
        assert webhook_handler.payment_service is not None
        assert "payment_intent.succeeded" in webhook_handler.supported_events
    
    def test_verify_signature_valid(self, webhook_handler):
        """Test valid signature verification."""
        payload = '{"test": "data"}'
        timestamp = int(datetime.now().timestamp())
        
        # Create valid signature
        import hmac
        import hashlib
        expected_signature = hmac.new(
            webhook_handler.webhook_secret.encode(),
            f"{timestamp}.{payload}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        result = webhook_handler._verify_signature(payload, expected_signature, timestamp)
        assert result is True
    
    def test_verify_signature_invalid(self, webhook_handler):
        """Test invalid signature verification."""
        payload = '{"test": "data"}'
        timestamp = int(datetime.now().timestamp())
        invalid_signature = "invalid_signature"
        
        result = webhook_handler._verify_signature(payload, invalid_signature, timestamp)
        assert result is False
    
    def test_verify_signature_old_timestamp(self, webhook_handler):
        """Test signature verification with old timestamp."""
        payload = '{"test": "data"}'
        timestamp = int(datetime.now().timestamp()) - 400  # 400 seconds ago
        valid_signature = "valid_signature"
        
        result = webhook_handler._verify_signature(payload, valid_signature, timestamp)
        assert result is False
    
    @pytest.mark.asyncio
    async def test_handle_webhook_success(self, webhook_handler, mock_payment):
        """Test successful webhook handling."""
        payload = json.dumps({
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_123",
                    "metadata": {"payment_id": "pay_123"}
                }
            }
        })
        timestamp = int(datetime.now().timestamp())
        
        with patch.object(webhook_handler, '_verify_signature', return_value=True):
            with patch.object(webhook_handler, '_process_event', return_value={"success": True}):
                result = await webhook_handler.handle_webhook(payload, "valid_signature", timestamp)
                
                assert result["success"] is True
    
    @pytest.mark.asyncio
    async def test_handle_webhook_invalid_signature(self, webhook_handler):
        """Test webhook handling with invalid signature."""
        payload = '{"test": "data"}'
        timestamp = int(datetime.now().timestamp())
        
        with patch.object(webhook_handler, '_verify_signature', return_value=False):
            result = await webhook_handler.handle_webhook(payload, "invalid_signature", timestamp)
            
            assert result["success"] is False
            assert "Invalid signature" in result["error"]
    
    @pytest.mark.asyncio
    async def test_handle_webhook_invalid_json(self, webhook_handler):
        """Test webhook handling with invalid JSON."""
        payload = "invalid json"
        timestamp = int(datetime.now().timestamp())
        
        with patch.object(webhook_handler, '_verify_signature', return_value=True):
            result = await webhook_handler.handle_webhook(payload, "valid_signature", timestamp)
            
            assert result["success"] is False
            assert "Invalid JSON payload" in result["error"]
    
    @pytest.mark.asyncio
    async def test_handle_webhook_unsupported_event(self, webhook_handler):
        """Test webhook handling with unsupported event."""
        payload = json.dumps({
            "type": "unsupported.event",
            "data": {"object": {}}
        })
        timestamp = int(datetime.now().timestamp())
        
        with patch.object(webhook_handler, '_verify_signature', return_value=True):
            result = await webhook_handler.handle_webhook(payload, "valid_signature", timestamp)
            
            assert result["success"] is True
            assert "not supported" in result["message"]
    
    @pytest.mark.asyncio
    async def test_handle_payment_intent_succeeded(self, webhook_handler, mock_payment):
        """Test handling successful payment intent."""
        payment_intent = {
            "id": "pi_123",
            "metadata": {"payment_id": "pay_123"}
        }
        
        with patch.object(webhook_handler.payment_service, 'get_payment_by_id', return_value=mock_payment):
            with patch.object(webhook_handler.payment_service, '_update_payment_status', return_value=mock_payment):
                result = await webhook_handler._handle_payment_intent_succeeded(payment_intent)
                
                assert result["success"] is True
                assert result["payment_id"] == "pay_123"
    
    @pytest.mark.asyncio
    async def test_handle_payment_intent_succeeded_no_payment_id(self, webhook_handler):
        """Test handling successful payment intent without payment ID."""
        payment_intent = {
            "id": "pi_123",
            "metadata": {}
        }
        
        result = await webhook_handler._handle_payment_intent_succeeded(payment_intent)
        
        assert result["success"] is False
        assert "No payment ID in metadata" in result["error"]
    
    @pytest.mark.asyncio
    async def test_handle_payment_intent_succeeded_payment_not_found(self, webhook_handler):
        """Test handling successful payment intent with payment not found."""
        payment_intent = {
            "id": "pi_123",
            "metadata": {"payment_id": "pay_123"}
        }
        
        with patch.object(webhook_handler.payment_service, 'get_payment_by_id', return_value=None):
            result = await webhook_handler._handle_payment_intent_succeeded(payment_intent)
            
            assert result["success"] is False
            assert "Payment not found" in result["error"]
    
    @pytest.mark.asyncio
    async def test_handle_payment_intent_failed(self, webhook_handler, mock_payment):
        """Test handling failed payment intent."""
        payment_intent = {
            "id": "pi_123",
            "metadata": {"payment_id": "pay_123"},
            "last_payment_error": {"message": "Card declined"}
        }
        
        with patch.object(webhook_handler.payment_service, 'get_payment_by_id', return_value=mock_payment):
            with patch.object(webhook_handler.payment_service, '_update_payment_status', return_value=mock_payment):
                result = await webhook_handler._handle_payment_intent_failed(payment_intent)
                
                assert result["success"] is True
                assert result["payment_id"] == "pay_123"
    
    @pytest.mark.asyncio
    async def test_handle_payment_intent_canceled(self, webhook_handler, mock_payment):
        """Test handling canceled payment intent."""
        payment_intent = {
            "id": "pi_123",
            "metadata": {"payment_id": "pay_123"}
        }
        
        with patch.object(webhook_handler.payment_service, 'get_payment_by_id', return_value=mock_payment):
            with patch.object(webhook_handler.payment_service, '_update_payment_status', return_value=mock_payment):
                result = await webhook_handler._handle_payment_intent_canceled(payment_intent)
                
                assert result["success"] is True
                assert result["payment_id"] == "pay_123"
    
    @pytest.mark.asyncio
    async def test_handle_invoice_payment_succeeded(self, webhook_handler, mock_invoice):
        """Test handling successful invoice payment."""
        invoice = {
            "id": "in_123",
            "metadata": {"invoice_id": "inv_123"},
            "payment_intent": "pi_123"
        }
        
        with patch.object(webhook_handler.payment_service, 'get_invoice_by_id', return_value=mock_invoice):
            with patch.object(webhook_handler.payment_service, '_update_invoice_status', return_value=mock_invoice):
                result = await webhook_handler._handle_invoice_payment_succeeded(invoice)
                
                assert result["success"] is True
                assert result["invoice_id"] == "inv_123"
    
    @pytest.mark.asyncio
    async def test_handle_invoice_payment_failed(self, webhook_handler, mock_invoice):
        """Test handling failed invoice payment."""
        invoice = {
            "id": "in_123",
            "metadata": {"invoice_id": "inv_123"}
        }
        
        with patch.object(webhook_handler.payment_service, 'get_invoice_by_id', return_value=mock_invoice):
            with patch.object(webhook_handler.payment_service, '_update_invoice_status', return_value=mock_invoice):
                result = await webhook_handler._handle_invoice_payment_failed(invoice)
                
                assert result["success"] is True
                assert result["invoice_id"] == "inv_123"
    
    @pytest.mark.asyncio
    async def test_handle_subscription_created(self, webhook_handler):
        """Test handling subscription creation."""
        subscription = {"id": "sub_123"}
        
        result = await webhook_handler._handle_subscription_created(subscription)
        
        assert result["success"] is True
        assert "Subscription created" in result["message"]
    
    @pytest.mark.asyncio
    async def test_handle_subscription_updated(self, webhook_handler):
        """Test handling subscription update."""
        subscription = {"id": "sub_123"}
        
        result = await webhook_handler._handle_subscription_updated(subscription)
        
        assert result["success"] is True
        assert "Subscription updated" in result["message"]
    
    @pytest.mark.asyncio
    async def test_handle_subscription_deleted(self, webhook_handler):
        """Test handling subscription deletion."""
        subscription = {"id": "sub_123"}
        
        result = await webhook_handler._handle_subscription_deleted(subscription)
        
        assert result["success"] is True
        assert "Subscription deleted" in result["message"]
    
    @pytest.mark.asyncio
    async def test_handle_dispute_created(self, webhook_handler):
        """Test handling dispute creation."""
        charge = {"id": "ch_123"}
        
        result = await webhook_handler._handle_dispute_created(charge)
        
        assert result["success"] is True
        assert "Dispute created" in result["message"]
    
    @pytest.mark.asyncio
    async def test_handle_charge_refunded(self, webhook_handler, mock_payment):
        """Test handling charge refund."""
        charge = {
            "id": "ch_123",
            "metadata": {"payment_id": "pay_123"},
            "refunds": {
                "data": [{"id": "re_123"}]
            }
        }
        
        with patch.object(webhook_handler.payment_service, 'get_payment_by_id', return_value=mock_payment):
            with patch.object(webhook_handler.payment_service, '_update_payment_status', return_value=mock_payment):
                result = await webhook_handler._handle_charge_refunded(charge)
                
                assert result["success"] is True
                assert result["payment_id"] == "pay_123"
    
    def test_supported_events(self, webhook_handler):
        """Test supported events list."""
        expected_events = {
            "payment_intent.succeeded",
            "payment_intent.payment_failed",
            "payment_intent.canceled",
            "invoice.payment_succeeded",
            "invoice.payment_failed",
            "customer.subscription.created",
            "customer.subscription.updated",
            "customer.subscription.deleted",
            "charge.dispute.created",
            "charge.refunded"
        }
        
        assert webhook_handler.supported_events == expected_events
