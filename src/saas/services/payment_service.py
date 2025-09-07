"""
Payment Service for SaaS Platform

This service handles payment processing integration with Stripe and other payment providers.
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
import stripe
from ..models.billing import Billing, BillingStatus, PaymentMethod
from ..models.subscription import Subscription

logger = logging.getLogger(__name__)


class PaymentService:
    """
    Payment processing service for the SaaS platform.
    
    This service provides:
    - Stripe integration for payment processing
    - Subscription billing management
    - Payment method management
    - Invoice generation and management
    - Webhook handling for payment events
    """
    
    def __init__(self, stripe_secret_key: str):
        self.stripe_secret_key = stripe_secret_key
        stripe.api_key = stripe_secret_key
    
    async def create_customer(self, email: str, name: str, tenant_id: str) -> Dict[str, Any]:
        """
        Create a Stripe customer.
        
        Args:
            email: Customer email
            name: Customer name
            tenant_id: Tenant ID
            
        Returns:
            Dict containing customer information
        """
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={
                    'tenant_id': tenant_id
                }
            )
            
            return {
                'status': 'success',
                'customer_id': customer.id,
                'customer': customer
            }
            
        except Exception as e:
            logger.error(f"Error creating Stripe customer: {e}")
            return {
                'status': 'error',
                'message': f"Failed to create customer: {str(e)}"
            }
    
    async def create_payment_method(self, customer_id: str, payment_method_id: str) -> Dict[str, Any]:
        """
        Attach a payment method to a customer.
        
        Args:
            customer_id: Stripe customer ID
            payment_method_id: Stripe payment method ID
            
        Returns:
            Dict containing payment method information
        """
        try:
            payment_method = stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer_id
            )
            
            # Set as default payment method
            stripe.Customer.modify(
                customer_id,
                invoice_settings={
                    'default_payment_method': payment_method_id
                }
            )
            
            return {
                'status': 'success',
                'payment_method': payment_method
            }
            
        except Exception as e:
            logger.error(f"Error creating payment method: {e}")
            return {
                'status': 'error',
                'message': f"Failed to create payment method: {str(e)}"
            }
    
    async def create_subscription(self, customer_id: str, price_id: str, 
                                 trial_period_days: int = 0) -> Dict[str, Any]:
        """
        Create a Stripe subscription.
        
        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID
            trial_period_days: Trial period in days
            
        Returns:
            Dict containing subscription information
        """
        try:
            subscription_data = {
                'customer': customer_id,
                'items': [{'price': price_id}],
                'payment_behavior': 'default_incomplete',
                'payment_settings': {'save_default_payment_method': 'on_subscription'},
                'expand': ['latest_invoice.payment_intent']
            }
            
            if trial_period_days > 0:
                subscription_data['trial_period_days'] = trial_period_days
            
            subscription = stripe.Subscription.create(**subscription_data)
            
            return {
                'status': 'success',
                'subscription_id': subscription.id,
                'subscription': subscription
            }
            
        except Exception as e:
            logger.error(f"Error creating Stripe subscription: {e}")
            return {
                'status': 'error',
                'message': f"Failed to create subscription: {str(e)}"
            }
    
    async def process_payment(self, billing: Billing, payment_method_id: str) -> Dict[str, Any]:
        """
        Process a payment for a billing record.
        
        Args:
            billing: Billing record
            payment_method_id: Stripe payment method ID
            
        Returns:
            Dict containing payment result
        """
        try:
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=int(billing.total_amount * 100),  # Convert to cents
                currency=billing.currency.lower(),
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True,
                metadata={
                    'billing_id': billing.billing_id,
                    'tenant_id': billing.tenant_id
                }
            )
            
            if intent.status == 'succeeded':
                # Update billing record
                billing.process_payment(
                    amount=billing.total_amount,
                    payment_method=PaymentMethod.STRIPE,
                    processor_transaction_id=intent.id,
                    payment_method_id=payment_method_id
                )
                
                return {
                    'status': 'success',
                    'payment_intent': intent,
                    'message': 'Payment processed successfully'
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Payment failed: {intent.status}'
                }
                
        except Exception as e:
            logger.error(f"Error processing payment: {e}")
            return {
                'status': 'error',
                'message': f"Payment processing failed: {str(e)}"
            }
    
    async def create_invoice(self, customer_id: str, subscription_id: str) -> Dict[str, Any]:
        """
        Create an invoice for a subscription.
        
        Args:
            customer_id: Stripe customer ID
            subscription_id: Stripe subscription ID
            
        Returns:
            Dict containing invoice information
        """
        try:
            invoice = stripe.Invoice.create(
                customer=customer_id,
                subscription=subscription_id,
                auto_advance=True
            )
            
            return {
                'status': 'success',
                'invoice_id': invoice.id,
                'invoice': invoice
            }
            
        except Exception as e:
            logger.error(f"Error creating invoice: {e}")
            return {
                'status': 'error',
                'message': f"Failed to create invoice: {str(e)}"
            }
    
    async def handle_webhook(self, payload: str, signature: str, webhook_secret: str) -> Dict[str, Any]:
        """
        Handle Stripe webhook events.
        
        Args:
            payload: Webhook payload
            signature: Webhook signature
            webhook_secret: Webhook secret
            
        Returns:
            Dict containing webhook handling result
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            
            # Handle different event types
            if event['type'] == 'invoice.payment_succeeded':
                await self._handle_payment_succeeded(event['data']['object'])
            elif event['type'] == 'invoice.payment_failed':
                await self._handle_payment_failed(event['data']['object'])
            elif event['type'] == 'customer.subscription.updated':
                await self._handle_subscription_updated(event['data']['object'])
            elif event['type'] == 'customer.subscription.deleted':
                await self._handle_subscription_deleted(event['data']['object'])
            
            return {
                'status': 'success',
                'message': 'Webhook handled successfully'
            }
            
        except Exception as e:
            logger.error(f"Error handling webhook: {e}")
            return {
                'status': 'error',
                'message': f"Webhook handling failed: {str(e)}"
            }
    
    async def _handle_payment_succeeded(self, invoice: Dict[str, Any]):
        """Handle successful payment webhook."""
        logger.info(f"Payment succeeded for invoice: {invoice['id']}")
        # Update billing record, send confirmation email, etc.
    
    async def _handle_payment_failed(self, invoice: Dict[str, Any]):
        """Handle failed payment webhook."""
        logger.warning(f"Payment failed for invoice: {invoice['id']}")
        # Update billing record, send notification, etc.
    
    async def _handle_subscription_updated(self, subscription: Dict[str, Any]):
        """Handle subscription update webhook."""
        logger.info(f"Subscription updated: {subscription['id']}")
        # Update subscription record, etc.
    
    async def _handle_subscription_deleted(self, subscription: Dict[str, Any]):
        """Handle subscription cancellation webhook."""
        logger.info(f"Subscription cancelled: {subscription['id']}")
        # Update subscription record, etc.
    
    async def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """
        Cancel a Stripe subscription.
        
        Args:
            subscription_id: Stripe subscription ID
            
        Returns:
            Dict containing cancellation result
        """
        try:
            subscription = stripe.Subscription.delete(subscription_id)
            
            return {
                'status': 'success',
                'subscription': subscription,
                'message': 'Subscription cancelled successfully'
            }
            
        except Exception as e:
            logger.error(f"Error cancelling subscription: {e}")
            return {
                'status': 'error',
                'message': f"Failed to cancel subscription: {str(e)}"
            }
    
    async def get_customer_payment_methods(self, customer_id: str) -> Dict[str, Any]:
        """
        Get payment methods for a customer.
        
        Args:
            customer_id: Stripe customer ID
            
        Returns:
            Dict containing payment methods
        """
        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id,
                type='card'
            )
            
            return {
                'status': 'success',
                'payment_methods': payment_methods.data
            }
            
        except Exception as e:
            logger.error(f"Error getting payment methods: {e}")
            return {
                'status': 'error',
                'message': f"Failed to get payment methods: {str(e)}"
            }
