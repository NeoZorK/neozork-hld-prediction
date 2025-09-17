"""
Invoice Model

This model represents invoices in the billing system,
including line items, taxes, discounts, and payment status.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from uuid import uuid4
from decimal import Decimal


class InvoiceStatus(Enum):
    """Status of invoices."""
    DRAFT = "draft"
    PENDING = "pending"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_PAID = "partially_paid"
    PARTIALLY_REFUNDED = "partially_refunded"


class InvoiceType(Enum):
    """Types of invoices."""
    STANDARD = "standard"
    CREDIT_NOTE = "credit_note"
    DEBIT_NOTE = "debit_note"
    PROFORMA = "proforma"
    RECURRING = "recurring"
    ONE_TIME = "one_time"


@dataclass
class Invoice:
    """
    Represents an invoice in the billing system.
    
    This model stores invoice information including line items,
    taxes, discounts, and payment status.
    """
    
    # Primary identifiers
    id: str = field(default_factory=lambda: str(uuid4()))
    invoice_number: str = ""
    tenant_id: str = ""
    customer_id: str = ""
    
    # Invoice details
    invoice_type: InvoiceType = InvoiceType.STANDARD
    status: InvoiceStatus = InvoiceStatus.DRAFT
    title: str = ""
    description: str = ""
    
    # Dates
    issue_date: datetime = field(default_factory=datetime.utcnow)
    due_date: datetime = field(default_factory=lambda: datetime.now(datetime.UTC) + timedelta(days=30))
    paid_date: Optional[datetime] = None
    
    # Financial information
    subtotal: Decimal = Decimal('0.00')
    tax_amount: Decimal = Decimal('0.00')
    discount_amount: Decimal = Decimal('0.00')
    total_amount: Decimal = Decimal('0.00')
    paid_amount: Decimal = Decimal('0.00')
    refunded_amount: Decimal = Decimal('0.00')
    balance_due: Decimal = Decimal('0.00')
    
    # Currency
    currency: str = "USD"
    exchange_rate: Decimal = Decimal('1.00')
    
    # Line items
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    
    # Taxes
    taxes: List[Dict[str, Any]] = field(default_factory=list)
    
    # Discounts
    discounts: List[Dict[str, Any]] = field(default_factory=list)
    
    # Payment information
    payment_terms: str = "Net 30"
    payment_method: Optional[str] = None
    payment_reference: Optional[str] = None
    
    # Customer information
    customer_name: str = ""
    customer_email: str = ""
    customer_address: Dict[str, str] = field(default_factory=dict)
    
    # Billing information
    billing_address: Dict[str, str] = field(default_factory=dict)
    
    # Metadata
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    # Related entities
    subscription_id: Optional[str] = None
    parent_invoice_id: Optional[str] = None
    
    def __post_init__(self):
        """Calculate derived values after initialization."""
        self._calculate_totals()
        if not self.invoice_number:
            self.invoice_number = self._generate_invoice_number()
    
    def _generate_invoice_number(self) -> str:
        """Generate invoice number."""
        timestamp = datetime.now(datetime.UTC).strftime("%Y%m%d%H%M%S")
        return f"INV-{timestamp}-{self.id[:8].upper()}"
    
    def _calculate_totals(self):
        """Calculate invoice totals."""
        # Calculate subtotal from line items
        self.subtotal = sum(
            Decimal(str(item.get("amount", 0))) for item in self.line_items
        )
        
        # Calculate tax amount
        self.tax_amount = sum(
            Decimal(str(tax.get("amount", 0))) for tax in self.taxes
        )
        
        # Calculate discount amount
        self.discount_amount = sum(
            Decimal(str(discount.get("amount", 0))) for discount in self.discounts
        )
        
        # Calculate total amount
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
        
        # Calculate balance due
        self.balance_due = self.total_amount - self.paid_amount + self.refunded_amount
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "invoice_number": self.invoice_number,
            "tenant_id": self.tenant_id,
            "customer_id": self.customer_id,
            "invoice_type": self.invoice_type.value,
            "status": self.status.value,
            "title": self.title,
            "description": self.description,
            "issue_date": self.issue_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "paid_date": self.paid_date.isoformat() if self.paid_date else None,
            "subtotal": float(self.subtotal),
            "tax_amount": float(self.tax_amount),
            "discount_amount": float(self.discount_amount),
            "total_amount": float(self.total_amount),
            "paid_amount": float(self.paid_amount),
            "refunded_amount": float(self.refunded_amount),
            "balance_due": float(self.balance_due),
            "currency": self.currency,
            "exchange_rate": float(self.exchange_rate),
            "line_items": self.line_items,
            "taxes": self.taxes,
            "discounts": self.discounts,
            "payment_terms": self.payment_terms,
            "payment_method": self.payment_method,
            "payment_reference": self.payment_reference,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "customer_address": self.customer_address,
            "billing_address": self.billing_address,
            "notes": self.notes,
            "metadata": self.metadata,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "subscription_id": self.subscription_id,
            "parent_invoice_id": self.parent_invoice_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Invoice":
        """Create from dictionary representation."""
        # Convert timestamp strings back to datetime objects
        for field_name in ["issue_date", "due_date", "paid_date", "created_at", "updated_at"]:
            if isinstance(data.get(field_name), str):
                data[field_name] = datetime.fromisoformat(data[field_name])
        
        # Convert enum values
        if isinstance(data.get("invoice_type"), str):
            data["invoice_type"] = InvoiceType(data["invoice_type"])
        if isinstance(data.get("status"), str):
            data["status"] = InvoiceStatus(data["status"])
        
        # Convert Decimal fields
        for field_name in ["subtotal", "tax_amount", "discount_amount", "total_amount", 
                          "paid_amount", "refunded_amount", "balance_due", "exchange_rate"]:
            if isinstance(data.get(field_name), (int, float)):
                data[field_name] = Decimal(str(data[field_name]))
        
        return cls(**data)
    
    def add_line_item(self, description: str, quantity: int, unit_price: Decimal, 
                     tax_rate: Decimal = Decimal('0.00'), discount_rate: Decimal = Decimal('0.00')) -> None:
        """Add a line item to the invoice."""
        amount = quantity * unit_price
        tax_amount = amount * tax_rate
        discount_amount = amount * discount_rate
        line_total = amount + tax_amount - discount_amount
        
        line_item = {
            "id": str(uuid4()),
            "description": description,
            "quantity": quantity,
            "unit_price": float(unit_price),
            "amount": float(amount),
            "tax_rate": float(tax_rate),
            "tax_amount": float(tax_amount),
            "discount_rate": float(discount_rate),
            "discount_amount": float(discount_amount),
            "line_total": float(line_total)
        }
        
        self.line_items.append(line_item)
        self._calculate_totals()
        self.updated_at = datetime.now(datetime.UTC)
    
    def add_tax(self, name: str, rate: Decimal, amount: Optional[Decimal] = None) -> None:
        """Add tax to the invoice."""
        if amount is None:
            amount = self.subtotal * rate
        
        tax = {
            "id": str(uuid4()),
            "name": name,
            "rate": float(rate),
            "amount": float(amount)
        }
        
        self.taxes.append(tax)
        self._calculate_totals()
        self.updated_at = datetime.now(datetime.UTC)
    
    def add_discount(self, name: str, amount: Decimal, percentage: Optional[Decimal] = None) -> None:
        """Add discount to the invoice."""
        if percentage is not None:
            amount = self.subtotal * percentage
        
        discount = {
            "id": str(uuid4()),
            "name": name,
            "amount": float(amount),
            "percentage": float(percentage) if percentage else None
        }
        
        self.discounts.append(discount)
        self._calculate_totals()
        self.updated_at = datetime.now(datetime.UTC)
    
    def mark_as_sent(self) -> None:
        """Mark invoice as sent."""
        self.status = InvoiceStatus.SENT
        self.updated_at = datetime.now(datetime.UTC)
    
    def mark_as_paid(self, payment_amount: Decimal, payment_method: str, 
                    payment_reference: Optional[str] = None) -> None:
        """Mark invoice as paid."""
        self.paid_amount += payment_amount
        self.payment_method = payment_method
        self.payment_reference = payment_reference
        
        if self.paid_amount >= self.total_amount:
            self.status = InvoiceStatus.PAID
            self.paid_date = datetime.now(datetime.UTC)
        else:
            self.status = InvoiceStatus.PARTIALLY_PAID
        
        self._calculate_totals()
        self.updated_at = datetime.now(datetime.UTC)
    
    def mark_as_refunded(self, refund_amount: Decimal) -> None:
        """Mark invoice as refunded."""
        self.refunded_amount += refund_amount
        
        if self.refunded_amount >= self.paid_amount:
            self.status = InvoiceStatus.REFUNDED
        else:
            self.status = InvoiceStatus.PARTIALLY_REFUNDED
        
        self._calculate_totals()
        self.updated_at = datetime.now(datetime.UTC)
    
    def mark_as_overdue(self) -> None:
        """Mark invoice as overdue."""
        if self.status in [InvoiceStatus.SENT, InvoiceStatus.PARTIALLY_PAID]:
            self.status = InvoiceStatus.OVERDUE
            self.updated_at = datetime.now(datetime.UTC)
    
    def cancel(self) -> None:
        """Cancel the invoice."""
        self.status = InvoiceStatus.CANCELLED
        self.updated_at = datetime.now(datetime.UTC)
    
    def is_overdue(self) -> bool:
        """Check if invoice is overdue."""
        return (self.status == InvoiceStatus.OVERDUE or 
                (self.status in [InvoiceStatus.SENT, InvoiceStatus.PARTIALLY_PAID] and 
                 datetime.now(datetime.UTC) > self.due_date))
    
    def is_paid(self) -> bool:
        """Check if invoice is fully paid."""
        return self.status == InvoiceStatus.PAID
    
    def is_partially_paid(self) -> bool:
        """Check if invoice is partially paid."""
        return self.status == InvoiceStatus.PARTIALLY_PAID
    
    def get_days_overdue(self) -> int:
        """Get number of days overdue."""
        if not self.is_overdue():
            return 0
        
        overdue_date = self.due_date if self.status == InvoiceStatus.OVERDUE else datetime.now(datetime.UTC)
        return (overdue_date - self.due_date).days
    
    def get_payment_status(self) -> str:
        """Get payment status description."""
        if self.is_paid():
            return "Paid"
        elif self.is_partially_paid():
            return f"Partially Paid ({self.paid_amount}/{self.total_amount})"
        elif self.is_overdue():
            return f"Overdue ({self.get_days_overdue()} days)"
        else:
            return "Pending"
    
    def add_note(self, note: str) -> None:
        """Add a note to the invoice."""
        if self.notes:
            self.notes += f"\n{note}"
        else:
            self.notes = note
        self.updated_at = datetime.now(datetime.UTC)
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the invoice."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now(datetime.UTC)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the invoice."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now(datetime.UTC)
    
    def get_remaining_balance(self) -> Decimal:
        """Get remaining balance to be paid."""
        return self.balance_due
    
    def get_payment_percentage(self) -> float:
        """Get payment percentage."""
        if self.total_amount == 0:
            return 0.0
        return float((self.paid_amount / self.total_amount) * 100)
