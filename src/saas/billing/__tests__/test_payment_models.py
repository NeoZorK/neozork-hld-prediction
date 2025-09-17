"""
Test cases for payment models.
"""

import pytest
from datetime import datetime, timezone
from decimal import Decimal
from src.saas.billing.models.payment import Payment, PaymentStatus, PaymentMethod
from src.saas.billing.models.invoice import Invoice, InvoiceStatus


class TestPayment:
    """Test cases for Payment model."""
    
    def test_payment_creation(self):
        """Test basic payment creation."""
        payment = Payment(
            id="pay_123",
            tenant_id="tenant_456",
            amount=Decimal("99.99"),
            currency="USD",
            status=PaymentStatus.PENDING,
            payment_method=PaymentMethod.CREDIT_CARD
        )
        
        assert payment.id == "pay_123"
        assert payment.tenant_id == "tenant_456"
        assert payment.amount == Decimal("99.99")
        assert payment.currency == "USD"
        assert payment.status == PaymentStatus.PENDING
        assert payment.payment_method == PaymentMethod.CREDIT_CARD
        assert payment.created_at is not None
        assert payment.updated_at is not None
    
    def test_payment_status_transitions(self):
        """Test payment status transitions."""
        payment = Payment(
            id="pay_123",
            tenant_id="tenant_456",
            amount=Decimal("99.99"),
            currency="USD",
            status=PaymentStatus.PENDING,
            payment_method=PaymentMethod.CREDIT_CARD
        )
        
        # Test valid transitions
        payment.status = PaymentStatus.PROCESSING
        assert payment.status == PaymentStatus.PROCESSING
        
        payment.status = PaymentStatus.COMPLETED
        assert payment.status == PaymentStatus.COMPLETED
    
    def test_payment_validation(self):
        """Test payment validation."""
        with pytest.raises(ValueError, match="Amount must be positive"):
            Payment(
                id="pay_123",
                tenant_id="tenant_456",
                amount=Decimal("-10.00"),
                currency="USD",
                status=PaymentStatus.PENDING,
                payment_method=PaymentMethod.CREDIT_CARD
            )
    
    def test_payment_serialization(self):
        """Test payment serialization to dict."""
        payment = Payment(
            id="pay_123",
            tenant_id="tenant_456",
            amount=Decimal("99.99"),
            currency="USD",
            status=PaymentStatus.PENDING,
            payment_method=PaymentMethod.CREDIT_CARD,
            stripe_payment_intent_id="pi_123"
        )
        
        data = payment.to_dict()
        assert data["id"] == "pay_123"
        assert data["tenant_id"] == "tenant_456"
        assert data["amount"] == "99.99"
        assert data["currency"] == "USD"
        assert data["status"] == "pending"
        assert data["payment_method"] == "credit_card"
        assert data["stripe_payment_intent_id"] == "pi_123"


class TestInvoice:
    """Test cases for Invoice model."""
    
    def test_invoice_creation(self):
        """Test basic invoice creation."""
        invoice = Invoice(
            id="inv_123",
            tenant_id="tenant_456",
            amount=Decimal("199.99"),
            currency="USD",
            status=InvoiceStatus.DRAFT,
            due_date=datetime.now(timezone.utc)
        )
        
        assert invoice.id == "inv_123"
        assert invoice.tenant_id == "tenant_456"
        assert invoice.amount == Decimal("199.99")
        assert invoice.currency == "USD"
        assert invoice.status == InvoiceStatus.DRAFT
        assert invoice.due_date is not None
        assert invoice.created_at is not None
        assert invoice.updated_at is not None
    
    def test_invoice_status_transitions(self):
        """Test invoice status transitions."""
        invoice = Invoice(
            id="inv_123",
            tenant_id="tenant_456",
            amount=Decimal("199.99"),
            currency="USD",
            status=InvoiceStatus.DRAFT,
            due_date=datetime.now(timezone.utc)
        )
        
        # Test valid transitions
        invoice.status = InvoiceStatus.SENT
        assert invoice.status == InvoiceStatus.SENT
        
        invoice.status = InvoiceStatus.PAID
        assert invoice.status == InvoiceStatus.PAID
    
    def test_invoice_validation(self):
        """Test invoice validation."""
        with pytest.raises(ValueError, match="Amount must be positive"):
            Invoice(
                id="inv_123",
                tenant_id="tenant_456",
                amount=Decimal("-50.00"),
                currency="USD",
                status=InvoiceStatus.DRAFT,
                due_date=datetime.now(timezone.utc)
            )
    
    def test_invoice_serialization(self):
        """Test invoice serialization to dict."""
        due_date = datetime.now(timezone.utc)
        invoice = Invoice(
            id="inv_123",
            tenant_id="tenant_456",
            amount=Decimal("199.99"),
            currency="USD",
            status=InvoiceStatus.DRAFT,
            due_date=due_date,
            stripe_invoice_id="in_123"
        )
        
        data = invoice.to_dict()
        assert data["id"] == "inv_123"
        assert data["tenant_id"] == "tenant_456"
        assert data["amount"] == "199.99"
        assert data["currency"] == "USD"
        assert data["status"] == "draft"
        assert data["due_date"] == due_date.isoformat()
        assert data["stripe_invoice_id"] == "in_123"
    
    def test_invoice_calculations(self):
        """Test invoice tax and total calculations."""
        invoice = Invoice(
            id="inv_123",
            tenant_id="tenant_456",
            amount=Decimal("100.00"),
            currency="USD",
            status=InvoiceStatus.DRAFT,
            due_date=datetime.now(timezone.utc),
            tax_rate=Decimal("0.08")
        )
        
        assert invoice.tax_amount == Decimal("8.00")
        assert invoice.total_amount == Decimal("108.00")
