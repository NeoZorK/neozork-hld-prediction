"""
Return Calculation Service for Pocket Hedge Fund

This module provides real-time return calculation functionality
including portfolio performance tracking, risk metrics, and analytics.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from decimal import Decimal
import math

from ..database.connection import get_db_manager

# Configure logging
logger = logging.getLogger(__name__)

class ReturnCalculator:
    """Service for calculating investment returns and performance metrics."""
    
    def __init__(self):
        self.db_manager = None
    
    async def initialize(self):
        """Initialize the return calculator."""
        self.db_manager = await get_db_manager()
    
    async def calculate_investment_return(self, investment_id: str) -> Dict[str, Any]:
        """Calculate real-time return for a specific investment."""
        try:
            # Get investment details with fund information
            query = """
                SELECT i.*, f.name as fund_name, f.current_value as fund_current_value, 
                       f.initial_capital, f.created_at as fund_created_at
                FROM investments i
                JOIN funds f ON i.fund_id = f.id
                WHERE i.id = $1
            """
            investments = await self.db_manager.execute_query(query, {'1': investment_id})
            
            if not investments:
                return {"error": "Investment not found"}
            
            investment = investments[0]
            
            # Calculate current value based on fund performance
            fund_share_price = float(investment['fund_current_value']) / float(investment['initial_capital']) if investment['initial_capital'] > 0 else 1.0
            current_value = float(investment['shares_acquired']) * fund_share_price
            
            # Calculate returns
            total_return = current_value - float(investment['amount'])
            total_return_percentage = (total_return / float(investment['amount']) * 100) if investment['amount'] > 0 else 0.0
            
            # Calculate time-based returns
            investment_date = investment['created_at']
            days_held = (datetime.utcnow() - investment_date).days
            annualized_return = self._calculate_annualized_return(
                float(investment['amount']), current_value, days_held
            )
            
            return {
                "investment_id": investment_id,
                "fund_name": investment['fund_name'],
                "invested_amount": float(investment['amount']),
                "current_value": current_value,
                "total_return": total_return,
                "total_return_percentage": total_return_percentage,
                "annualized_return": annualized_return,
                "days_held": days_held,
                "shares_owned": float(investment['shares_acquired']),
                "current_share_price": fund_share_price,
                "original_share_price": float(investment['share_price']),
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate investment return: {e}")
            return {"error": str(e)}
    
    async def calculate_portfolio_return(self, investor_id: str) -> Dict[str, Any]:
        """Calculate real-time return for entire portfolio."""
        try:
            # Get all active investments
            query = """
                SELECT i.*, f.name as fund_name, f.fund_type, f.current_value as fund_current_value, 
                       f.initial_capital, f.created_at as fund_created_at
                FROM investments i
                JOIN funds f ON i.fund_id = f.id
                WHERE i.investor_id = $1 AND i.status = 'active'
            """
            investments = await self.db_manager.execute_query(query, {'1': investor_id})
            
            if not investments:
                return {
                    "investor_id": investor_id,
                    "total_invested": 0.0,
                    "total_current_value": 0.0,
                    "total_return": 0.0,
                    "total_return_percentage": 0.0,
                    "investments": [],
                    "last_updated": datetime.utcnow().isoformat()
                }
            
            # Calculate portfolio metrics
            total_invested = sum(float(inv['amount']) for inv in investments)
            total_current_value = 0.0
            investment_returns = []
            
            for inv in investments:
                fund_share_price = float(inv['fund_current_value']) / float(inv['initial_capital']) if inv['initial_capital'] > 0 else 1.0
                current_value = float(inv['shares_acquired']) * fund_share_price
                total_current_value += current_value
                
                investment_return = current_value - float(inv['amount'])
                investment_return_percentage = (investment_return / float(inv['amount']) * 100) if inv['amount'] > 0 else 0.0
                
                investment_returns.append({
                    "investment_id": str(inv['id']),
                    "fund_name": inv['fund_name'],
                    "fund_type": inv['fund_type'],
                    "invested_amount": float(inv['amount']),
                    "current_value": current_value,
                    "return_amount": investment_return,
                    "return_percentage": investment_return_percentage,
                    "shares_owned": float(inv['shares_acquired']),
                    "current_share_price": fund_share_price
                })
            
            total_return = total_current_value - total_invested
            total_return_percentage = (total_return / total_invested * 100) if total_invested > 0 else 0.0
            
            return {
                "investor_id": investor_id,
                "total_invested": total_invested,
                "total_current_value": total_current_value,
                "total_return": total_return,
                "total_return_percentage": total_return_percentage,
                "investments": investment_returns,
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate portfolio return: {e}")
            return {"error": str(e)}
    
    async def calculate_fund_performance(self, fund_id: str) -> Dict[str, Any]:
        """Calculate performance metrics for a specific fund."""
        try:
            # Get fund details
            fund_query = """
                SELECT * FROM funds WHERE id = $1
            """
            funds = await self.db_manager.execute_query(fund_query, {'1': fund_id})
            
            if not funds:
                return {"error": "Fund not found"}
            
            fund = funds[0]
            
            # Calculate fund performance
            total_return = float(fund['current_value']) - float(fund['initial_capital'])
            total_return_percentage = (total_return / float(fund['initial_capital']) * 100) if fund['initial_capital'] > 0 else 0.0
            
            # Calculate time-based metrics
            fund_created = fund['created_at']
            days_active = (datetime.utcnow() - fund_created).days
            annualized_return = self._calculate_annualized_return(
                float(fund['initial_capital']), float(fund['current_value']), days_active
            )
            
            # Get investor count and total investments
            investor_query = """
                SELECT COUNT(*) as investor_count, SUM(amount) as total_investments
                FROM investments WHERE fund_id = $1 AND status = 'active'
            """
            investor_data = await self.db_manager.execute_query(investor_query, {'1': fund_id})
            investor_count = investor_data[0]['investor_count'] if investor_data else 0
            total_investments = float(investor_data[0]['total_investments']) if investor_data and investor_data[0]['total_investments'] else 0.0
            
            return {
                "fund_id": fund_id,
                "fund_name": fund['name'],
                "fund_type": fund['fund_type'],
                "initial_capital": float(fund['initial_capital']),
                "current_value": float(fund['current_value']),
                "total_return": total_return,
                "total_return_percentage": total_return_percentage,
                "annualized_return": annualized_return,
                "days_active": days_active,
                "investor_count": investor_count,
                "total_investments": total_investments,
                "management_fee": float(fund['management_fee']),
                "performance_fee": float(fund['performance_fee']),
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate fund performance: {e}")
            return {"error": str(e)}
    
    async def calculate_risk_metrics(self, investor_id: str) -> Dict[str, Any]:
        """Calculate risk metrics for investor's portfolio."""
        try:
            # Get portfolio data
            portfolio_data = await self.calculate_portfolio_return(investor_id)
            
            if "error" in portfolio_data:
                return portfolio_data
            
            # Calculate basic risk metrics
            total_invested = portfolio_data['total_invested']
            total_current_value = portfolio_data['total_current_value']
            
            if total_invested == 0:
                return {
                    "investor_id": investor_id,
                    "risk_metrics": {
                        "volatility": 0.0,
                        "sharpe_ratio": 0.0,
                        "max_drawdown": 0.0,
                        "var_95": 0.0,
                        "beta": 1.0,
                        "diversification_ratio": 0.0
                    },
                    "last_updated": datetime.utcnow().isoformat()
                }
            
            # Calculate volatility (simplified - would need historical data in real implementation)
            volatility = self._calculate_volatility(portfolio_data['investments'])
            
            # Calculate Sharpe ratio (simplified)
            risk_free_rate = 0.02  # 2% risk-free rate
            excess_return = portfolio_data['total_return_percentage'] / 100 - risk_free_rate
            sharpe_ratio = excess_return / volatility if volatility > 0 else 0.0
            
            # Calculate diversification ratio
            diversification_ratio = self._calculate_diversification_ratio(portfolio_data['investments'])
            
            # Calculate concentration risk
            concentration_risk = self._calculate_concentration_risk(portfolio_data['investments'])
            
            return {
                "investor_id": investor_id,
                "risk_metrics": {
                    "volatility": volatility,
                    "sharpe_ratio": sharpe_ratio,
                    "max_drawdown": 0.0,  # Would need historical data
                    "var_95": 0.0,  # Would need historical data
                    "beta": 1.0,  # Would need market data
                    "diversification_ratio": diversification_ratio,
                    "concentration_risk": concentration_risk
                },
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate risk metrics: {e}")
            return {"error": str(e)}
    
    def _calculate_annualized_return(self, initial_value: float, current_value: float, days: int) -> float:
        """Calculate annualized return percentage."""
        if days <= 0 or initial_value <= 0:
            return 0.0
        
        years = days / 365.25
        if years <= 0:
            return 0.0
        
        return ((current_value / initial_value) ** (1 / years) - 1) * 100
    
    def _calculate_volatility(self, investments: List[Dict[str, Any]]) -> float:
        """Calculate portfolio volatility (simplified)."""
        if not investments:
            return 0.0
        
        # Simple volatility calculation based on return percentages
        returns = [inv['return_percentage'] for inv in investments]
        if len(returns) < 2:
            return 0.15  # Default volatility
        
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        return math.sqrt(variance) / 100  # Convert to decimal
    
    def _calculate_diversification_ratio(self, investments: List[Dict[str, Any]]) -> float:
        """Calculate diversification ratio."""
        if not investments:
            return 0.0
        
        # Simple diversification based on number of different funds
        fund_types = set(inv['fund_type'] for inv in investments)
        return min(len(fund_types) / 3.0, 1.0)  # Normalize to 0-1
    
    def _calculate_concentration_risk(self, investments: List[Dict[str, Any]]) -> float:
        """Calculate concentration risk (Herfindahl index)."""
        if not investments:
            return 0.0
        
        total_value = sum(inv['current_value'] for inv in investments)
        if total_value == 0:
            return 0.0
        
        # Calculate Herfindahl index
        weights = [inv['current_value'] / total_value for inv in investments]
        herfindahl = sum(w ** 2 for w in weights)
        
        # Convert to percentage (0-100)
        return herfindahl * 100

# Global instance
return_calculator = ReturnCalculator()

async def get_return_calculator() -> ReturnCalculator:
    """Get global return calculator instance."""
    if return_calculator.db_manager is None:
        await return_calculator.initialize()
    return return_calculator
