"""Licensing System - Strategy licensing and revenue management"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class LicenseType(Enum):
    """License type enumeration."""
    FREE = "free"
    PREMIUM = "premium"
    EXCLUSIVE = "exclusive"


class LicenseStatus(Enum):
    """License status enumeration."""
    ACTIVE = "active"
    EXPIRED = "expired"
    SUSPENDED = "suspended"


class PaymentStatus(Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class License:
    """License data class."""
    license_id: str
    strategy_id: str
    user_id: str
    license_type: LicenseType
    status: LicenseStatus
    price: float
    payment_status: PaymentStatus
    start_date: datetime
    end_date: Optional[datetime]
    usage_limit: Optional[int]
    current_usage: int
    created_at: datetime
    updated_at: datetime


class LicensingSystem:
    """Strategy licensing and revenue management system."""
    
    def __init__(self):
        self.licenses: Dict[str, License] = {}
        self.revenue_shares: Dict[str, List[Dict[str, Any]]] = {}
        self.license_templates: Dict[LicenseType, Dict[str, Any]] = {
            LicenseType.FREE: {'price': 0.0, 'duration_days': None, 'usage_limit': None},
            LicenseType.PREMIUM: {'price': 99.0, 'duration_days': 365, 'usage_limit': 1000},
            LicenseType.EXCLUSIVE: {'price': 999.0, 'duration_days': 365, 'usage_limit': None}
        }
        self.platform_commission = 0.30  # 30% platform commission
        
    async def create_license(self, strategy_id: str, user_id: str, 
                           license_type: LicenseType, custom_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new license for a strategy."""
        try:
            license_id = str(uuid.uuid4())
            
            # Get license template
            template = self.license_templates[license_type]
            
            # Calculate license parameters
            price = custom_params.get('price', template['price']) if custom_params else template['price']
            duration_days = custom_params.get('duration_days', template['duration_days']) if custom_params else template['duration_days']
            usage_limit = custom_params.get('usage_limit', template['usage_limit']) if custom_params else template['usage_limit']
            
            # Calculate end date
            end_date = None
            if duration_days:
                end_date = datetime.now() + timedelta(days=duration_days)
            
            # Create license
            license_obj = License(
                license_id=license_id,
                strategy_id=strategy_id,
                user_id=user_id,
                license_type=license_type,
                status=LicenseStatus.ACTIVE,
                price=price,
                payment_status=PaymentStatus.PENDING if price > 0 else PaymentStatus.COMPLETED,
                start_date=datetime.now(),
                end_date=end_date,
                usage_limit=usage_limit,
                current_usage=0,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            self.licenses[license_id] = license_obj
            
            logger.info(f"Created license {license_id} for strategy {strategy_id}")
            return {
                'status': 'success',
                'license_id': license_id,
                'license': license_obj.__dict__,
                'payment_required': price > 0
            }
            
        except Exception as e:
            logger.error(f"Failed to create license: {e}")
            return {'error': str(e)}
    
    async def validate_license(self, strategy_id: str, user_id: str) -> Dict[str, Any]:
        """Validate if user has valid license for strategy."""
        try:
            # Find active licenses for user and strategy
            valid_licenses = []
            
            for license_obj in self.licenses.values():
                if (license_obj.strategy_id == strategy_id and 
                    license_obj.user_id == user_id and 
                    license_obj.status == LicenseStatus.ACTIVE and
                    license_obj.payment_status == PaymentStatus.COMPLETED):
                    
                    # Check if license is not expired
                    if license_obj.end_date is None or license_obj.end_date > datetime.now():
                        # Check usage limit
                        if license_obj.usage_limit is None or license_obj.current_usage < license_obj.usage_limit:
                            valid_licenses.append(license_obj)
            
            if valid_licenses:
                # Use the most permissive license
                best_license = max(valid_licenses, key=lambda x: x.license_type.value)
                
                # Increment usage
                best_license.current_usage += 1
                best_license.updated_at = datetime.now()
                
                return {
                    'valid': True,
                    'license_id': best_license.license_id,
                    'license_type': best_license.license_type.value,
                    'usage_remaining': (best_license.usage_limit - best_license.current_usage) if best_license.usage_limit else None
                }
            else:
                return {
                    'valid': False,
                    'reason': 'No valid license found'
                }
                
        except Exception as e:
            logger.error(f"Failed to validate license: {e}")
            return {'error': str(e)}
    
    async def get_user_licenses(self, user_id: str) -> Dict[str, Any]:
        """Get all licenses for a user."""
        try:
            user_licenses = []
            
            for license_obj in self.licenses.values():
                if license_obj.user_id == user_id:
                    user_licenses.append(license_obj.__dict__)
            
            # Sort by creation date (newest first)
            user_licenses.sort(key=lambda x: x['created_at'], reverse=True)
            
            return {
                'user_id': user_id,
                'licenses': user_licenses,
                'total_count': len(user_licenses)
            }
            
        except Exception as e:
            logger.error(f"Failed to get user licenses: {e}")
            return {'error': str(e)}
    
    async def calculate_revenue_share(self, strategy_id: str, 
                                    period_start: datetime, 
                                    period_end: datetime) -> Dict[str, Any]:
        """Calculate revenue share for a strategy in a period."""
        try:
            # Get all licenses for strategy in period
            period_licenses = []
            for license_obj in self.licenses.values():
                if (license_obj.strategy_id == strategy_id and
                    license_obj.created_at >= period_start and
                    license_obj.created_at <= period_end and
                    license_obj.payment_status == PaymentStatus.COMPLETED):
                    period_licenses.append(license_obj)
            
            # Calculate total revenue
            total_revenue = sum(license_obj.price for license_obj in period_licenses)
            
            # Calculate shares
            platform_earnings = total_revenue * self.platform_commission
            author_earnings = total_revenue * (1 - self.platform_commission)
            
            # Create revenue share record
            share_id = str(uuid.uuid4())
            revenue_share = {
                'share_id': share_id,
                'strategy_id': strategy_id,
                'author_id': '',  # TODO: Get from strategy data
                'platform_share': self.platform_commission,
                'author_share': 1 - self.platform_commission,
                'total_revenue': total_revenue,
                'author_earnings': author_earnings,
                'platform_earnings': platform_earnings,
                'period_start': period_start,
                'period_end': period_end,
                'calculated_at': datetime.now()
            }
            
            # Store revenue share
            if strategy_id not in self.revenue_shares:
                self.revenue_shares[strategy_id] = []
            self.revenue_shares[strategy_id].append(revenue_share)
            
            logger.info(f"Calculated revenue share for strategy {strategy_id}: {total_revenue}")
            return {
                'strategy_id': strategy_id,
                'period_start': period_start,
                'period_end': period_end,
                'total_revenue': total_revenue,
                'author_earnings': author_earnings,
                'platform_earnings': platform_earnings,
                'license_count': len(period_licenses),
                'revenue_share': revenue_share
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate revenue share: {e}")
            return {'error': str(e)}
    
    def get_licensing_summary(self) -> Dict[str, Any]:
        """Get licensing system summary."""
        total_licenses = len(self.licenses)
        active_licenses = len([l for l in self.licenses.values() if l.status == LicenseStatus.ACTIVE])
        total_revenue = sum(l.price for l in self.licenses.values() if l.payment_status == PaymentStatus.COMPLETED)
        
        # License type distribution
        type_distribution = {}
        for license_obj in self.licenses.values():
            license_type = license_obj.license_type.value
            type_distribution[license_type] = type_distribution.get(license_type, 0) + 1
        
        return {
            'total_licenses': total_licenses,
            'active_licenses': active_licenses,
            'total_revenue': total_revenue,
            'type_distribution': type_distribution,
            'platform_commission': self.platform_commission
        }