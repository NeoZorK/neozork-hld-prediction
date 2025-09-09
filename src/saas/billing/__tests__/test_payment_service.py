"""
Test cases for payment service.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from decimal import Decimal
from datetime import datetime, timezone
from src.saas.billing.services.payment_service import PaymentService
from src.saas.billing.models.payment import Payment, PaymentStatus, PaymentMethod
from src.saas.billing.models.invoice import Invoice, InvoiceStatus


class TestPaymentService:
    """Test cases for PaymentService."""
    
    @pytest.fixture
    def payment_service(self):
        """Create PaymentService instance for testing."""
        return PaymentService()
    
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
            due_date=datetime.now(timezone.utc)
        )
    
    @pytest.mark.asyncio
    async def test_create_payment(self, payment_service, mock_payment):
        """Test payment creation."""
        with patch.object(payment_service, '_generate_payment_id', return_value="pay_123"):
            with patch.object(payment_service, '_save_payment', return_value=mock_payment):
                result = await payment_service.create_payment(
                    tenant_id="tenant_456",
                    amount=Decimal("99.99"),
                    currency="USD",
                    payment_method=PaymentMethod.CREDIT_CARD
                )
                
                assert result.id == "pay_123"
                assert result.tenant_id == "tenant_456"
                assert result.amount == Decimal("99.99")
                assert result.status == PaymentStatus.PENDING
    
    @pytest.mark.asyncio
    async def test_process_payment_success(self, payment_service, mock_payment):
        """Test successful payment processing."""
        mock_payment.status = PaymentStatus.PROCESSING
        
        with patch.object(payment_service, '_call_payment_gateway', return_value={
            "success": True,
            "transaction_id": "txn_123",
            "gateway_response": {"status": "succeeded"}
        }):
            with patch.object(payment_service, '_update_payment_status', return_value=mock_payment):
                result = await payment_service.process_payment(mock_payment)
                
                assert result.status == PaymentStatus.COMPLETED
                assert result.gateway_transaction_id == "txn_123"
    
    @pytest.mark.asyncio
    async def test_process_payment_failure(self, payment_service, mock_payment):
        """Test failed payment processing."""
        mock_payment.status = PaymentStatus.PROCESSING
        
        with patch.object(payment_service, '_call_payment_gateway', return_value={
            "success": False,
            "error": "Insufficient funds",
            "gateway_response": {"status": "failed"}
        }):
            with patch.object(payment_service, '_update_payment_status', return_value=mock_payment):
                result = await payment_service.process_payment(mock_payment)
                
                assert result.status == PaymentStatus.FAILED
                assert result.failure_reason == "Insufficient funds"
    
    @pytest.mark.asyncio
    async def test_refund_payment(self, payment_service, mock_payment):
        """Test payment refund."""
        mock_payment.status = PaymentStatus.COMPLETED
        mock_payment.gateway_transaction_id = "txn_123"
        
        with patch.object(payment_service, '_call_payment_gateway', return_value={
            "success": True,
            "refund_id": "ref_123",
            "gateway_response": {"status": "succeeded"}
        }):
            with patch.object(payment_service, '_update_payment_status', return_value=mock_payment):
                result = await payment_service.refund_payment(
                    payment_id="pay_123",
                    amount=Decimal("50.00"),
                    reason="Customer request"
                )
                
                assert result.status == PaymentStatus.REFUNDED
                assert result.refund_id == "ref_123"
    
    @pytest.mark.asyncio
    async def test_get_payment_by_id(self, payment_service, mock_payment):
        """Test getting payment by ID."""
        with patch.object(payment_service, '_get_payment_from_db', return_value=mock_payment):
            result = await payment_service.get_payment_by_id("pay_123")
            
            assert result.id == "pay_123"
            assert result.tenant_id == "tenant_456"
    
    @pytest.mark.asyncio
    async def test_get_payments_by_tenant(self, payment_service):
        """Test getting payments by tenant ID."""
        payments = [mock_payment, mock_payment]
        
        with patch.object(payment_service, '_get_payments_from_db', return_value=payments):
            result = await payment_service.get_payments_by_tenant("tenant_456")
            
            assert len(result) == 2
            assert all(p.tenant_id == "tenant_456" for p in result)
    
    @pytest.mark.asyncio
    async def test_create_invoice(self, payment_service, mock_invoice):
        """Test invoice creation."""
        with patch.object(payment_service, '_generate_invoice_id', return_value="inv_123"):
            with patch.object(payment_service, '_save_invoice', return_value=mock_invoice):
                result = await payment_service.create_invoice(
                    tenant_id="tenant_456",
                    amount=Decimal("199.99"),
                    currency="USD",
                    due_date=datetime.now(timezone.utc)
                )
                
                assert result.id == "inv_123"
                assert result.tenant_id == "tenant_456"
                assert result.amount == Decimal("199.99")
                assert result.status == InvoiceStatus.DRAFT
    
    @pytest.mark.asyncio
    async def test_send_invoice(self, payment_service, mock_invoice):
        """Test sending invoice."""
        mock_invoice.status = InvoiceStatus.DRAFT
        
        with patch.object(payment_service, '_send_invoice_email', return_value=True):
            with patch.object(payment_service, '_update_invoice_status', return_value=mock_invoice):
                result = await payment_service.send_invoice("inv_123")
                
                assert result.status == InvoiceStatus.SENT
    
    @pytest.mark.asyncio
    async def test_mark_invoice_paid(self, payment_service, mock_invoice):
        """Test marking invoice as paid."""
        mock_invoice.status = InvoiceStatus.SENT
        
        with patch.object(payment_service, '_update_invoice_status', return_value=mock_invoice):
            result = await payment_service.mark_invoice_paid("inv_123", "pay_123")
            
            assert result.status == InvoiceStatus.PAID
            assert result.payment_id == "pay_123"
    
    def test_validate_payment_amount(self, payment_service):
        """Test payment amount validation."""
        # Valid amounts
        assert payment_service._validate_payment_amount(Decimal("10.00")) is True
        assert payment_service._validate_payment_amount(Decimal("0.01")) is True
        
        # Invalid amounts
        with pytest.raises(ValueError, match="Amount must be positive"):
            payment_service._validate_payment_amount(Decimal("-10.00"))
        
        with pytest.raises(ValueError, match="Amount must be positive"):
            payment_service._validate_payment_amount(Decimal("0.00"))
    
    def test_calculate_tax(self, payment_service):
        """Test tax calculation."""
        # Test with tax rate
        tax_amount = payment_service._calculate_tax(Decimal("100.00"), Decimal("0.08"))
        assert tax_amount == Decimal("8.00")
        
        # Test without tax rate
        tax_amount = payment_service._calculate_tax(Decimal("100.00"), None)
        assert tax_amount == Decimal("0.00")
    
    def test_generate_payment_id(self, payment_service):
        """Test payment ID generation."""
        payment_id = payment_service._generate_payment_id()
        assert payment_id.startswith("pay_")
        assert len(payment_id) > 4
    
    def test_generate_invoice_id(self, payment_service):
        """Test invoice ID generation."""
        invoice_id = payment_service._generate_invoice_id()
        assert invoice_id.startswith("inv_")
        assert len(invoice_id) > 4
