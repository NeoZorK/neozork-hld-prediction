"""
Payment API

This module provides API endpoints for payment processing.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from aiohttp import web
from aiohttp.web import Request, Response

from ..models import Payment, PaymentStatus, PaymentMethod, PaymentIntent
from ..services import PaymentService

logger = logging.getLogger(__name__)


class PaymentAPI:
    """
    API endpoints for payment processing.
    
    This class provides REST API endpoints for:
    - Creating payments
    - Processing payments
    - Managing payment status
    - Handling refunds
    - Processing webhooks
    """
    
    def __init__(self, payment_service: PaymentService):
        """
        Initialize the payment API.
        
        Args:
            payment_service: Payment service instance
        """
        self.payment_service = payment_service
        self.app = web.Application()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup API routes."""
        # Payment creation and processing
        self.app.router.add_post('/api/v1/payments', self.create_payment)
        self.app.router.add_post('/api/v1/payments/{payment_id}/process', self.process_payment)
        self.app.router.add_post('/api/v1/payments/{payment_id}/cancel', self.cancel_payment)
        
        # Payment retrieval
        self.app.router.add_get('/api/v1/payments/{payment_id}', self.get_payment)
        self.app.router.add_get('/api/v1/payments', self.get_payments)
        self.app.router.add_get('/api/v1/payments/statistics', self.get_payment_statistics)
        
        # Refunds
        self.app.router.add_post('/api/v1/payments/{payment_id}/refund', self.refund_payment)
        
        # Payment methods
        self.app.router.add_get('/api/v1/payment-methods', self.get_payment_methods)
        self.app.router.add_get('/api/v1/payment-fees', self.get_payment_fees)
        
        # Webhooks
        self.app.router.add_post('/api/v1/webhooks/payments', self.process_webhook)
        
        # Health check
        self.app.router.add_get('/api/v1/payments/health', self.health_check)
    
    async def create_payment(self, request: Request) -> Response:
        """Create a new payment."""
        try:
            data = await request.json()
            
            # Validate required fields
            required_fields = ["tenant_id", "customer_id", "amount", "currency"]
            for field in required_fields:
                if field not in data:
                    return web.json_response({
                        "success": False,
                        "error": f"Missing required field: {field}"
                    }, status=400)
            
            # Create payment
            payment = await self.payment_service.create_payment(
                tenant_id=data["tenant_id"],
                customer_id=data["customer_id"],
                amount=data["amount"],
                currency=data.get("currency", "USD"),
                payment_method=PaymentMethod(data.get("payment_method", "credit_card")),
                description=data.get("description", ""),
                metadata=data.get("metadata", {})
            )
            
            return web.json_response({
                "success": True,
                "payment": payment.to_dict(),
                "message": "Payment created successfully"
            })
            
        except Exception as e:
            logger.error(f"Failed to create payment: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def process_payment(self, request: Request) -> Response:
        """Process a payment."""
        try:
            payment_id = request.match_info["payment_id"]
            data = await request.json()
            
            # Validate payment data
            is_valid, errors = await self.payment_service.validate_payment_data(data)
            if not is_valid:
                return web.json_response({
                    "success": False,
                    "error": "Invalid payment data",
                    "details": errors
                }, status=400)
            
            # Process payment
            payment = await self.payment_service.process_payment(payment_id, data)
            
            return web.json_response({
                "success": True,
                "payment": payment.to_dict(),
                "message": "Payment processed successfully"
            })
            
        except ValueError as e:
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=400)
        except Exception as e:
            logger.error(f"Failed to process payment: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def cancel_payment(self, request: Request) -> Response:
        """Cancel a payment."""
        try:
            payment_id = request.match_info["payment_id"]
            data = await request.json()
            reason = data.get("reason", "")
            
            # Cancel payment
            payment = await self.payment_service.cancel_payment(payment_id, reason)
            
            return web.json_response({
                "success": True,
                "payment": payment.to_dict(),
                "message": "Payment cancelled successfully"
            })
            
        except ValueError as e:
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=400)
        except Exception as e:
            logger.error(f"Failed to cancel payment: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def get_payment(self, request: Request) -> Response:
        """Get a payment by ID."""
        try:
            payment_id = request.match_info["payment_id"]
            
            payment = await self.payment_service.get_payment(payment_id)
            if not payment:
                return web.json_response({
                    "success": False,
                    "error": "Payment not found"
                }, status=404)
            
            return web.json_response({
                "success": True,
                "payment": payment.to_dict()
            })
            
        except Exception as e:
            logger.error(f"Failed to get payment: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def get_payments(self, request: Request) -> Response:
        """Get payments with filtering."""
        try:
            # Extract query parameters
            tenant_id = request.query.get("tenant_id")
            customer_id = request.query.get("customer_id")
            status = request.query.get("status")
            payment_method = request.query.get("payment_method")
            start_date = request.query.get("start_date")
            end_date = request.query.get("end_date")
            limit = int(request.query.get("limit", 100))
            offset = int(request.query.get("offset", 0))
            
            if not tenant_id:
                return web.json_response({
                    "success": False,
                    "error": "tenant_id is required"
                }, status=400)
            
            # Parse dates
            if start_date:
                start_date = datetime.fromisoformat(start_date)
            if end_date:
                end_date = datetime.fromisoformat(end_date)
            
            # Parse enums
            status_enum = PaymentStatus(status) if status else None
            payment_method_enum = PaymentMethod(payment_method) if payment_method else None
            
            # Get payments
            payments = await self.payment_service.get_payments(
                tenant_id=tenant_id,
                customer_id=customer_id,
                status=status_enum,
                payment_method=payment_method_enum,
                start_date=start_date,
                end_date=end_date,
                limit=limit,
                offset=offset
            )
            
            # Convert to dict format
            payments_data = [payment.to_dict() for payment in payments]
            
            return web.json_response({
                "success": True,
                "payments": payments_data,
                "count": len(payments_data)
            })
            
        except Exception as e:
            logger.error(f"Failed to get payments: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def get_payment_statistics(self, request: Request) -> Response:
        """Get payment statistics."""
        try:
            tenant_id = request.query.get("tenant_id")
            start_date = request.query.get("start_date")
            end_date = request.query.get("end_date")
            
            if not tenant_id:
                return web.json_response({
                    "success": False,
                    "error": "tenant_id is required"
                }, status=400)
            
            # Parse dates
            if start_date:
                start_date = datetime.fromisoformat(start_date)
            if end_date:
                end_date = datetime.fromisoformat(end_date)
            
            # Get statistics
            statistics = await self.payment_service.get_payment_statistics(
                tenant_id=tenant_id,
                start_date=start_date,
                end_date=end_date
            )
            
            return web.json_response({
                "success": True,
                "statistics": statistics
            })
            
        except Exception as e:
            logger.error(f"Failed to get payment statistics: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def refund_payment(self, request: Request) -> Response:
        """Refund a payment."""
        try:
            payment_id = request.match_info["payment_id"]
            data = await request.json()
            
            amount = data.get("amount")
            reason = data.get("reason", "")
            metadata = data.get("metadata", {})
            
            # Refund payment
            payment = await self.payment_service.refund_payment(
                payment_id=payment_id,
                amount=amount,
                reason=reason,
                metadata=metadata
            )
            
            return web.json_response({
                "success": True,
                "payment": payment.to_dict(),
                "message": "Payment refunded successfully"
            })
            
        except ValueError as e:
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=400)
        except Exception as e:
            logger.error(f"Failed to refund payment: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def get_payment_methods(self, request: Request) -> Response:
        """Get available payment methods."""
        try:
            tenant_id = request.query.get("tenant_id")
            
            if not tenant_id:
                return web.json_response({
                    "success": False,
                    "error": "tenant_id is required"
                }, status=400)
            
            # Get payment methods
            payment_methods = await self.payment_service.get_payment_methods(tenant_id)
            
            return web.json_response({
                "success": True,
                "payment_methods": payment_methods
            })
            
        except Exception as e:
            logger.error(f"Failed to get payment methods: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def get_payment_fees(self, request: Request) -> Response:
        """Get payment processing fees."""
        try:
            tenant_id = request.query.get("tenant_id")
            amount = request.query.get("amount")
            payment_method = request.query.get("payment_method")
            
            if not all([tenant_id, amount, payment_method]):
                return web.json_response({
                    "success": False,
                    "error": "tenant_id, amount, and payment_method are required"
                }, status=400)
            
            # Get payment fees
            fees = await self.payment_service.get_payment_fees(
                tenant_id=tenant_id,
                amount=amount,
                payment_method=PaymentMethod(payment_method)
            )
            
            return web.json_response({
                "success": True,
                "fees": fees
            })
            
        except Exception as e:
            logger.error(f"Failed to get payment fees: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def process_webhook(self, request: Request) -> Response:
        """Process webhook from payment gateway."""
        try:
            data = await request.json()
            
            # Process webhook
            success = await self.payment_service.process_webhook(data)
            
            if success:
                return web.json_response({
                    "success": True,
                    "message": "Webhook processed successfully"
                })
            else:
                return web.json_response({
                    "success": False,
                    "error": "Webhook processing failed"
                }, status=400)
            
        except Exception as e:
            logger.error(f"Failed to process webhook: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def health_check(self, request: Request) -> Response:
        """Health check endpoint."""
        return web.json_response({
            "status": "healthy",
            "service": "Payment API",
            "timestamp": datetime.utcnow().isoformat()
        })
