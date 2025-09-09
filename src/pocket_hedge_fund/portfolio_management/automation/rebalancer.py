"""
Portfolio Rebalancer - Automated Portfolio Rebalancing

This module provides automated portfolio rebalancing functionality including
rebalancing strategies, execution, and monitoring.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
import uuid

from ..models.portfolio_models import Portfolio, Position, AssetType
from ..models.transaction_models import RebalancePlan, RebalanceAction, Transaction, TransactionType, TransactionStatus

logger = logging.getLogger(__name__)


class PortfolioRebalancer:
    """Automated portfolio rebalancing functionality."""
    
    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        self.rebalancing_strategies = {
            'threshold_based': self._threshold_based_rebalancing,
            'time_based': self._time_based_rebalancing,
            'volatility_based': self._volatility_based_rebalancing,
            'risk_based': self._risk_based_rebalancing
        }
        
    async def create_rebalance_plan(
        self, 
        portfolio: Portfolio, 
        target_allocations: Dict[str, float],
        strategy: str = 'threshold_based',
        rebalance_threshold: float = 0.05
    ) -> RebalancePlan:
        """Create a rebalancing plan for the portfolio."""
        try:
            # Get current allocations
            current_allocations = portfolio.calculate_weight_percentages()
            
            # Calculate rebalancing needs
            rebalancing_actions = await self._calculate_rebalancing_actions(
                portfolio, current_allocations, target_allocations, rebalance_threshold
            )
            
            # Create rebalance plan
            plan_id = str(uuid.uuid4())
            plan = RebalancePlan(
                id=plan_id,
                portfolio_id=portfolio.id,
                target_allocations=target_allocations,
                current_allocations=current_allocations,
                rebalance_threshold=rebalance_threshold,
                actions=rebalancing_actions
            )
            
            # Calculate estimated costs
            plan.estimated_cost = await self._calculate_rebalance_cost(plan)
            plan.estimated_fees = await self._calculate_rebalance_fees(plan)
            
            # Save to database if available
            if self.db_manager:
                await self._save_rebalance_plan_to_db(plan)
            
            logger.info(f"Created rebalance plan {plan_id} for portfolio {portfolio.id}")
            return plan
            
        except Exception as e:
            logger.error(f"Failed to create rebalance plan: {e}")
            raise
    
    async def execute_rebalance_plan(self, plan: RebalancePlan) -> bool:
        """Execute a rebalancing plan."""
        try:
            # Validate plan
            if not await self._validate_rebalance_plan(plan):
                logger.error(f"Invalid rebalance plan {plan.id}")
                return False
            
            # Execute actions in order
            executed_actions = []
            failed_actions = []
            
            for action in plan.actions:
                try:
                    success = await self._execute_rebalance_action(action)
                    if success:
                        executed_actions.append(action)
                        action.status = 'executed'
                    else:
                        failed_actions.append(action)
                        action.status = 'failed'
                except Exception as e:
                    logger.error(f"Failed to execute action {action.id}: {e}")
                    failed_actions.append(action)
                    action.status = 'failed'
            
            # Update plan status
            if failed_actions:
                plan.status = 'partially_executed'
            else:
                plan.status = 'executed'
            
            plan.executed_at = datetime.utcnow()
            
            # Update database
            if self.db_manager:
                await self._update_rebalance_plan_in_db(plan)
            
            logger.info(f"Executed rebalance plan {plan.id}: {len(executed_actions)} actions executed, {len(failed_actions)} failed")
            return len(failed_actions) == 0
            
        except Exception as e:
            logger.error(f"Failed to execute rebalance plan: {e}")
            return False
    
    async def check_rebalancing_needs(
        self, 
        portfolio: Portfolio, 
        target_allocations: Dict[str, float],
        threshold: float = 0.05
    ) -> bool:
        """Check if portfolio needs rebalancing."""
        try:
            current_allocations = portfolio.calculate_weight_percentages()
            
            for asset_id, target_weight in target_allocations.items():
                current_weight = current_allocations.get(asset_id, 0)
                weight_diff = abs(target_weight - current_weight)
                
                if weight_diff > threshold:
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to check rebalancing needs: {e}")
            return False
    
    async def get_rebalancing_recommendations(
        self, 
        portfolio: Portfolio, 
        target_allocations: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Get rebalancing recommendations."""
        try:
            current_allocations = portfolio.calculate_weight_percentages()
            recommendations = []
            
            for asset_id, target_weight in target_allocations.items():
                current_weight = current_allocations.get(asset_id, 0)
                weight_diff = target_weight - current_weight
                
                if abs(weight_diff) > 0.01:  # 1% threshold
                    total_value = portfolio.calculate_total_value()
                    required_trade_value = total_value * (weight_diff / 100)
                    
                    recommendation = {
                        'asset_id': asset_id,
                        'current_weight': current_weight,
                        'target_weight': target_weight,
                        'weight_difference': weight_diff,
                        'required_trade_value': float(required_trade_value),
                        'action': 'buy' if weight_diff > 0 else 'sell',
                        'priority': self._calculate_action_priority(weight_diff, current_weight, target_weight)
                    }
                    
                    recommendations.append(recommendation)
            
            # Sort by priority
            recommendations.sort(key=lambda x: x['priority'], reverse=True)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to get rebalancing recommendations: {e}")
            return []
    
    async def optimize_rebalancing_order(self, actions: List[RebalanceAction]) -> List[RebalanceAction]:
        """Optimize the order of rebalancing actions."""
        try:
            # Sort actions by priority and estimated impact
            optimized_actions = sorted(actions, key=lambda x: (
                x.priority,
                abs(x.weight_difference),
                x.required_trade_amount
            ), reverse=True)
            
            # Update execution order
            for i, action in enumerate(optimized_actions):
                action.execution_order = i + 1
            
            return optimized_actions
            
        except Exception as e:
            logger.error(f"Failed to optimize rebalancing order: {e}")
            return actions
    
    async def calculate_rebalancing_impact(
        self, 
        plan: RebalancePlan
    ) -> Dict[str, Any]:
        """Calculate the impact of rebalancing."""
        try:
            # Calculate expected impact on portfolio metrics
            impact = {
                'expected_cost': float(plan.estimated_cost),
                'expected_fees': float(plan.estimated_fees),
                'expected_trades': len(plan.actions),
                'expected_risk_change': await self._calculate_risk_change(plan),
                'expected_return_change': await self._calculate_return_change(plan),
                'expected_volatility_change': await self._calculate_volatility_change(plan)
            }
            
            return impact
            
        except Exception as e:
            logger.error(f"Failed to calculate rebalancing impact: {e}")
            return {}
    
    # Rebalancing strategy methods
    async def _threshold_based_rebalancing(
        self, 
        portfolio: Portfolio, 
        target_allocations: Dict[str, float],
        threshold: float = 0.05
    ) -> List[RebalanceAction]:
        """Threshold-based rebalancing strategy."""
        try:
            current_allocations = portfolio.calculate_weight_percentages()
            actions = []
            
            for asset_id, target_weight in target_allocations.items():
                current_weight = current_allocations.get(asset_id, 0)
                weight_diff = target_weight - current_weight
                
                if abs(weight_diff) > threshold:
                    action = await self._create_rebalance_action(
                        portfolio, asset_id, current_weight, target_weight, weight_diff
                    )
                    actions.append(action)
            
            return actions
            
        except Exception as e:
            logger.error(f"Failed to execute threshold-based rebalancing: {e}")
            return []
    
    async def _time_based_rebalancing(
        self, 
        portfolio: Portfolio, 
        target_allocations: Dict[str, float],
        rebalance_frequency: int = 30
    ) -> List[RebalanceAction]:
        """Time-based rebalancing strategy."""
        try:
            # Check if enough time has passed since last rebalance
            if portfolio.last_rebalance:
                days_since_rebalance = (datetime.utcnow() - portfolio.last_rebalance).days
                if days_since_rebalance < rebalance_frequency:
                    return []
            
            # Execute threshold-based rebalancing with lower threshold
            return await self._threshold_based_rebalancing(portfolio, target_allocations, 0.02)
            
        except Exception as e:
            logger.error(f"Failed to execute time-based rebalancing: {e}")
            return []
    
    async def _volatility_based_rebalancing(
        self, 
        portfolio: Portfolio, 
        target_allocations: Dict[str, float],
        volatility_threshold: float = 0.20
    ) -> List[RebalanceAction]:
        """Volatility-based rebalancing strategy."""
        try:
            # Calculate portfolio volatility
            portfolio_volatility = await self._calculate_portfolio_volatility(portfolio)
            
            if portfolio_volatility > volatility_threshold:
                # Use higher threshold for volatile portfolios
                return await self._threshold_based_rebalancing(portfolio, target_allocations, 0.08)
            else:
                # Use normal threshold for stable portfolios
                return await self._threshold_based_rebalancing(portfolio, target_allocations, 0.05)
            
        except Exception as e:
            logger.error(f"Failed to execute volatility-based rebalancing: {e}")
            return []
    
    async def _risk_based_rebalancing(
        self, 
        portfolio: Portfolio, 
        target_allocations: Dict[str, float],
        risk_threshold: float = 0.15
    ) -> List[RebalanceAction]:
        """Risk-based rebalancing strategy."""
        try:
            # Calculate portfolio risk
            portfolio_risk = await self._calculate_portfolio_risk(portfolio)
            
            if portfolio_risk > risk_threshold:
                # Use higher threshold for high-risk portfolios
                return await self._threshold_based_rebalancing(portfolio, target_allocations, 0.10)
            else:
                # Use normal threshold for low-risk portfolios
                return await self._threshold_based_rebalancing(portfolio, target_allocations, 0.05)
            
        except Exception as e:
            logger.error(f"Failed to execute risk-based rebalancing: {e}")
            return []
    
    # Helper methods
    async def _calculate_rebalancing_actions(
        self, 
        portfolio: Portfolio, 
        current_allocations: Dict[str, float],
        target_allocations: Dict[str, float],
        threshold: float
    ) -> List[RebalanceAction]:
        """Calculate rebalancing actions."""
        try:
            actions = []
            
            for asset_id, target_weight in target_allocations.items():
                current_weight = current_allocations.get(asset_id, 0)
                weight_diff = target_weight - current_weight
                
                if abs(weight_diff) > threshold:
                    action = await self._create_rebalance_action(
                        portfolio, asset_id, current_weight, target_weight, weight_diff
                    )
                    actions.append(action)
            
            return actions
            
        except Exception as e:
            logger.error(f"Failed to calculate rebalancing actions: {e}")
            return []
    
    async def _create_rebalance_action(
        self, 
        portfolio: Portfolio, 
        asset_id: str, 
        current_weight: float, 
        target_weight: float, 
        weight_diff: float
    ) -> RebalanceAction:
        """Create a rebalancing action."""
        try:
            action_id = str(uuid.uuid4())
            total_value = portfolio.calculate_total_value()
            required_trade_amount = total_value * (weight_diff / 100)
            
            # Get current position
            position = portfolio.get_position_by_asset_id(asset_id)
            estimated_price = position.current_price if position else Decimal('0')
            trade_quantity = required_trade_amount / estimated_price if estimated_price > 0 else Decimal('0')
            
            action = RebalanceAction(
                id=action_id,
                portfolio_id=portfolio.id,
                rebalance_id=portfolio.id,  # This would be the plan ID
                asset_id=asset_id,
                action_type='buy' if weight_diff > 0 else 'sell',
                current_weight=current_weight,
                target_weight=target_weight,
                weight_difference=weight_diff,
                required_trade_amount=required_trade_amount,
                trade_quantity=trade_quantity,
                estimated_price=estimated_price,
                estimated_fees=Decimal('0'),  # Would be calculated based on broker
                priority=self._calculate_action_priority(weight_diff, current_weight, target_weight)
            )
            
            return action
            
        except Exception as e:
            logger.error(f"Failed to create rebalance action: {e}")
            raise
    
    def _calculate_action_priority(self, weight_diff: float, current_weight: float, target_weight: float) -> int:
        """Calculate action priority."""
        try:
            # Higher priority for larger deviations
            priority = int(abs(weight_diff) * 100)
            
            # Increase priority for actions that reduce concentration
            if current_weight > target_weight and current_weight > 0.2:  # Reducing large positions
                priority += 20
            
            # Increase priority for actions that increase diversification
            if weight_diff > 0 and target_weight < 0.1:  # Adding small positions
                priority += 10
            
            return min(priority, 100)  # Cap at 100
            
        except Exception as e:
            logger.error(f"Failed to calculate action priority: {e}")
            return 1
    
    async def _calculate_rebalance_cost(self, plan: RebalancePlan) -> Decimal:
        """Calculate rebalancing cost."""
        try:
            total_cost = Decimal('0')
            
            for action in plan.actions:
                total_cost += action.required_trade_amount
            
            return total_cost
            
        except Exception as e:
            logger.error(f"Failed to calculate rebalance cost: {e}")
            return Decimal('0')
    
    async def _calculate_rebalance_fees(self, plan: RebalancePlan) -> Decimal:
        """Calculate rebalancing fees."""
        try:
            total_fees = Decimal('0')
            
            for action in plan.actions:
                total_fees += action.estimated_fees
            
            return total_fees
            
        except Exception as e:
            logger.error(f"Failed to calculate rebalance fees: {e}")
            return Decimal('0')
    
    async def _validate_rebalance_plan(self, plan: RebalancePlan) -> bool:
        """Validate rebalancing plan."""
        try:
            # Check if plan has actions
            if not plan.actions:
                return False
            
            # Check if actions are valid
            for action in plan.actions:
                if not action.asset_id or action.required_trade_amount <= 0:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate rebalance plan: {e}")
            return False
    
    async def _execute_rebalance_action(self, action: RebalanceAction) -> bool:
        """Execute a rebalancing action."""
        try:
            # This would execute the actual trade
            # For now, just simulate success
            
            # Create transaction record
            transaction = Transaction(
                id=str(uuid.uuid4()),
                portfolio_id=action.portfolio_id,
                transaction_type=TransactionType.BUY if action.action_type == 'buy' else TransactionType.SELL,
                asset_id=action.asset_id,
                quantity=action.trade_quantity,
                price=action.estimated_price,
                total_amount=action.required_trade_amount,
                fees=action.estimated_fees,
                net_amount=action.required_trade_amount - action.estimated_fees,
                status=TransactionStatus.EXECUTED,
                execution_date=datetime.utcnow()
            )
            
            # Save transaction to database
            if self.db_manager:
                await self._save_transaction_to_db(transaction)
            
            logger.info(f"Executed rebalance action {action.id}: {action.action_type} {action.trade_quantity} of {action.asset_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to execute rebalance action {action.id}: {e}")
            return False
    
    # Placeholder methods for complex calculations
    async def _calculate_risk_change(self, plan: RebalancePlan) -> float:
        """Calculate expected risk change."""
        return 0.0
    
    async def _calculate_return_change(self, plan: RebalancePlan) -> float:
        """Calculate expected return change."""
        return 0.0
    
    async def _calculate_volatility_change(self, plan: RebalancePlan) -> float:
        """Calculate expected volatility change."""
        return 0.0
    
    async def _calculate_portfolio_volatility(self, portfolio: Portfolio) -> float:
        """Calculate portfolio volatility."""
        return 0.0
    
    async def _calculate_portfolio_risk(self, portfolio: Portfolio) -> float:
        """Calculate portfolio risk."""
        return 0.0
    
    # Database helper methods
    async def _save_rebalance_plan_to_db(self, plan: RebalancePlan):
        """Save rebalance plan to database."""
        if not self.db_manager:
            return
        
        # This would save the plan to the database
        pass
    
    async def _update_rebalance_plan_in_db(self, plan: RebalancePlan):
        """Update rebalance plan in database."""
        if not self.db_manager:
            return
        
        # This would update the plan in the database
        pass
    
    async def _save_transaction_to_db(self, transaction: Transaction):
        """Save transaction to database."""
        if not self.db_manager:
            return
        
        # This would save the transaction to the database
        pass
