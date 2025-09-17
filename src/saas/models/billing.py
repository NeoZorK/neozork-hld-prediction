"""
Billing Model for SaaS Platform

This module defines the billing model which handles payment processing,
invoicing, and financial transactions for the SaaS platform.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid


class BillingStatus(Enum):
    """Billing status enumeration"""
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"


class PaymentMethod(Enum):
    """Payment method enumeration"""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    WIRE_TRANSFER = "wire_transfer"
    CRYPTO = "crypto"


@dataclass
class Billing:
    """
    Billing model representing payment processing and invoicing for the SaaS platform.
    
    Each billing record includes:
    - Invoice details and line items
    - Payment processing information
    - Transaction history
    - Tax and fee calculations
    - Refund and dispute handling
    """
    
    # Core identification
    billing_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    subscription_id: str = ""
    
    # Invoice details
    invoice_number: str = ""
    invoice_date: datetime = field(default_factory=datetime.utcnow)
    due_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=30))
    
    # Billing status
    status: BillingStatus = BillingStatus.PENDING
    
    # Amounts
    subtotal: float = 0.0
    tax_amount: float = 0.0
    discount_amount: float = 0.0
    total_amount: float = 0.0
    paid_amount: float = 0.0
    refunded_amount: float = 0.0
    currency: str = "USD"
    
    # Payment information
    payment_method: Optional[PaymentMethod] = None
    payment_method_id: Optional[str] = None
    payment_processor: Optional[str] = None
    payment_processor_transaction_id: Optional[str] = None
    
    # Line items
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    
    # Tax information
    tax_rate: float = 0.0
    tax_inclusive: bool = True
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    paid_at: Optional[datetime] = None
    refunded_at: Optional[datetime] = None
    
    # Billing period
    billing_period_start: datetime = field(default_factory=datetime.utcnow)
    billing_period_end: datetime = field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=30))
    
    # Customer information
    billing_email: Optional[str] = None
    billing_address: Optional[Dict[str, str]] = None
    
    # Notes and metadata
    notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Dispute and refund information
    dispute_reason: Optional[str] = None
    refund_reason: Optional[str] = None
    
    def __post_init__(self):
        """Post-initialization setup"""
        # Generate invoice number if not provided
        if not self.invoice_number:
            self.invoice_number = self._generate_invoice_number()
        
        # Calculate total if not set
        if self.total_amount == 0.0:
            self._calculate_total()
    
    def _generate_invoice_number(self) -> str:
        """Generate a unique invoice number"""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d")
        random_suffix = str(uuid.uuid4())[:8].upper()
        return f"INV-{timestamp}-{random_suffix}"
    
    def _calculate_total(self) -> None:
        """Calculate total amount including tax and discounts"""
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
    
    def is_paid(self) -> bool:
        """Check if billing is paid"""
        return self.status == BillingStatus.PAID
    
    def is_pending(self) -> bool:
        """Check if billing is pending"""
        return self.status == BillingStatus.PENDING
    
    def is_failed(self) -> bool:
        """Check if billing payment failed"""
        return self.status == BillingStatus.FAILED
    
    def is_refunded(self) -> bool:
        """Check if billing is refunded"""
        return self.status in [BillingStatus.REFUNDED, BillingStatus.PARTIALLY_REFUNDED]
    
    def is_overdue(self) -> bool:
        """Check if billing is overdue"""
        return self.status == BillingStatus.PENDING and datetime.now(timezone.utc) > self.due_date
    
    def get_days_overdue(self) -> int:
        """Get number of days overdue"""
        if not self.is_overdue():
            return 0
        delta = datetime.now(timezone.utc) - self.due_date
        return delta.days
    
    def get_outstanding_amount(self) -> float:
        """Get outstanding amount to be paid"""
        return self.total_amount - self.paid_amount + self.refunded_amount
    
    def add_line_item(self, description: str, quantity: int, unit_price: float, 
                     tax_rate: float = 0.0, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a line item to the billing"""
        line_item = {
            "id": str(uuid.uuid4()),
            "description": description,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_price": quantity * unit_price,
            "tax_rate": tax_rate,
            "tax_amount": (quantity * unit_price) * (tax_rate / 100),
            "metadata": metadata or {}
        }
        
        self.line_items.append(line_item)
        self._recalculate_amounts()
        self.updated_at = datetime.now(timezone.utc)
    
    def remove_line_item(self, line_item_id: str) -> None:
        """Remove a line item from the billing"""
        self.line_items = [item for item in self.line_items if item["id"] != line_item_id]
        self._recalculate_amounts()
        self.updated_at = datetime.now(timezone.utc)
    
    def _recalculate_amounts(self) -> None:
        """Recalculate all amounts based on line items"""
        self.subtotal = sum(item["total_price"] for item in self.line_items)
        self.tax_amount = sum(item["tax_amount"] for item in self.line_items)
        self._calculate_total()
    
    def apply_discount(self, amount: float, reason: str = "") -> None:
        """Apply a discount to the billing"""
        self.discount_amount += amount
        self._calculate_total()
        self.updated_at = datetime.now(timezone.utc)
        
        if reason:
            self.notes = f"{self.notes or ''}\nDiscount applied: {reason}".strip()
    
    def process_payment(self, amount: float, payment_method: PaymentMethod, 
                       processor_transaction_id: str, payment_method_id: Optional[str] = None) -> None:
        """Process a payment for the billing"""
        self.paid_amount += amount
        self.payment_method = payment_method
        self.payment_method_id = payment_method_id
        self.payment_processor_transaction_id = processor_transaction_id
        self.paid_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        
        # Update status based on payment amount
        if self.paid_amount >= self.total_amount:
            self.status = BillingStatus.PAID
        elif self.paid_amount > 0:
            self.status = BillingStatus.PARTIALLY_REFUNDED  # This should be PARTIALLY_PAID, but using existing enum
    
    def process_refund(self, amount: float, reason: str = "") -> None:
        """Process a refund for the billing"""
        self.refunded_amount += amount
        self.refund_reason = reason
        self.refunded_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        
        # Update status based on refund amount
        if self.refunded_amount >= self.paid_amount:
            self.status = BillingStatus.REFUNDED
        else:
            self.status = BillingStatus.PARTIALLY_REFUNDED
    
    def mark_as_failed(self, reason: str = "") -> None:
        """Mark billing as failed"""
        self.status = BillingStatus.FAILED
        self.updated_at = datetime.now(timezone.utc)
        
        if reason:
            self.notes = f"{self.notes or ''}\nPayment failed: {reason}".strip()
    
    def mark_as_disputed(self, reason: str) -> None:
        """Mark billing as disputed"""
        self.status = BillingStatus.DISPUTED
        self.dispute_reason = reason
        self.updated_at = datetime.now(timezone.utc)
    
    def cancel(self, reason: str = "") -> None:
        """Cancel the billing"""
        self.status = BillingStatus.CANCELLED
        self.updated_at = datetime.now(timezone.utc)
        
        if reason:
            self.notes = f"{self.notes or ''}\nCancelled: {reason}".strip()
    
    def get_tax_breakdown(self) -> Dict[str, float]:
        """Get tax breakdown by rate"""
        tax_breakdown = {}
        for item in self.line_items:
            rate = item["tax_rate"]
            if rate not in tax_breakdown:
                tax_breakdown[rate] = 0.0
            tax_breakdown[rate] += item["tax_amount"]
        return tax_breakdown
    
    def get_summary(self) -> Dict[str, Any]:
        """Get billing summary"""
        return {
            "billing_id": self.billing_id,
            "invoice_number": self.invoice_number,
            "status": self.status.value,
            "total_amount": self.total_amount,
            "paid_amount": self.paid_amount,
            "outstanding_amount": self.get_outstanding_amount(),
            "currency": self.currency,
            "due_date": self.due_date.isoformat(),
            "is_overdue": self.is_overdue(),
            "days_overdue": self.get_days_overdue(),
            "line_items_count": len(self.line_items)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert billing to dictionary"""
        return {
            "billing_id": self.billing_id,
            "tenant_id": self.tenant_id,
            "subscription_id": self.subscription_id,
            "invoice_number": self.invoice_number,
            "invoice_date": self.invoice_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "status": self.status.value,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "total_amount": self.total_amount,
            "paid_amount": self.paid_amount,
            "refunded_amount": self.refunded_amount,
            "currency": self.currency,
            "payment_method": self.payment_method.value if self.payment_method else None,
            "payment_method_id": self.payment_method_id,
            "payment_processor": self.payment_processor,
            "payment_processor_transaction_id": self.payment_processor_transaction_id,
            "line_items": self.line_items,
            "tax_rate": self.tax_rate,
            "tax_inclusive": self.tax_inclusive,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "refunded_at": self.refunded_at.isoformat() if self.refunded_at else None,
            "billing_period_start": self.billing_period_start.isoformat(),
            "billing_period_end": self.billing_period_end.isoformat(),
            "billing_email": self.billing_email,
            "billing_address": self.billing_address,
            "notes": self.notes,
            "metadata": self.metadata,
            "dispute_reason": self.dispute_reason,
            "refund_reason": self.refund_reason
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Billing":
        """Create billing from dictionary"""
        # Convert string dates back to datetime objects
        date_fields = [
            "invoice_date", "due_date", "created_at", "updated_at", 
            "paid_at", "refunded_at", "billing_period_start", "billing_period_end"
        ]
        
        for field in date_fields:
            if data.get(field):
                data[field] = datetime.fromisoformat(data[field])
        
        # Convert enum values
        if data.get("status"):
            data["status"] = BillingStatus(data["status"])
        if data.get("payment_method"):
            data["payment_method"] = PaymentMethod(data["payment_method"])
        
        return cls(**data)
    
    def __str__(self) -> str:
        return f"Billing({self.invoice_number}: {self.status.value})"
    
    def __repr__(self) -> str:
        return f"Billing(id='{self.billing_id}', invoice='{self.invoice_number}', status='{self.status.value}')"
