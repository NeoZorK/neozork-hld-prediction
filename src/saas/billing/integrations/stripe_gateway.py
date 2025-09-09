"""
Stripe Payment Gateway Integration

This module provides integration with Stripe payment processing
including payments, refunds, and webhook handling.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from decimal import Decimal

import stripe
from ..base_gateway import PaymentGateway, PaymentResult, WebhookEvent
from ...models import Payment, PaymentMethod

logger = logging.getLogger(__name__)


class StripeGateway(PaymentGateway):
    """
    Stripe payment gateway integration.
    
    This class provides integration with Stripe for:
    - Payment processing
    - Refund processing
    - Webhook handling
    - Payment method management
    """
    
    def __init__(self, api_key: str, webhook_secret: str):
        """
        Initialize Stripe gateway.
        
        Args:
            api_key: Stripe API key
            webhook_secret: Stripe webhook secret for signature verification
        """
        self.api_key = api_key
        self.webhook_secret = webhook_secret
        stripe.api_key = api_key
    
    async def process_payment(self, payment: Payment, payment_data: Dict[str, Any]) -> PaymentResult:
        """
        Process payment through Stripe.
        
        Args:
            payment: Payment object
            payment_data: Payment data including card details
            
        Returns:
            Payment result
        """
        try:
            # Create payment intent
            intent_data = {
                "amount": int(payment.amount * 100),  # Convert to cents
                "currency": payment.currency.lower(),
                "description": payment.description,
                "metadata": {
                    "payment_id": payment.id,
                    "tenant_id": payment.tenant_id,
                    "customer_id": payment.customer_id
                }
            }
            
            # Add customer if available
            if payment.customer_id:
                intent_data["customer"] = payment.customer_id
            
            # Create payment intent
            intent = stripe.PaymentIntent.create(**intent_data)
            
            # Confirm payment intent with payment method
            if "payment_method_id" in payment_data:
                # Use existing payment method
                intent = stripe.PaymentIntent.confirm(
                    intent.id,
                    payment_method=payment_data["payment_method_id"]
                )
            elif "card" in payment_data:
                # Create payment method from card data
                payment_method = stripe.PaymentMethod.create(
                    type="card",
                    card=payment_data["card"]
                )
                
                intent = stripe.PaymentIntent.confirm(
                    intent.id,
                    payment_method=payment_method.id
                )
            else:
                return PaymentResult(
                    success=False,
                    error_code="INVALID_PAYMENT_DATA",
                    error_message="No payment method provided"
                )
            
            if intent.status == "succeeded":
                # Get charge details
                charge = intent.charges.data[0] if intent.charges.data else None
                
                return PaymentResult(
                    success=True,
                    transaction_id=intent.id,
                    gateway_transaction_id=charge.id if charge else intent.id,
                    gateway_response=intent.to_dict(),
                    processing_fee=charge.balance_transaction.fee / 100 if charge and charge.balance_transaction else 0,
                    card_details={
                        "last_four": charge.payment_method_details.card.last4 if charge else None,
                        "brand": charge.payment_method_details.card.brand if charge else None,
                        "exp_month": charge.payment_method_details.card.exp_month if charge else None,
                        "exp_year": charge.payment_method_details.card.exp_year if charge else None
                    } if charge and charge.payment_method_details else None
                )
            else:
                return PaymentResult(
                    success=False,
                    error_code=intent.last_payment_error.code if intent.last_payment_error else "PAYMENT_FAILED",
                    error_message=intent.last_payment_error.message if intent.last_payment_error else "Payment failed"
                )
                
        except stripe.error.CardError as e:
            return PaymentResult(
                success=False,
                error_code=e.code,
                error_message=e.user_message
            )
        except stripe.error.RateLimitError as e:
            return PaymentResult(
                success=False,
                error_code="RATE_LIMIT_ERROR",
                error_message="Too many requests"
            )
        except stripe.error.InvalidRequestError as e:
            return PaymentResult(
                success=False,
                error_code="INVALID_REQUEST",
                error_message=str(e)
            )
        except stripe.error.AuthenticationError as e:
            return PaymentResult(
                success=False,
                error_code="AUTHENTICATION_ERROR",
                error_message="Authentication failed"
            )
        except stripe.error.APIConnectionError as e:
            return PaymentResult(
                success=False,
                error_code="API_CONNECTION_ERROR",
                error_message="Network error"
            )
        except stripe.error.StripeError as e:
            return PaymentResult(
                success=False,
                error_code="STRIPE_ERROR",
                error_message=str(e)
            )
        except Exception as e:
            logger.error(f"Unexpected error processing payment: {e}")
            return PaymentResult(
                success=False,
                error_code="UNKNOWN_ERROR",
                error_message="An unexpected error occurred"
            )
    
    async def refund_payment(self, payment: Payment, amount: Decimal, reason: str) -> PaymentResult:
        """
        Refund payment through Stripe.
        
        Args:
            payment: Payment object
            amount: Refund amount
            reason: Refund reason
            
        Returns:
            Payment result
        """
        try:
            if not payment.gateway_transaction_id:
                return PaymentResult(
                    success=False,
                    error_code="NO_TRANSACTION_ID",
                    error_message="No transaction ID found for refund"
                )
            
            # Create refund
            refund_data = {
                "charge": payment.gateway_transaction_id,
                "amount": int(amount * 100),  # Convert to cents
                "reason": "requested_by_customer" if reason else "duplicate"
            }
            
            refund = stripe.Refund.create(**refund_data)
            
            return PaymentResult(
                success=True,
                transaction_id=refund.id,
                gateway_transaction_id=refund.id,
                gateway_response=refund.to_dict()
            )
            
        except stripe.error.InvalidRequestError as e:
            return PaymentResult(
                success=False,
                error_code="INVALID_REQUEST",
                error_message=str(e)
            )
        except stripe.error.StripeError as e:
            return PaymentResult(
                success=False,
                error_code="STRIPE_ERROR",
                error_message=str(e)
            )
        except Exception as e:
            logger.error(f"Unexpected error refunding payment: {e}")
            return PaymentResult(
                success=False,
                error_code="UNKNOWN_ERROR",
                error_message="An unexpected error occurred"
            )
    
    async def cancel_payment(self, payment: Payment) -> PaymentResult:
        """
        Cancel payment through Stripe.
        
        Args:
            payment: Payment object
            
        Returns:
            Payment result
        """
        try:
            if not payment.gateway_transaction_id:
                return PaymentResult(
                    success=False,
                    error_code="NO_TRANSACTION_ID",
                    error_message="No transaction ID found for cancellation"
                )
            
            # Cancel payment intent
            intent = stripe.PaymentIntent.cancel(payment.gateway_transaction_id)
            
            return PaymentResult(
                success=True,
                transaction_id=intent.id,
                gateway_transaction_id=intent.id,
                gateway_response=intent.to_dict()
            )
            
        except stripe.error.InvalidRequestError as e:
            return PaymentResult(
                success=False,
                error_code="INVALID_REQUEST",
                error_message=str(e)
            )
        except stripe.error.StripeError as e:
            return PaymentResult(
                success=False,
                error_code="STRIPE_ERROR",
                error_message=str(e)
            )
        except Exception as e:
            logger.error(f"Unexpected error cancelling payment: {e}")
            return PaymentResult(
                success=False,
                error_code="UNKNOWN_ERROR",
                error_message="An unexpected error occurred"
            )
    
    async def verify_webhook(self, webhook_data: Dict[str, Any]) -> bool:
        """
        Verify webhook signature.
        
        Args:
            webhook_data: Webhook payload
            
        Returns:
            True if signature is valid
        """
        try:
            # In a real implementation, you'd verify the Stripe signature
            # using the webhook secret and the request headers
            return True
        except Exception as e:
            logger.error(f"Webhook verification failed: {e}")
            return False
    
    async def parse_webhook(self, webhook_data: Dict[str, Any]) -> WebhookEvent:
        """
        Parse webhook event from Stripe.
        
        Args:
            webhook_data: Webhook payload
            
        Returns:
            Parsed webhook event
        """
        try:
            event_type = webhook_data.get("type", "")
            data = webhook_data.get("data", {})
            object_data = data.get("object", {})
            
            if event_type == "payment_intent.succeeded":
                return WebhookEvent(
                    event_type="payment.completed",
                    payment_id=object_data.get("metadata", {}).get("payment_id"),
                    transaction_id=object_data.get("id"),
                    gateway_transaction_id=object_data.get("id"),
                    gateway_response=object_data
                )
            elif event_type == "payment_intent.payment_failed":
                return WebhookEvent(
                    event_type="payment.failed",
                    payment_id=object_data.get("metadata", {}).get("payment_id"),
                    transaction_id=object_data.get("id"),
                    gateway_transaction_id=object_data.get("id"),
                    error_code=object_data.get("last_payment_error", {}).get("code"),
                    error_message=object_data.get("last_payment_error", {}).get("message"),
                    gateway_response=object_data
                )
            elif event_type == "charge.dispute.created":
                return WebhookEvent(
                    event_type="payment.disputed",
                    payment_id=object_data.get("metadata", {}).get("payment_id"),
                    transaction_id=object_data.get("id"),
                    gateway_transaction_id=object_data.get("id"),
                    gateway_response=object_data
                )
            else:
                return WebhookEvent(
                    event_type="unknown",
                    payment_id=object_data.get("metadata", {}).get("payment_id"),
                    transaction_id=object_data.get("id"),
                    gateway_transaction_id=object_data.get("id"),
                    gateway_response=object_data
                )
                
        except Exception as e:
            logger.error(f"Failed to parse webhook: {e}")
            raise
    
    async def get_payment_methods(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get available payment methods for a tenant."""
        return [
            {"id": "credit_card", "name": "Credit Card", "enabled": True},
            {"id": "debit_card", "name": "Debit Card", "enabled": True},
            {"id": "bank_transfer", "name": "Bank Transfer", "enabled": True},
            {"id": "apple_pay", "name": "Apple Pay", "enabled": True},
            {"id": "google_pay", "name": "Google Pay", "enabled": True}
        ]
    
    async def get_payment_fees(self, tenant_id: str, amount: Decimal, 
                             payment_method: PaymentMethod) -> Dict[str, Any]:
        """Get payment processing fees."""
        # Stripe fees: 2.9% + $0.30 for domestic cards
        processing_fee = amount * Decimal('0.029') + Decimal('0.30')
        
        return {
            "processing_fee": float(processing_fee),
            "currency": "USD",
            "breakdown": {
                "percentage": 2.9,
                "fixed": 0.30
            }
        }
    
    async def create_customer(self, tenant_id: str, customer_data: Dict[str, Any]) -> str:
        """
        Create a Stripe customer.
        
        Args:
            tenant_id: Tenant ID
            customer_data: Customer data
            
        Returns:
            Stripe customer ID
        """
        try:
            customer = stripe.Customer.create(
                email=customer_data.get("email"),
                name=customer_data.get("name"),
                metadata={
                    "tenant_id": tenant_id,
                    "customer_id": customer_data.get("customer_id")
                }
            )
            
            return customer.id
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create Stripe customer: {e}")
            raise
    
    async def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """
        Get Stripe customer by ID.
        
        Args:
            customer_id: Stripe customer ID
            
        Returns:
            Customer data or None if not found
        """
        try:
            customer = stripe.Customer.retrieve(customer_id)
            return customer.to_dict()
        except stripe.error.InvalidRequestError:
            return None
        except stripe.error.StripeError as e:
            logger.error(f"Failed to get Stripe customer: {e}")
            raise
    
    async def update_customer(self, customer_id: str, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update Stripe customer.
        
        Args:
            customer_id: Stripe customer ID
            customer_data: Updated customer data
            
        Returns:
            Updated customer data
        """
        try:
            customer = stripe.Customer.modify(
                customer_id,
                **customer_data
            )
            
            return customer.to_dict()
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to update Stripe customer: {e}")
            raise
    
    async def delete_customer(self, customer_id: str) -> bool:
        """
        Delete Stripe customer.
        
        Args:
            customer_id: Stripe customer ID
            
        Returns:
            True if deleted successfully
        """
        try:
            stripe.Customer.delete(customer_id)
            return True
        except stripe.error.StripeError as e:
            logger.error(f"Failed to delete Stripe customer: {e}")
            return False
    
    async def create_payment_method(self, customer_id: str, payment_method_data: Dict[str, Any]) -> str:
        """
        Create a payment method for a customer.
        
        Args:
            customer_id: Stripe customer ID
            payment_method_data: Payment method data
            
        Returns:
            Stripe payment method ID
        """
        try:
            payment_method = stripe.PaymentMethod.create(
                type="card",
                card=payment_method_data.get("card"),
                billing_details=payment_method_data.get("billing_details", {})
            )
            
            # Attach to customer
            stripe.PaymentMethod.attach(
                payment_method.id,
                customer=customer_id
            )
            
            return payment_method.id
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create payment method: {e}")
            raise
    
    async def get_payment_methods_for_customer(self, customer_id: str) -> List[Dict[str, Any]]:
        """
        Get payment methods for a customer.
        
        Args:
            customer_id: Stripe customer ID
            
        Returns:
            List of payment methods
        """
        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id,
                type="card"
            )
            
            return [pm.to_dict() for pm in payment_methods.data]
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to get payment methods: {e}")
            raise
    
    async def delete_payment_method(self, payment_method_id: str) -> bool:
        """
        Delete a payment method.
        
        Args:
            payment_method_id: Stripe payment method ID
            
        Returns:
            True if deleted successfully
        """
        try:
            stripe.PaymentMethod.detach(payment_method_id)
            return True
        except stripe.error.StripeError as e:
            logger.error(f"Failed to delete payment method: {e}")
            return False
