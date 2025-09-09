"""
Payment Model

This model represents payments in the billing system,
including payment methods, status, and transaction details.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from uuid import uuid4
from decimal import Decimal


class PaymentStatus(Enum):
    """Status of payments."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    DISPUTED = "disputed"
    EXPIRED = "expired"


class PaymentMethod(Enum):
    """Payment methods."""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    ACH = "ach"
    WIRE_TRANSFER = "wire_transfer"
    CHECK = "check"
    CASH = "cash"
    CRYPTOCURRENCY = "cryptocurrency"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    APPLE_PAY = "apple_pay"
    GOOGLE_PAY = "google_pay"
    SAMSUNG_PAY = "samsung_pay"
    AMAZON_PAY = "amazon_pay"
    SQUARE = "square"
    VENMO = "venmo"
    ZELLE = "zelle"
    CASH_APP = "cash_app"
    OTHER = "other"


class PaymentIntent(Enum):
    """Payment intent types."""
    CAPTURE = "capture"
    AUTHORIZE = "authorize"
    REFUND = "refund"
    PARTIAL_REFUND = "partial_refund"
    VOID = "void"
    CHARGEBACK = "chargeback"
    DISPUTE = "dispute"


@dataclass
class Payment:
    """
    Represents a payment in the billing system.
    
    This model stores payment information including amount,
    method, status, and transaction details.
    """
    
    # Primary identifiers
    id: str = field(default_factory=lambda: str(uuid4()))
    payment_number: str = ""
    tenant_id: str = ""
    customer_id: str = ""
    
    # Payment details
    amount: Decimal = Decimal('0.00')
    currency: str = "USD"
    payment_method: PaymentMethod = PaymentMethod.CREDIT_CARD
    status: PaymentStatus = PaymentStatus.PENDING
    intent: PaymentIntent = PaymentIntent.CAPTURE
    
    # Transaction information
    transaction_id: Optional[str] = None
    gateway_transaction_id: Optional[str] = None
    gateway_response: Optional[Dict[str, Any]] = None
    
    # Payment processing
    processing_fee: Decimal = Decimal('0.00')
    net_amount: Decimal = Decimal('0.00')
    exchange_rate: Decimal = Decimal('1.00')
    
    # Dates
    payment_date: Optional[datetime] = None
    processed_date: Optional[datetime] = None
    failed_date: Optional[datetime] = None
    refunded_date: Optional[datetime] = None
    
    # Related entities
    invoice_id: Optional[str] = None
    subscription_id: Optional[str] = None
    refund_id: Optional[str] = None
    
    # Payment method details
    card_last_four: Optional[str] = None
    card_brand: Optional[str] = None
    card_exp_month: Optional[int] = None
    card_exp_year: Optional[int] = None
    bank_name: Optional[str] = None
    bank_account_last_four: Optional[str] = None
    
    # Billing information
    billing_address: Dict[str, str] = field(default_factory=dict)
    
    # Error information
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    error_details: Optional[Dict[str, Any]] = None
    
    # Metadata
    description: str = ""
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    # Webhook information
    webhook_received: bool = False
    webhook_processed: bool = False
    webhook_attempts: int = 0
    
    def __post_init__(self):
        """Calculate derived values after initialization."""
        self._calculate_net_amount()
        if not self.payment_number:
            self.payment_number = self._generate_payment_number()
    
    def _generate_payment_number(self) -> str:
        """Generate payment number."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"PAY-{timestamp}-{self.id[:8].upper()}"
    
    def _calculate_net_amount(self):
        """Calculate net amount after processing fees."""
        self.net_amount = self.amount - self.processing_fee
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "payment_number": self.payment_number,
            "tenant_id": self.tenant_id,
            "customer_id": self.customer_id,
            "amount": float(self.amount),
            "currency": self.currency,
            "payment_method": self.payment_method.value,
            "status": self.status.value,
            "intent": self.intent.value,
            "transaction_id": self.transaction_id,
            "gateway_transaction_id": self.gateway_transaction_id,
            "gateway_response": self.gateway_response,
            "processing_fee": float(self.processing_fee),
            "net_amount": float(self.net_amount),
            "exchange_rate": float(self.exchange_rate),
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "processed_date": self.processed_date.isoformat() if self.processed_date else None,
            "failed_date": self.failed_date.isoformat() if self.failed_date else None,
            "refunded_date": self.refunded_date.isoformat() if self.refunded_date else None,
            "invoice_id": self.invoice_id,
            "subscription_id": self.subscription_id,
            "refund_id": self.refund_id,
            "card_last_four": self.card_last_four,
            "card_brand": self.card_brand,
            "card_exp_month": self.card_exp_month,
            "card_exp_year": self.card_exp_year,
            "bank_name": self.bank_name,
            "bank_account_last_four": self.bank_account_last_four,
            "billing_address": self.billing_address,
            "error_code": self.error_code,
            "error_message": self.error_message,
            "error_details": self.error_details,
            "description": self.description,
            "notes": self.notes,
            "metadata": self.metadata,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "webhook_received": self.webhook_received,
            "webhook_processed": self.webhook_processed,
            "webhook_attempts": self.webhook_attempts
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Payment":
        """Create from dictionary representation."""
        # Convert timestamp strings back to datetime objects
        for field_name in ["payment_date", "processed_date", "failed_date", "refunded_date", 
                          "created_at", "updated_at"]:
            if isinstance(data.get(field_name), str):
                data[field_name] = datetime.fromisoformat(data[field_name])
        
        # Convert enum values
        if isinstance(data.get("payment_method"), str):
            data["payment_method"] = PaymentMethod(data["payment_method"])
        if isinstance(data.get("status"), str):
            data["status"] = PaymentStatus(data["status"])
        if isinstance(data.get("intent"), str):
            data["intent"] = PaymentIntent(data["intent"])
        
        # Convert Decimal fields
        for field_name in ["amount", "processing_fee", "net_amount", "exchange_rate"]:
            if isinstance(data.get(field_name), (int, float)):
                data[field_name] = Decimal(str(data[field_name]))
        
        return cls(**data)
    
    def mark_as_processing(self) -> None:
        """Mark payment as processing."""
        self.status = PaymentStatus.PROCESSING
        self.updated_at = datetime.utcnow()
    
    def mark_as_completed(self, transaction_id: Optional[str] = None, 
                         gateway_transaction_id: Optional[str] = None,
                         gateway_response: Optional[Dict[str, Any]] = None) -> None:
        """Mark payment as completed."""
        self.status = PaymentStatus.COMPLETED
        self.payment_date = datetime.utcnow()
        self.processed_date = datetime.utcnow()
        
        if transaction_id:
            self.transaction_id = transaction_id
        if gateway_transaction_id:
            self.gateway_transaction_id = gateway_transaction_id
        if gateway_response:
            self.gateway_response = gateway_response
        
        self.updated_at = datetime.utcnow()
    
    def mark_as_failed(self, error_code: str, error_message: str, 
                      error_details: Optional[Dict[str, Any]] = None) -> None:
        """Mark payment as failed."""
        self.status = PaymentStatus.FAILED
        self.failed_date = datetime.utcnow()
        self.error_code = error_code
        self.error_message = error_message
        self.error_details = error_details
        self.updated_at = datetime.utcnow()
    
    def mark_as_cancelled(self) -> None:
        """Mark payment as cancelled."""
        self.status = PaymentStatus.CANCELLED
        self.updated_at = datetime.utcnow()
    
    def mark_as_refunded(self, refund_id: Optional[str] = None) -> None:
        """Mark payment as refunded."""
        self.status = PaymentStatus.REFUNDED
        self.refunded_date = datetime.utcnow()
        if refund_id:
            self.refund_id = refund_id
        self.updated_at = datetime.utcnow()
    
    def mark_as_partially_refunded(self, refund_id: Optional[str] = None) -> None:
        """Mark payment as partially refunded."""
        self.status = PaymentStatus.PARTIALLY_REFUNDED
        if refund_id:
            self.refund_id = refund_id
        self.updated_at = datetime.utcnow()
    
    def mark_as_disputed(self) -> None:
        """Mark payment as disputed."""
        self.status = PaymentStatus.DISPUTED
        self.updated_at = datetime.utcnow()
    
    def mark_as_expired(self) -> None:
        """Mark payment as expired."""
        self.status = PaymentStatus.EXPIRED
        self.updated_at = datetime.utcnow()
    
    def is_completed(self) -> bool:
        """Check if payment is completed."""
        return self.status == PaymentStatus.COMPLETED
    
    def is_failed(self) -> bool:
        """Check if payment failed."""
        return self.status == PaymentStatus.FAILED
    
    def is_pending(self) -> bool:
        """Check if payment is pending."""
        return self.status == PaymentStatus.PENDING
    
    def is_processing(self) -> bool:
        """Check if payment is processing."""
        return self.status == PaymentStatus.PROCESSING
    
    def is_refunded(self) -> bool:
        """Check if payment is refunded."""
        return self.status in [PaymentStatus.REFUNDED, PaymentStatus.PARTIALLY_REFUNDED]
    
    def is_disputed(self) -> bool:
        """Check if payment is disputed."""
        return self.status == PaymentStatus.DISPUTED
    
    def is_expired(self) -> bool:
        """Check if payment is expired."""
        return self.status == PaymentStatus.EXPIRED
    
    def set_card_details(self, last_four: str, brand: str, exp_month: int, exp_year: int) -> None:
        """Set card details for card payments."""
        self.card_last_four = last_four
        self.card_brand = brand
        self.card_exp_month = exp_month
        self.card_exp_year = exp_year
        self.updated_at = datetime.utcnow()
    
    def set_bank_details(self, bank_name: str, account_last_four: str) -> None:
        """Set bank details for bank transfers."""
        self.bank_name = bank_name
        self.bank_account_last_four = account_last_four
        self.updated_at = datetime.utcnow()
    
    def set_processing_fee(self, fee: Decimal) -> None:
        """Set processing fee."""
        self.processing_fee = fee
        self._calculate_net_amount()
        self.updated_at = datetime.utcnow()
    
    def add_note(self, note: str) -> None:
        """Add a note to the payment."""
        if self.notes:
            self.notes += f"\n{note}"
        else:
            self.notes = note
        self.updated_at = datetime.utcnow()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the payment."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow()
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the payment."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()
    
    def get_payment_method_display(self) -> str:
        """Get display name for payment method."""
        if self.payment_method == PaymentMethod.CREDIT_CARD and self.card_brand:
            return f"{self.card_brand.title()} ****{self.card_last_four}"
        elif self.payment_method == PaymentMethod.BANK_TRANSFER and self.bank_name:
            return f"{self.bank_name} ****{self.bank_account_last_four}"
        else:
            return self.payment_method.value.replace("_", " ").title()
    
    def get_status_display(self) -> str:
        """Get display name for payment status."""
        return self.status.value.replace("_", " ").title()
    
    def get_processing_fee_percentage(self) -> float:
        """Get processing fee as percentage of amount."""
        if self.amount == 0:
            return 0.0
        return float((self.processing_fee / self.amount) * 100)
    
    def can_be_refunded(self) -> bool:
        """Check if payment can be refunded."""
        return (self.is_completed() and 
                not self.is_refunded() and 
                not self.is_disputed())
    
    def can_be_disputed(self) -> bool:
        """Check if payment can be disputed."""
        return (self.is_completed() and 
                not self.is_disputed() and
                not self.is_refunded())
    
    def get_refundable_amount(self) -> Decimal:
        """Get amount that can be refunded."""
        if not self.can_be_refunded():
            return Decimal('0.00')
        
        # In a real implementation, you'd track refunded amounts
        return self.amount
    
    def update_webhook_status(self, received: bool = True, processed: bool = False) -> None:
        """Update webhook processing status."""
        self.webhook_received = received
        self.webhook_processed = processed
        if received:
            self.webhook_attempts += 1
        self.updated_at = datetime.utcnow()
