"""
Investment Validation Module

This module provides comprehensive validation for investment operations
including business rules, risk checks, and compliance validation.
"""

import logging
from decimal import Decimal
from typing import Dict, List, Tuple, Any
from datetime import datetime, timedelta

from src.pocket_hedge_fund.database.connection import get_db_manager

logger = logging.getLogger(__name__)

class InvestmentValidator:
    """Comprehensive investment validation with business rules."""
    
    def __init__(self):
        self.min_investment_amount = Decimal('100.00')  # $100 minimum
        self.max_investment_amount = Decimal('1000000.00')  # $1M maximum
        self.max_portfolio_concentration = Decimal('0.20')  # 20% max in single fund
        self.max_daily_investment = Decimal('50000.00')  # $50K daily limit
        self.min_fund_balance = Decimal('10000.00')  # $10K minimum fund balance
        
    async def validate_investment(self, investor_id: str, fund_id: str, amount: Decimal) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate investment request with comprehensive business rules.
        
        Args:
            investor_id: ID of the investor
            fund_id: ID of the fund to invest in
            amount: Investment amount
            
        Returns:
            Tuple of (is_valid, error_message, validation_data)
        """
        try:
            validation_data = {}
            
            # Basic amount validation
            is_valid, error_msg = await self._validate_amount(amount)
            if not is_valid:
                return False, error_msg, validation_data
            
            # Fund validation
            is_valid, error_msg, fund_data = await self._validate_fund(fund_id)
            if not is_valid:
                return False, error_msg, validation_data
            validation_data['fund'] = fund_data
            
            # Investor validation
            is_valid, error_msg, investor_data = await self._validate_investor(investor_id)
            if not is_valid:
                return False, error_msg, validation_data
            validation_data['investor'] = investor_data
            
            # Portfolio concentration check
            is_valid, error_msg = await self._validate_portfolio_concentration(
                investor_id, fund_id, amount, validation_data
            )
            if not is_valid:
                return False, error_msg, validation_data
            
            # Daily investment limit check
            is_valid, error_msg = await self._validate_daily_limit(investor_id, amount)
            if not is_valid:
                return False, error_msg, validation_data
            
            # Fund capacity check
            is_valid, error_msg = await self._validate_fund_capacity(fund_id, amount, validation_data)
            if not is_valid:
                return False, error_msg, validation_data
            
            # Risk assessment
            risk_score = await self._assess_investment_risk(investor_id, fund_id, amount, validation_data)
            validation_data['risk_score'] = risk_score
            
            # Compliance check
            is_valid, error_msg = await self._validate_compliance(investor_id, fund_id, amount, validation_data)
            if not is_valid:
                return False, error_msg, validation_data
            
            return True, "Investment validation passed", validation_data
            
        except Exception as e:
            logger.error(f"Investment validation failed: {e}")
            return False, f"Validation error: {str(e)}", {}
    
    async def _validate_amount(self, amount: Decimal) -> Tuple[bool, str]:
        """Validate investment amount."""
        if amount <= 0:
            return False, "Investment amount must be positive"
        
        if amount < self.min_investment_amount:
            return False, f"Minimum investment amount is ${self.min_investment_amount}"
        
        if amount > self.max_investment_amount:
            return False, f"Maximum investment amount is ${self.max_investment_amount}"
        
        return True, "Amount validation passed"
    
    async def _validate_fund(self, fund_id: str) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate fund exists and is active."""
        try:
            db_manager = await get_db_manager()
            
            fund_query = """
                SELECT id, name, fund_type, status, current_value, initial_capital,
                       min_investment, max_investment
                FROM funds 
                WHERE id = $1
            """
            
            result = await db_manager.execute_query(fund_query, {'1': fund_id})
            
            if not result:
                return False, "Fund not found", {}
            
            fund = result[0]
            
            if fund['status'] != 'active':
                return False, f"Fund is not accepting investments (status: {fund['status']})", {}
            
            return True, "Fund validation passed", {
                'id': fund['id'],
                'name': fund['name'],
                'fund_type': fund['fund_type'],
                'status': fund['status'],
                'current_value': fund['current_value'],
                'initial_capital': fund['initial_capital'],
                'min_investment': fund['min_investment'],
                'max_investment': fund['max_investment']
            }
            
        except Exception as e:
            logger.error(f"Fund validation failed: {e}")
            return False, f"Fund validation error: {str(e)}", {}
    
    async def _validate_investor(self, investor_id: str) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate investor exists and is active."""
        try:
            db_manager = await get_db_manager()
            
            investor_query = """
                SELECT id, username, email, role, is_active, created_at
                FROM users 
                WHERE id = $1
            """
            
            result = await db_manager.execute_query(investor_query, {'1': investor_id})
            
            if not result:
                return False, "Investor not found", {}
            
            investor = result[0]
            
            if not investor['is_active']:
                return False, "Investor account is not active", {}
            
            return True, "Investor validation passed", {
                'id': investor['id'],
                'username': investor['username'],
                'email': investor['email'],
                'role': investor['role'],
                'is_active': investor['is_active'],
                'created_at': investor['created_at']
            }
            
        except Exception as e:
            logger.error(f"Investor validation failed: {e}")
            return False, f"Investor validation error: {str(e)}", {}
    
    async def _validate_portfolio_concentration(self, investor_id: str, fund_id: str, 
                                             amount: Decimal, validation_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate portfolio concentration limits."""
        try:
            db_manager = await get_db_manager()
            
            # Get current portfolio value
            portfolio_query = """
                SELECT COALESCE(SUM(i.amount), 0) as total_invested
                FROM investments i
                WHERE i.investor_id = $1 AND i.status = 'active'
            """
            
            result = await db_manager.execute_query(portfolio_query, {'1': investor_id})
            total_invested = Decimal(str(result[0]['total_invested'])) if result else Decimal('0')
            
            # Get current investment in this fund
            fund_investment_query = """
                SELECT COALESCE(SUM(i.amount), 0) as fund_invested
                FROM investments i
                WHERE i.investor_id = $1 AND i.fund_id = $2 AND i.status = 'active'
            """
            
            result = await db_manager.execute_query(fund_investment_query, {'1': investor_id, '2': fund_id})
            fund_invested = Decimal(str(result[0]['fund_invested'])) if result else Decimal('0')
            
            # Calculate new concentration
            new_total = total_invested + amount
            new_fund_total = fund_invested + amount
            
            if new_total > 0:
                concentration = new_fund_total / new_total
                if concentration > self.max_portfolio_concentration:
                    return False, f"Investment would exceed maximum concentration limit of {self.max_portfolio_concentration * 100}%"
            
            validation_data['portfolio_concentration'] = float(concentration) if new_total > 0 else 0.0
            return True, "Portfolio concentration validation passed"
            
        except Exception as e:
            logger.error(f"Portfolio concentration validation failed: {e}")
            return False, f"Portfolio concentration validation error: {str(e)}"
    
    async def _validate_daily_limit(self, investor_id: str, amount: Decimal) -> Tuple[bool, str]:
        """Validate daily investment limit."""
        try:
            db_manager = await get_db_manager()
            
            # Get today's investments
            today = datetime.now().date()
            daily_query = """
                SELECT COALESCE(SUM(amount), 0) as daily_total
                FROM investments 
                WHERE investor_id = $1 
                AND DATE(created_at) = $2
                AND status = 'active'
            """
            
            result = await db_manager.execute_query(daily_query, {'1': investor_id, '2': today})
            daily_total = Decimal(str(result[0]['daily_total'])) if result else Decimal('0')
            
            if daily_total + amount > self.max_daily_investment:
                return False, f"Daily investment limit exceeded. Current: ${daily_total}, Limit: ${self.max_daily_investment}"
            
            return True, "Daily limit validation passed"
            
        except Exception as e:
            logger.error(f"Daily limit validation failed: {e}")
            return False, f"Daily limit validation error: {str(e)}"
    
    async def _validate_fund_capacity(self, fund_id: str, amount: Decimal, validation_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate fund has capacity for investment."""
        try:
            fund = validation_data.get('fund', {})
            
            # Check if fund has minimum balance
            current_value = Decimal(str(fund.get('current_value', 0)))
            if current_value < self.min_fund_balance:
                return False, f"Fund does not meet minimum balance requirement of ${self.min_fund_balance}"
            
            # Check fund-specific limits
            min_investment = Decimal(str(fund.get('min_investment', 0)))
            max_investment = Decimal(str(fund.get('max_investment', 0)))
            
            if min_investment > 0 and amount < min_investment:
                return False, f"Investment below fund minimum of ${min_investment}"
            
            if max_investment > 0 and amount > max_investment:
                return False, f"Investment above fund maximum of ${max_investment}"
            
            return True, "Fund capacity validation passed"
            
        except Exception as e:
            logger.error(f"Fund capacity validation failed: {e}")
            return False, f"Fund capacity validation error: {str(e)}"
    
    async def _assess_investment_risk(self, investor_id: str, fund_id: str, 
                                    amount: Decimal, validation_data: Dict[str, Any]) -> float:
        """Assess investment risk score (0-100)."""
        try:
            risk_score = 0.0
            
            # Amount risk (higher amount = higher risk)
            amount_risk = min(float(amount) / float(self.max_investment_amount) * 30, 30)
            risk_score += amount_risk
            
            # Portfolio concentration risk
            concentration = validation_data.get('portfolio_concentration', 0.0)
            concentration_risk = concentration * 40  # Up to 40 points for concentration
            risk_score += concentration_risk
            
            # Fund type risk
            fund = validation_data.get('fund', {})
            fund_type = fund.get('fund_type', 'standard')
            if fund_type == 'mini':
                risk_score += 10
            elif fund_type == 'premium':
                risk_score += 20
            
            # Investor experience risk (newer investors = higher risk)
            investor = validation_data.get('investor', {})
            created_at = investor.get('created_at')
            if created_at:
                try:
                    # Handle different datetime formats
                    if isinstance(created_at, str):
                        if 'T' in created_at:
                            # ISO format
                            if created_at.endswith('Z'):
                                created_at = created_at.replace('Z', '+00:00')
                            dt = datetime.fromisoformat(created_at)
                        else:
                            # Simple date format
                            dt = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                    else:
                        # Already a datetime object
                        dt = created_at
                    
                    days_since_creation = (datetime.now() - dt).days
                    if days_since_creation < 30:
                        risk_score += 15
                    elif days_since_creation < 90:
                        risk_score += 10
                except Exception as e:
                    logger.warning(f"Could not parse created_at: {created_at}, error: {e}")
                    # Default to new investor risk
                    risk_score += 15
            
            return min(risk_score, 100.0)
            
        except Exception as e:
            logger.error(f"Risk assessment failed: {e}")
            return 50.0  # Default medium risk
    
    async def _validate_compliance(self, investor_id: str, fund_id: str, 
                                 amount: Decimal, validation_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate compliance requirements."""
        try:
            # Check for suspicious patterns
            if amount == Decimal('1000000.00'):  # Exactly $1M
                return False, "Investment amount requires additional verification"
            
            # Check for round numbers (potential test transactions)
            if amount % Decimal('1000') == 0 and amount > Decimal('10000'):
                # Allow but flag for review
                validation_data['requires_review'] = True
            
            # Check investor role
            investor = validation_data.get('investor', {})
            role = investor.get('role', 'investor')
            if role not in ['investor', 'premium_investor', 'institutional']:
                return False, "Invalid investor role for investment"
            
            return True, "Compliance validation passed"
            
        except Exception as e:
            logger.error(f"Compliance validation failed: {e}")
            return False, f"Compliance validation error: {str(e)}"

# Global validator instance
_investment_validator = None

async def get_investment_validator() -> InvestmentValidator:
    """Get global investment validator instance."""
    global _investment_validator
    if _investment_validator is None:
        _investment_validator = InvestmentValidator()
    return _investment_validator
