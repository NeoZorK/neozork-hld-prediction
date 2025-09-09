"""
Payment Service

This service handles payment processing, including integration
with payment gateways, payment validation, and transaction management.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from decimal import Decimal

from ..models import Payment, PaymentStatus, PaymentMethod, PaymentIntent
from ..integrations import PaymentGateway

logger = logging.getLogger(__name__)


class PaymentService:
    """
    Service for payment processing and management.
    
    This service provides functionality to:
    - Process payments through various gateways
    - Validate payment information
    - Handle payment status updates
    - Manage payment refunds
    - Process webhooks from payment gateways
    """
    
    def __init__(self, storage_backend=None, gateway: Optional[PaymentGateway] = None):
        """
        Initialize the payment service.
        
        Args:
            storage_backend: Storage backend for persisting data
            gateway: Payment gateway integration
        """
        self.storage_backend = storage_backend
        self.gateway = gateway
        self._payment_queue = asyncio.Queue()
        self._processing = False
    
    async def start(self):
        """Start the payment service background processing."""
        if self._processing:
            return
            
        self._processing = True
        asyncio.create_task(self._process_payments())
        logger.info("Payment service started")
    
    async def stop(self):
        """Stop the payment service background processing."""
        self._processing = False
        logger.info("Payment service stopped")
    
    async def create_payment(self, tenant_id: str, customer_id: str, amount: Decimal,
                           currency: str = "USD", payment_method: PaymentMethod = PaymentMethod.CREDIT_CARD,
                           description: str = "", metadata: Optional[Dict[str, Any]] = None) -> Payment:
        """
        Create a new payment.
        
        Args:
            tenant_id: Tenant ID
            customer_id: Customer ID
            amount: Payment amount
            currency: Currency code
            payment_method: Payment method
            description: Payment description
            metadata: Additional metadata
            
        Returns:
            Created payment object
        """
        payment = Payment(
            tenant_id=tenant_id,
            customer_id=customer_id,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            description=description,
            metadata=metadata or {}
        )
        
        # Store payment
        if self.storage_backend:
            await self.storage_backend.store_payment(payment)
        
        logger.info(f"Created payment {payment.id} for tenant {tenant_id}")
        return payment
    
    async def process_payment(self, payment_id: str, payment_data: Dict[str, Any]) -> Payment:
        """
        Process a payment through the payment gateway.
        
        Args:
            payment_id: Payment ID
            payment_data: Payment data (card details, etc.)
            
        Returns:
            Updated payment object
        """
        # Get payment
        payment = await self.get_payment(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")
        
        if payment.is_completed():
            raise ValueError(f"Payment {payment_id} already completed")
        
        try:
            # Mark as processing
            payment.mark_as_processing()
            await self._update_payment(payment)
            
            # Process through gateway
            if self.gateway:
                result = await self.gateway.process_payment(payment, payment_data)
                
                if result.success:
                    payment.mark_as_completed(
                        transaction_id=result.transaction_id,
                        gateway_transaction_id=result.gateway_transaction_id,
                        gateway_response=result.gateway_response
                    )
                    
                    # Set processing fee if provided
                    if result.processing_fee:
                        payment.set_processing_fee(Decimal(str(result.processing_fee)))
                    
                    # Set payment method details
                    if result.card_details:
                        payment.set_card_details(**result.card_details)
                    elif result.bank_details:
                        payment.set_bank_details(**result.bank_details)
                    
                else:
                    payment.mark_as_failed(
                        error_code=result.error_code,
                        error_message=result.error_message,
                        error_details=result.error_details
                    )
            else:
                # No gateway configured, mark as completed for testing
                payment.mark_as_completed()
            
            # Update payment
            await self._update_payment(payment)
            
            logger.info(f"Processed payment {payment_id} with status {payment.status.value}")
            return payment
            
        except Exception as e:
            logger.error(f"Failed to process payment {payment_id}: {e}")
            payment.mark_as_failed("PROCESSING_ERROR", str(e))
            await self._update_payment(payment)
            raise
    
    async def refund_payment(self, payment_id: str, amount: Optional[Decimal] = None,
                           reason: str = "", metadata: Optional[Dict[str, Any]] = None) -> Payment:
        """
        Refund a payment.
        
        Args:
            payment_id: Payment ID
            amount: Refund amount (if None, full refund)
            reason: Refund reason
            metadata: Additional metadata
            
        Returns:
            Updated payment object
        """
        payment = await self.get_payment(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")
        
        if not payment.can_be_refunded():
            raise ValueError(f"Payment {payment_id} cannot be refunded")
        
        if amount is None:
            amount = payment.get_refundable_amount()
        
        if amount > payment.get_refundable_amount():
            raise ValueError("Refund amount exceeds refundable amount")
        
        try:
            # Process refund through gateway
            if self.gateway:
                result = await self.gateway.refund_payment(payment, amount, reason)
                
                if result.success:
                    if amount == payment.get_refundable_amount():
                        payment.mark_as_refunded()
                    else:
                        payment.mark_as_partially_refunded()
                    
                    # Add refund note
                    payment.add_note(f"Refunded {amount} {payment.currency}: {reason}")
                    
                else:
                    raise Exception(f"Refund failed: {result.error_message}")
            else:
                # No gateway configured, mark as refunded for testing
                if amount == payment.get_refundable_amount():
                    payment.mark_as_refunded()
                else:
                    payment.mark_as_partially_refunded()
            
            # Update payment
            await self._update_payment(payment)
            
            logger.info(f"Refunded payment {payment_id} for amount {amount}")
            return payment
            
        except Exception as e:
            logger.error(f"Failed to refund payment {payment_id}: {e}")
            raise
    
    async def cancel_payment(self, payment_id: str, reason: str = "") -> Payment:
        """
        Cancel a payment.
        
        Args:
            payment_id: Payment ID
            reason: Cancellation reason
            
        Returns:
            Updated payment object
        """
        payment = await self.get_payment(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")
        
        if payment.is_completed():
            raise ValueError(f"Payment {payment_id} already completed")
        
        try:
            # Cancel through gateway if needed
            if self.gateway and payment.gateway_transaction_id:
                result = await self.gateway.cancel_payment(payment)
                if not result.success:
                    raise Exception(f"Cancel failed: {result.error_message}")
            
            # Mark as cancelled
            payment.mark_as_cancelled()
            if reason:
                payment.add_note(f"Cancelled: {reason}")
            
            # Update payment
            await self._update_payment(payment)
            
            logger.info(f"Cancelled payment {payment_id}")
            return payment
            
        except Exception as e:
            logger.error(f"Failed to cancel payment {payment_id}: {e}")
            raise
    
    async def get_payment(self, payment_id: str) -> Optional[Payment]:
        """Get payment by ID."""
        if self.storage_backend:
            return await self.storage_backend.get_payment(payment_id)
        return None
    
    async def get_payments(self, tenant_id: str, customer_id: Optional[str] = None,
                         status: Optional[PaymentStatus] = None,
                         payment_method: Optional[PaymentMethod] = None,
                         start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None,
                         limit: int = 100, offset: int = 0) -> List[Payment]:
        """Get payments with filtering."""
        if self.storage_backend:
            return await self.storage_backend.get_payments(
                tenant_id=tenant_id,
                customer_id=customer_id,
                status=status,
                payment_method=payment_method,
                start_date=start_date,
                end_date=end_date,
                limit=limit,
                offset=offset
            )
        return []
    
    async def get_payment_statistics(self, tenant_id: str, 
                                   start_date: Optional[datetime] = None,
                                   end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get payment statistics for a tenant."""
        if not self.storage_backend:
            return {}
        
        payments = await self.storage_backend.get_payments(
            tenant_id=tenant_id,
            start_date=start_date,
            end_date=end_date
        )
        
        if not payments:
            return {
                "total_payments": 0,
                "total_amount": 0.0,
                "successful_payments": 0,
                "failed_payments": 0,
                "refunded_payments": 0,
                "success_rate": 0.0,
                "average_payment": 0.0
            }
        
        total_payments = len(payments)
        successful_payments = len([p for p in payments if p.is_completed()])
        failed_payments = len([p for p in payments if p.is_failed()])
        refunded_payments = len([p for p in payments if p.is_refunded()])
        
        total_amount = sum(p.amount for p in payments if p.is_completed())
        success_rate = (successful_payments / total_payments) * 100 if total_payments > 0 else 0
        average_payment = total_amount / successful_payments if successful_payments > 0 else 0
        
        return {
            "total_payments": total_payments,
            "total_amount": float(total_amount),
            "successful_payments": successful_payments,
            "failed_payments": failed_payments,
            "refunded_payments": refunded_payments,
            "success_rate": success_rate,
            "average_payment": float(average_payment)
        }
    
    async def process_webhook(self, webhook_data: Dict[str, Any]) -> bool:
        """
        Process webhook from payment gateway.
        
        Args:
            webhook_data: Webhook payload
            
        Returns:
            True if webhook was processed successfully
        """
        try:
            if not self.gateway:
                logger.warning("No payment gateway configured for webhook processing")
                return False
            
            # Verify webhook signature
            if not await self.gateway.verify_webhook(webhook_data):
                logger.error("Invalid webhook signature")
                return False
            
            # Parse webhook event
            event = await self.gateway.parse_webhook(webhook_data)
            
            # Get payment
            payment = await self.get_payment(event.payment_id)
            if not payment:
                logger.error(f"Payment {event.payment_id} not found for webhook")
                return False
            
            # Update payment based on webhook event
            if event.event_type == "payment.completed":
                payment.mark_as_completed(
                    transaction_id=event.transaction_id,
                    gateway_transaction_id=event.gateway_transaction_id,
                    gateway_response=event.gateway_response
                )
            elif event.event_type == "payment.failed":
                payment.mark_as_failed(
                    error_code=event.error_code,
                    error_message=event.error_message,
                    error_details=event.error_details
                )
            elif event.event_type == "payment.refunded":
                payment.mark_as_refunded()
            elif event.event_type == "payment.disputed":
                payment.mark_as_disputed()
            
            # Update webhook status
            payment.update_webhook_status(received=True, processed=True)
            
            # Update payment
            await self._update_payment(payment)
            
            logger.info(f"Processed webhook for payment {payment.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to process webhook: {e}")
            return False
    
    async def _process_payments(self):
        """Process payments from the queue."""
        while self._processing:
            try:
                # Get payment from queue with timeout
                payment = await asyncio.wait_for(self._payment_queue.get(), timeout=1.0)
                
                # Process payment
                await self._process_single_payment(payment)
                
                # Mark task as done
                self._payment_queue.task_done()
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing payment: {e}")
    
    async def _process_single_payment(self, payment: Payment):
        """Process a single payment."""
        try:
            # Add payment to queue for processing
            await self._payment_queue.put(payment)
            
        except Exception as e:
            logger.error(f"Failed to process payment {payment.id}: {e}")
    
    async def _update_payment(self, payment: Payment):
        """Update payment in storage."""
        if self.storage_backend:
            await self.storage_backend.update_payment(payment)
    
    async def validate_payment_data(self, payment_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate payment data.
        
        Args:
            payment_data: Payment data to validate
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Validate required fields
        required_fields = ["amount", "currency", "payment_method"]
        for field in required_fields:
            if field not in payment_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate amount
        if "amount" in payment_data:
            try:
                amount = Decimal(str(payment_data["amount"]))
                if amount <= 0:
                    errors.append("Amount must be greater than 0")
            except (ValueError, TypeError):
                errors.append("Invalid amount format")
        
        # Validate currency
        if "currency" in payment_data:
            currency = payment_data["currency"]
            if not isinstance(currency, str) or len(currency) != 3:
                errors.append("Invalid currency code")
        
        # Validate payment method
        if "payment_method" in payment_data:
            try:
                PaymentMethod(payment_data["payment_method"])
            except ValueError:
                errors.append("Invalid payment method")
        
        # Validate card details for credit card payments
        if payment_data.get("payment_method") == PaymentMethod.CREDIT_CARD.value:
            card_fields = ["card_number", "exp_month", "exp_year", "cvv"]
            for field in card_fields:
                if field not in payment_data:
                    errors.append(f"Missing required field for credit card: {field}")
        
        return len(errors) == 0, errors
    
    async def get_payment_methods(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get available payment methods for a tenant."""
        if self.gateway:
            return await self.gateway.get_payment_methods(tenant_id)
        
        # Return default payment methods
        return [
            {"id": "credit_card", "name": "Credit Card", "enabled": True},
            {"id": "debit_card", "name": "Debit Card", "enabled": True},
            {"id": "bank_transfer", "name": "Bank Transfer", "enabled": True},
            {"id": "paypal", "name": "PayPal", "enabled": True}
        ]
    
    async def get_payment_fees(self, tenant_id: str, amount: Decimal, 
                             payment_method: PaymentMethod) -> Dict[str, Any]:
        """Get payment processing fees."""
        if self.gateway:
            return await self.gateway.get_payment_fees(tenant_id, amount, payment_method)
        
        # Return default fees
        return {
            "processing_fee": float(amount * Decimal('0.029') + Decimal('0.30')),  # 2.9% + $0.30
            "currency": "USD",
            "breakdown": {
                "percentage": 2.9,
                "fixed": 0.30
            }
        }
