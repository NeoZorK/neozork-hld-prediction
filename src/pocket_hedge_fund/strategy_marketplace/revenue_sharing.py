"""Revenue Sharing - Revenue distribution and payment system"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class PaymentMethod(Enum):
    """Payment method enumeration."""
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    CRYPTO = "crypto"


class PaymentStatus(Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class RevenueShare:
    """Revenue share data class."""
    share_id: str
    strategy_id: str
    author_id: str
    period_start: datetime
    period_end: datetime
    total_revenue: float
    author_earnings: float
    platform_earnings: float
    calculated_at: datetime
    paid_at: Optional[datetime] = None
    payment_status: PaymentStatus = PaymentStatus.PENDING


class RevenueSharing:
    """Revenue distribution and payment system."""
    
    def __init__(self):
        self.revenue_shares: Dict[str, List[RevenueShare]] = {}
        self.payments: Dict[str, List[Dict[str, Any]]] = {}
        self.author_accounts: Dict[str, Dict[str, Any]] = {}
        
    async def calculate_revenue_share(self, strategy_id: str, author_id: str,
                                    period_start: datetime, period_end: datetime,
                                    total_revenue: float, platform_commission: float = 0.30) -> Dict[str, Any]:
        """Calculate revenue share for a strategy."""
        try:
            # Calculate shares
            platform_earnings = total_revenue * platform_commission
            author_earnings = total_revenue * (1 - platform_commission)
            
            # Create revenue share record
            share_id = str(uuid.uuid4())
            revenue_share = RevenueShare(
                share_id=share_id,
                strategy_id=strategy_id,
                author_id=author_id,
                period_start=period_start,
                period_end=period_end,
                total_revenue=total_revenue,
                author_earnings=author_earnings,
                platform_earnings=platform_earnings,
                calculated_at=datetime.now()
            )
            
            # Store revenue share
            if strategy_id not in self.revenue_shares:
                self.revenue_shares[strategy_id] = []
            self.revenue_shares[strategy_id].append(revenue_share)
            
            logger.info(f"Calculated revenue share for strategy {strategy_id}: {author_earnings}")
            return {
                'share_id': share_id,
                'strategy_id': strategy_id,
                'author_id': author_id,
                'total_revenue': total_revenue,
                'author_earnings': author_earnings,
                'platform_earnings': platform_earnings,
                'revenue_share': revenue_share.__dict__
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate revenue share: {e}")
            return {'error': str(e)}
    
    async def process_author_payment(self, author_id: str, amount: float,
                                   payment_method: PaymentMethod,
                                   currency: str = "USD") -> Dict[str, Any]:
        """Process payment to strategy author."""
        try:
            # Check if author has payment account set up
            if author_id not in self.author_accounts:
                return {'error': 'Author payment account not set up'}
            
            # Create payment record
            payment_id = str(uuid.uuid4())
            payment = {
                'payment_id': payment_id,
                'recipient_id': author_id,
                'amount': amount,
                'currency': currency,
                'payment_method': payment_method.value,
                'status': PaymentStatus.PENDING.value,
                'created_at': datetime.now()
            }
            
            # Store payment
            if author_id not in self.payments:
                self.payments[author_id] = []
            self.payments[author_id].append(payment)
            
            # Process payment
            payment_result = await self._process_payment(payment)
            
            if payment_result['success']:
                payment['status'] = PaymentStatus.COMPLETED.value
                payment['processed_at'] = datetime.now()
                payment['transaction_id'] = payment_result['transaction_id']
                
                logger.info(f"Payment processed for author {author_id}: {amount}")
                return {
                    'status': 'success',
                    'payment_id': payment_id,
                    'transaction_id': payment['transaction_id'],
                    'amount': amount,
                    'processed_at': payment['processed_at']
                }
            else:
                payment['status'] = PaymentStatus.FAILED.value
                return {
                    'status': 'failed',
                    'error': payment_result['error']
                }
                
        except Exception as e:
            logger.error(f"Failed to process author payment: {e}")
            return {'error': str(e)}
    
    async def setup_author_account(self, author_id: str, account_details: Dict[str, Any]) -> Dict[str, Any]:
        """Set up payment account for strategy author."""
        try:
            # Validate account details
            payment_method = account_details.get('payment_method')
            if not payment_method:
                return {'error': 'Payment method is required'}
            
            # Store account details
            self.author_accounts[author_id] = {
                'payment_method': payment_method,
                'account_details': account_details,
                'setup_date': datetime.now(),
                'verified': False
            }
            
            logger.info(f"Set up payment account for author {author_id}")
            return {
                'status': 'success',
                'author_id': author_id,
                'payment_method': payment_method,
                'setup_date': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Failed to setup author account: {e}")
            return {'error': str(e)}
    
    async def get_author_earnings(self, author_id: str, period_days: int = 30) -> Dict[str, Any]:
        """Get earnings summary for an author."""
        try:
            cutoff_date = datetime.now() - timedelta(days=period_days)
            
            total_earnings = 0.0
            total_paid = 0.0
            pending_earnings = 0.0
            strategy_earnings = {}
            
            # Calculate earnings from all strategies by author
            for strategy_id, shares in self.revenue_shares.items():
                for share in shares:
                    if (share.author_id == author_id and 
                        share.calculated_at >= cutoff_date):
                        
                        total_earnings += share.author_earnings
                        
                        if share.payment_status == PaymentStatus.COMPLETED:
                            total_paid += share.author_earnings
                        else:
                            pending_earnings += share.author_earnings
                        
                        if strategy_id not in strategy_earnings:
                            strategy_earnings[strategy_id] = 0.0
                        strategy_earnings[strategy_id] += share.author_earnings
            
            return {
                'author_id': author_id,
                'period_days': period_days,
                'total_earnings': total_earnings,
                'total_paid': total_paid,
                'pending_earnings': pending_earnings,
                'strategy_earnings': strategy_earnings,
                'account_setup': author_id in self.author_accounts,
                'calculated_at': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Failed to get author earnings: {e}")
            return {'error': str(e)}
    
    async def _process_payment(self, payment: Dict[str, Any]) -> Dict[str, Any]:
        """Process payment using specified method."""
        try:
            # TODO: Integrate with actual payment providers
            transaction_id = f"txn_{uuid.uuid4()}"
            
            # Simulate success
            return {
                'success': True,
                'transaction_id': transaction_id,
                'processed_at': datetime.now()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_revenue_sharing_summary(self) -> Dict[str, Any]:
        """Get revenue sharing system summary."""
        total_shares = sum(len(shares) for shares in self.revenue_shares.values())
        total_revenue = sum(share.total_revenue for shares in self.revenue_shares.values() for share in shares)
        total_author_earnings = sum(share.author_earnings for shares in self.revenue_shares.values() for share in shares)
        total_payments = sum(len(payments) for payments in self.payments.values())
        
        return {
            'total_revenue_shares': total_shares,
            'total_revenue': total_revenue,
            'total_author_earnings': total_author_earnings,
            'total_payments': total_payments,
            'authors_with_accounts': len(self.author_accounts)
        }