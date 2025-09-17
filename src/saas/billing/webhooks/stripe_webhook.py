"""
Stripe webhook handler for processing billing events.
"""

import json
import hmac
import hashlib
import time
from typing import Dict, Any, Optional
from decimal import Decimal
from datetime import datetime, timezone

from src.saas.billing.models.payment import Payment, PaymentStatus
from src.saas.billing.models.invoice import Invoice, InvoiceStatus
from src.saas.billing.services.payment_service import PaymentService


class StripeWebhookHandler:
    """Handler for Stripe webhook events."""
    
    def __init__(self, webhook_secret: str, payment_service: PaymentService):
        """
        Initialize Stripe webhook handler.
        
        Args:
            webhook_secret: Stripe webhook endpoint secret
            payment_service: Payment service instance
        """
        self.webhook_secret = webhook_secret
        self.payment_service = payment_service
        self.supported_events = {
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
    
    async def handle_webhook(self, payload: str, signature: str, timestamp: int) -> Dict[str, Any]:
        """
        Handle incoming Stripe webhook.
        
        Args:
            payload: Raw webhook payload
            signature: Stripe signature header
            timestamp: Webhook timestamp
            
        Returns:
            Response dictionary
        """
        try:
            # Verify webhook signature
            if not self._verify_signature(payload, signature, timestamp):
                return {"success": False, "error": "Invalid signature"}
            
            # Parse webhook data
            event_data = json.loads(payload)
            event_type = event_data.get("type")
            
            if event_type not in self.supported_events:
                return {"success": True, "message": f"Event {event_type} not supported"}
            
            # Process the event
            result = await self._process_event(event_data)
            return result
            
        except json.JSONDecodeError:
            return {"success": False, "error": "Invalid JSON payload"}
        except Exception as e:
            return {"success": False, "error": f"Webhook processing failed: {str(e)}"}
    
    async def _process_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process specific webhook event.
        
        Args:
            event_data: Parsed webhook event data
            
        Returns:
            Processing result
        """
        event_type = event_data["type"]
        event_object = event_data["data"]["object"]
        
        if event_type == "payment_intent.succeeded":
            return await self._handle_payment_intent_succeeded(event_object)
        elif event_type == "payment_intent.payment_failed":
            return await self._handle_payment_intent_failed(event_object)
        elif event_type == "payment_intent.canceled":
            return await self._handle_payment_intent_canceled(event_object)
        elif event_type == "invoice.payment_succeeded":
            return await self._handle_invoice_payment_succeeded(event_object)
        elif event_type == "invoice.payment_failed":
            return await self._handle_invoice_payment_failed(event_object)
        elif event_type == "customer.subscription.created":
            return await self._handle_subscription_created(event_object)
        elif event_type == "customer.subscription.updated":
            return await self._handle_subscription_updated(event_object)
        elif event_type == "customer.subscription.deleted":
            return await self._handle_subscription_deleted(event_object)
        elif event_type == "charge.dispute.created":
            return await self._handle_dispute_created(event_object)
        elif event_type == "charge.refunded":
            return await self._handle_charge_refunded(event_object)
        else:
            return {"success": True, "message": f"Event {event_type} processed"}
    
    async def _handle_payment_intent_succeeded(self, payment_intent: Dict[str, Any]) -> Dict[str, Any]:
        """Handle successful payment intent."""
        try:
            payment_id = payment_intent.get("metadata", {}).get("payment_id")
            if not payment_id:
                return {"success": False, "error": "No payment ID in metadata"}
            
            # Update payment status
            payment = await self.payment_service.get_payment_by_id(payment_id)
            if not payment:
                return {"success": False, "error": "Payment not found"}
            
            payment.status = PaymentStatus.COMPLETED
            payment.gateway_transaction_id = payment_intent["id"]
            payment.gateway_response = payment_intent
            
            await self.payment_service._update_payment_status(payment)
            
            return {"success": True, "payment_id": payment_id}
            
        except Exception as e:
            return {"success": False, "error": f"Failed to process payment: {str(e)}"}
    
    async def _handle_payment_intent_failed(self, payment_intent: Dict[str, Any]) -> Dict[str, Any]:
        """Handle failed payment intent."""
        try:
            payment_id = payment_intent.get("metadata", {}).get("payment_id")
            if not payment_id:
                return {"success": False, "error": "No payment ID in metadata"}
            
            # Update payment status
            payment = await self.payment_service.get_payment_by_id(payment_id)
            if not payment:
                return {"success": False, "error": "Payment not found"}
            
            payment.status = PaymentStatus.FAILED
            payment.failure_reason = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")
            payment.gateway_response = payment_intent
            
            await self.payment_service._update_payment_status(payment)
            
            return {"success": True, "payment_id": payment_id}
            
        except Exception as e:
            return {"success": False, "error": f"Failed to process payment failure: {str(e)}"}
    
    async def _handle_payment_intent_canceled(self, payment_intent: Dict[str, Any]) -> Dict[str, Any]:
        """Handle canceled payment intent."""
        try:
            payment_id = payment_intent.get("metadata", {}).get("payment_id")
            if not payment_id:
                return {"success": False, "error": "No payment ID in metadata"}
            
            # Update payment status
            payment = await self.payment_service.get_payment_by_id(payment_id)
            if not payment:
                return {"success": False, "error": "Payment not found"}
            
            payment.status = PaymentStatus.CANCELED
            payment.gateway_response = payment_intent
            
            await self.payment_service._update_payment_status(payment)
            
            return {"success": True, "payment_id": payment_id}
            
        except Exception as e:
            return {"success": False, "error": f"Failed to process payment cancellation: {str(e)}"}
    
    async def _handle_invoice_payment_succeeded(self, invoice: Dict[str, Any]) -> Dict[str, Any]:
        """Handle successful invoice payment."""
        try:
            invoice_id = invoice.get("metadata", {}).get("invoice_id")
            if not invoice_id:
                return {"success": False, "error": "No invoice ID in metadata"}
            
            # Update invoice status
            invoice_obj = await self.payment_service.get_invoice_by_id(invoice_id)
            if not invoice_obj:
                return {"success": False, "error": "Invoice not found"}
            
            invoice_obj.status = InvoiceStatus.PAID
            invoice_obj.stripe_invoice_id = invoice["id"]
            invoice_obj.payment_id = invoice.get("payment_intent")
            
            await self.payment_service._update_invoice_status(invoice_obj)
            
            return {"success": True, "invoice_id": invoice_id}
            
        except Exception as e:
            return {"success": False, "error": f"Failed to process invoice payment: {str(e)}"}
    
    async def _handle_invoice_payment_failed(self, invoice: Dict[str, Any]) -> Dict[str, Any]:
        """Handle failed invoice payment."""
        try:
            invoice_id = invoice.get("metadata", {}).get("invoice_id")
            if not invoice_id:
                return {"success": False, "error": "No invoice ID in metadata"}
            
            # Update invoice status
            invoice_obj = await self.payment_service.get_invoice_by_id(invoice_id)
            if not invoice_obj:
                return {"success": False, "error": "Invoice not found"}
            
            invoice_obj.status = InvoiceStatus.OVERDUE
            invoice_obj.failure_reason = "Payment failed"
            
            await self.payment_service._update_invoice_status(invoice_obj)
            
            return {"success": True, "invoice_id": invoice_id}
            
        except Exception as e:
            return {"success": False, "error": f"Failed to process invoice payment failure: {str(e)}"}
    
    async def _handle_subscription_created(self, subscription: Dict[str, Any]) -> Dict[str, Any]:
        """Handle subscription creation."""
        # This would typically create a subscription record in the database
        return {"success": True, "message": "Subscription created"}
    
    async def _handle_subscription_updated(self, subscription: Dict[str, Any]) -> Dict[str, Any]:
        """Handle subscription update."""
        # This would typically update the subscription record
        return {"success": True, "message": "Subscription updated"}
    
    async def _handle_subscription_deleted(self, subscription: Dict[str, Any]) -> Dict[str, Any]:
        """Handle subscription deletion."""
        # This would typically mark the subscription as cancelled
        return {"success": True, "message": "Subscription deleted"}
    
    async def _handle_dispute_created(self, charge: Dict[str, Any]) -> Dict[str, Any]:
        """Handle charge dispute creation."""
        # This would typically create a dispute record and notify relevant parties
        return {"success": True, "message": "Dispute created"}
    
    async def _handle_charge_refunded(self, charge: Dict[str, Any]) -> Dict[str, Any]:
        """Handle charge refund."""
        try:
            payment_id = charge.get("metadata", {}).get("payment_id")
            if not payment_id:
                return {"success": False, "error": "No payment ID in metadata"}
            
            # Update payment status
            payment = await self.payment_service.get_payment_by_id(payment_id)
            if not payment:
                return {"success": False, "error": "Payment not found"}
            
            payment.status = PaymentStatus.REFUNDED
            payment.refund_id = charge.get("refunds", {}).get("data", [{}])[0].get("id")
            
            await self.payment_service._update_payment_status(payment)
            
            return {"success": True, "payment_id": payment_id}
            
        except Exception as e:
            return {"success": False, "error": f"Failed to process refund: {str(e)}"}
    
    def _verify_signature(self, payload: str, signature: str, timestamp: int) -> bool:
        """
        Verify Stripe webhook signature.
        
        Args:
            payload: Raw webhook payload
            signature: Stripe signature header
            timestamp: Webhook timestamp
            
        Returns:
            True if signature is valid
        """
        try:
            # Check timestamp (prevent replay attacks)
            current_time = int(time.time())
            if abs(current_time - timestamp) > 300:  # 5 minutes tolerance
                return False
            
            # Verify signature
            expected_signature = hmac.new(
                self.webhook_secret.encode(),
                f"{timestamp}.{payload}".encode(),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(signature, expected_signature)
            
        except Exception:
            return False
