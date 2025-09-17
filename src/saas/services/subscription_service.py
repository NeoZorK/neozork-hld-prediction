"""
Subscription Service for SaaS Platform

This service handles subscription management including creation, updates,
billing cycles, and feature access control.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import uuid

from ..models.subscription import Subscription, SubscriptionStatus, SubscriptionTier
from ..models.plan import Plan

logger = logging.getLogger(__name__)


class SubscriptionService:
    """
    Service for managing subscriptions in the SaaS platform.
    
    This service provides:
    - Subscription creation and management
    - Billing cycle management
    - Feature access control
    - Usage tracking and limits
    - Subscription lifecycle management
    """
    
    def __init__(self):
        self.subscriptions: Dict[str, Subscription] = {}
        self.tenant_subscriptions: Dict[str, str] = {}  # tenant_id -> subscription_id
    
    async def create_subscription(self, tenant_id: str, plan: Plan, 
                                 billing_cycle: str = "monthly",
                                 trial_days: int = 0) -> Dict[str, Any]:
        """
        Create a new subscription for a tenant.
        
        Args:
            tenant_id: Tenant ID
            plan: Plan object
            billing_cycle: Billing cycle (monthly, annual, quarterly)
            trial_days: Number of trial days
            
        Returns:
            Dict containing subscription information and status
        """
        try:
            # Check if tenant already has an active subscription
            if tenant_id in self.tenant_subscriptions:
                existing_subscription_id = self.tenant_subscriptions[tenant_id]
                existing_subscription = self.subscriptions.get(existing_subscription_id)
                if existing_subscription and existing_subscription.is_active():
                    return {
                        "status": "error",
                        "message": "Tenant already has an active subscription"
                    }
            
            # Create subscription
            subscription = Subscription(
                tenant_id=tenant_id,
                plan_id=plan.plan_id,
                tier=SubscriptionTier(plan.plan_type.value),
                status=SubscriptionStatus.TRIALING if trial_days > 0 else SubscriptionStatus.ACTIVE,
                monthly_price=plan.monthly_price,
                annual_price=plan.annual_price,
                currency=plan.currency,
                billing_cycle=billing_cycle,
                features=plan.features.copy(),
                limits=plan.limits.copy()
            )
            
            # Set trial period
            if trial_days > 0:
                subscription.trial_start = datetime.now(datetime.UTC)
                subscription.trial_end = datetime.now(datetime.UTC) + timedelta(days=trial_days)
            
            # Set billing period
            self._set_billing_period(subscription)
            
            # Store subscription
            self.subscriptions[subscription.subscription_id] = subscription
            self.tenant_subscriptions[tenant_id] = subscription.subscription_id
            
            logger.info(f"Created subscription: {subscription.subscription_id} for tenant: {tenant_id}")
            
            return {
                "status": "success",
                "subscription": subscription.to_dict(),
                "message": "Subscription created successfully"
            }
            
        except Exception as e:
            logger.error(f"Error creating subscription: {e}")
            return {
                "status": "error",
                "message": f"Failed to create subscription: {str(e)}"
            }
    
    async def get_subscription(self, subscription_id: str) -> Optional[Subscription]:
        """Get subscription by ID."""
        return self.subscriptions.get(subscription_id)
    
    async def get_tenant_subscription(self, tenant_id: str) -> Optional[Subscription]:
        """Get subscription for a tenant."""
        subscription_id = self.tenant_subscriptions.get(tenant_id)
        if subscription_id:
            return self.subscriptions.get(subscription_id)
        return None
    
    async def update_subscription(self, subscription_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update subscription information.
        
        Args:
            subscription_id: Subscription ID
            updates: Dictionary of fields to update
            
        Returns:
            Dict containing update status
        """
        try:
            subscription = self.subscriptions.get(subscription_id)
            if not subscription:
                return {
                    "status": "error",
                    "message": "Subscription not found"
                }
            
            # Update allowed fields
            allowed_fields = [
                "monthly_price", "annual_price", "currency", "billing_cycle",
                "features", "limits", "payment_method_id", "billing_email",
                "auto_renew", "custom_pricing", "discount_percentage"
            ]
            
            for field, value in updates.items():
                if field in allowed_fields and hasattr(subscription, field):
                    setattr(subscription, field, value)
            
            subscription.updated_at = datetime.now(datetime.UTC)
            
            logger.info(f"Updated subscription: {subscription_id}")
            
            return {
                "status": "success",
                "subscription": subscription.to_dict(),
                "message": "Subscription updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error updating subscription: {e}")
            return {
                "status": "error",
                "message": f"Failed to update subscription: {str(e)}"
            }
    
    async def upgrade_subscription(self, subscription_id: str, new_plan: Plan) -> Dict[str, Any]:
        """Upgrade subscription to a new plan."""
        try:
            subscription = self.subscriptions.get(subscription_id)
            if not subscription:
                return {
                    "status": "error",
                    "message": "Subscription not found"
                }
            
            # Update subscription with new plan details
            subscription.plan_id = new_plan.plan_id
            subscription.tier = SubscriptionTier(new_plan.plan_type.value)
            subscription.monthly_price = new_plan.monthly_price
            subscription.annual_price = new_plan.annual_price
            subscription.features = new_plan.features.copy()
            subscription.limits = new_plan.limits.copy()
            subscription.updated_at = datetime.now(datetime.UTC)
            
            logger.info(f"Upgraded subscription: {subscription_id} to plan: {new_plan.plan_id}")
            
            return {
                "status": "success",
                "subscription": subscription.to_dict(),
                "message": "Subscription upgraded successfully"
            }
            
        except Exception as e:
            logger.error(f"Error upgrading subscription: {e}")
            return {
                "status": "error",
                "message": f"Failed to upgrade subscription: {str(e)}"
            }
    
    async def cancel_subscription(self, subscription_id: str, effective_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Cancel a subscription."""
        try:
            subscription = self.subscriptions.get(subscription_id)
            if not subscription:
                return {
                    "status": "error",
                    "message": "Subscription not found"
                }
            
            subscription.cancel(effective_date)
            
            logger.info(f"Cancelled subscription: {subscription_id}")
            
            return {
                "status": "success",
                "message": "Subscription cancelled successfully"
            }
            
        except Exception as e:
            logger.error(f"Error cancelling subscription: {e}")
            return {
                "status": "error",
                "message": f"Failed to cancel subscription: {str(e)}"
            }
    
    async def reactivate_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Reactivate a cancelled subscription."""
        try:
            subscription = self.subscriptions.get(subscription_id)
            if not subscription:
                return {
                    "status": "error",
                    "message": "Subscription not found"
                }
            
            subscription.reactivate()
            
            logger.info(f"Reactivated subscription: {subscription_id}")
            
            return {
                "status": "success",
                "message": "Subscription reactivated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error reactivating subscription: {e}")
            return {
                "status": "error",
                "message": f"Failed to reactivate subscription: {str(e)}"
            }
    
    async def process_billing_cycle(self, subscription_id: str) -> Dict[str, Any]:
        """Process billing cycle for a subscription."""
        try:
            subscription = self.subscriptions.get(subscription_id)
            if not subscription:
                return {
                    "status": "error",
                    "message": "Subscription not found"
                }
            
            # Check if billing cycle needs to be processed
            if datetime.now(datetime.UTC) < subscription.current_period_end:
                return {
                    "status": "success",
                    "message": "Billing cycle not yet due"
                }
            
            # Reset usage for new period
            subscription.reset_period_usage()
            
            logger.info(f"Processed billing cycle for subscription: {subscription_id}")
            
            return {
                "status": "success",
                "subscription": subscription.to_dict(),
                "message": "Billing cycle processed successfully"
            }
            
        except Exception as e:
            logger.error(f"Error processing billing cycle: {e}")
            return {
                "status": "error",
                "message": f"Failed to process billing cycle: {str(e)}"
            }
    
    async def check_feature_access(self, subscription_id: str, feature_name: str) -> bool:
        """Check if subscription has access to a feature."""
        try:
            subscription = self.subscriptions.get(subscription_id)
            if not subscription:
                return False
            
            return subscription.has_feature(feature_name)
            
        except Exception as e:
            logger.error(f"Error checking feature access: {e}")
            return False
    
    async def check_usage_limit(self, subscription_id: str, limit_type: str, current_usage: int) -> bool:
        """Check if current usage is within subscription limits."""
        try:
            subscription = self.subscriptions.get(subscription_id)
            if not subscription:
                return False
            
            return subscription.is_within_limit(limit_type, current_usage)
            
        except Exception as e:
            logger.error(f"Error checking usage limit: {e}")
            return False
    
    async def update_usage(self, subscription_id: str, usage_type: str, amount: int) -> Dict[str, Any]:
        """Update usage for a subscription."""
        try:
            subscription = self.subscriptions.get(subscription_id)
            if not subscription:
                return {
                    "status": "error",
                    "message": "Subscription not found"
                }
            
            subscription.update_usage(usage_type, amount)
            
            return {
                "status": "success",
                "message": "Usage updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error updating usage: {e}")
            return {
                "status": "error",
                "message": f"Failed to update usage: {str(e)}"
            }
    
    async def add_feature(self, subscription_id: str, feature_name: str) -> Dict[str, Any]:
        """Add a feature to a subscription."""
        try:
            subscription = self.subscriptions.get(subscription_id)
            if not subscription:
                return {
                    "status": "error",
                    "message": "Subscription not found"
                }
            
            subscription.add_feature(feature_name)
            
            return {
                "status": "success",
                "message": "Feature added successfully"
            }
            
        except Exception as e:
            logger.error(f"Error adding feature: {e}")
            return {
                "status": "error",
                "message": f"Failed to add feature: {str(e)}"
            }
    
    async def remove_feature(self, subscription_id: str, feature_name: str) -> Dict[str, Any]:
        """Remove a feature from a subscription."""
        try:
            subscription = self.subscriptions.get(subscription_id)
            if not subscription:
                return {
                    "status": "error",
                    "message": "Subscription not found"
                }
            
            subscription.remove_feature(feature_name)
            
            return {
                "status": "success",
                "message": "Feature removed successfully"
            }
            
        except Exception as e:
            logger.error(f"Error removing feature: {e}")
            return {
                "status": "error",
                "message": f"Failed to remove feature: {str(e)}"
            }
    
    async def get_subscription_analytics(self, subscription_id: str) -> Dict[str, Any]:
        """Get subscription analytics and insights."""
        try:
            subscription = self.subscriptions.get(subscription_id)
            if not subscription:
                return {
                    "status": "error",
                    "message": "Subscription not found"
                }
            
            analytics = {
                "subscription_info": {
                    "subscription_id": subscription.subscription_id,
                    "tenant_id": subscription.tenant_id,
                    "tier": subscription.tier.value,
                    "status": subscription.status.value,
                    "billing_cycle": subscription.billing_cycle,
                    "created_at": subscription.created_at.isoformat()
                },
                "pricing_info": {
                    "monthly_price": subscription.monthly_price,
                    "annual_price": subscription.annual_price,
                    "currency": subscription.currency,
                    "effective_price": subscription.get_effective_price(),
                    "total_price": subscription.get_total_price()
                },
                "usage_info": {
                    "usage_this_period": subscription.usage_this_period,
                    "limits": subscription.limits
                },
                "features": subscription.features,
                "trial_info": {
                    "is_trial": subscription.is_trial(),
                    "trial_days_remaining": subscription.get_trial_days_remaining(),
                    "trial_end": subscription.trial_end.isoformat() if subscription.trial_end else None
                },
                "billing_info": {
                    "current_period_start": subscription.current_period_start.isoformat(),
                    "current_period_end": subscription.current_period_end.isoformat(),
                    "next_billing_date": subscription.get_next_billing_date().isoformat(),
                    "days_until_renewal": subscription.get_days_until_renewal()
                }
            }
            
            return {
                "status": "success",
                "analytics": analytics
            }
            
        except Exception as e:
            logger.error(f"Error getting subscription analytics: {e}")
            return {
                "status": "error",
                "message": f"Failed to get subscription analytics: {str(e)}"
            }
    
    async def list_subscriptions(self, status: Optional[SubscriptionStatus] = None,
                                tier: Optional[SubscriptionTier] = None,
                                limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """List subscriptions with optional filtering."""
        try:
            subscriptions = list(self.subscriptions.values())
            
            # Apply filters
            if status:
                subscriptions = [s for s in subscriptions if s.status == status]
            if tier:
                subscriptions = [s for s in subscriptions if s.tier == tier]
            
            # Sort by created_at (newest first)
            subscriptions.sort(key=lambda s: s.created_at, reverse=True)
            
            # Apply pagination
            total_count = len(subscriptions)
            subscriptions = subscriptions[offset:offset + limit]
            
            return {
                "status": "success",
                "subscriptions": [subscription.to_dict() for subscription in subscriptions],
                "total_count": total_count,
                "limit": limit,
                "offset": offset
            }
            
        except Exception as e:
            logger.error(f"Error listing subscriptions: {e}")
            return {
                "status": "error",
                "message": f"Failed to list subscriptions: {str(e)}"
            }
    
    def _set_billing_period(self, subscription: Subscription) -> None:
        """Set billing period based on billing cycle."""
        now = datetime.now(datetime.UTC)
        subscription.current_period_start = now
        
        if subscription.billing_cycle == "annual":
            subscription.current_period_end = now + timedelta(days=365)
        elif subscription.billing_cycle == "quarterly":
            subscription.current_period_end = now + timedelta(days=90)
        else:  # monthly
            subscription.current_period_end = now + timedelta(days=30)
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """Get system-wide subscription statistics."""
        try:
            total_subscriptions = len(self.subscriptions)
            active_subscriptions = len([s for s in self.subscriptions.values() if s.is_active()])
            trial_subscriptions = len([s for s in self.subscriptions.values() if s.is_trial()])
            cancelled_subscriptions = len([s for s in self.subscriptions.values() if s.is_cancelled()])
            
            # Tier distribution
            tier_distribution = {}
            for subscription in self.subscriptions.values():
                tier = subscription.tier.value
                tier_distribution[tier] = tier_distribution.get(tier, 0) + 1
            
            # Billing cycle distribution
            billing_cycle_distribution = {}
            for subscription in self.subscriptions.values():
                cycle = subscription.billing_cycle
                billing_cycle_distribution[cycle] = billing_cycle_distribution.get(cycle, 0) + 1
            
            return {
                "status": "success",
                "stats": {
                    "total_subscriptions": total_subscriptions,
                    "active_subscriptions": active_subscriptions,
                    "trial_subscriptions": trial_subscriptions,
                    "cancelled_subscriptions": cancelled_subscriptions,
                    "tier_distribution": tier_distribution,
                    "billing_cycle_distribution": billing_cycle_distribution
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {
                "status": "error",
                "message": f"Failed to get system stats: {str(e)}"
            }
