"""
Fund Validation Module

This module provides comprehensive validation for fund operations
including creation, management, and compliance validation.
"""

import logging
from decimal import Decimal
from typing import Dict, List, Tuple, Any
from datetime import datetime

from src.pocket_hedge_fund.database.connection import get_db_manager

logger = logging.getLogger(__name__)

class FundValidator:
    """Comprehensive fund validation with business rules."""
    
    def __init__(self):
        self.min_initial_capital = Decimal('10000.00')  # $10K minimum
        self.max_initial_capital = Decimal('100000000.00')  # $100M maximum
        self.min_fund_name_length = 3
        self.max_fund_name_length = 100
        self.allowed_fund_types = ['mini', 'standard', 'premium', 'institutional']
        self.max_funds_per_manager = 10
        
    async def validate_fund_creation(self, manager_id: str, fund_data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate fund creation request.
        
        Args:
            manager_id: ID of the fund manager
            fund_data: Fund creation data
            
        Returns:
            Tuple of (is_valid, error_message, validation_data)
        """
        try:
            validation_data = {}
            
            # Validate manager
            is_valid, error_msg, manager_data = await self._validate_manager(manager_id)
            if not is_valid:
                return False, error_msg, validation_data
            validation_data['manager'] = manager_data
            
            # Validate fund name
            is_valid, error_msg = self._validate_fund_name(fund_data.get('name', ''))
            if not is_valid:
                return False, error_msg, validation_data
            
            # Validate fund type
            is_valid, error_msg = self._validate_fund_type(fund_data.get('fund_type', ''))
            if not is_valid:
                return False, error_msg, validation_data
            
            # Validate initial capital
            is_valid, error_msg = self._validate_initial_capital(fund_data.get('initial_capital', 0))
            if not is_valid:
                return False, error_msg, validation_data
            
            # Validate investment limits
            is_valid, error_msg = self._validate_investment_limits(fund_data)
            if not is_valid:
                return False, error_msg, validation_data
            
            # Check manager fund limit
            is_valid, error_msg = await self._validate_manager_fund_limit(manager_id)
            if not is_valid:
                return False, error_msg, validation_data
            
            # Validate fund strategy
            is_valid, error_msg = await self._validate_fund_strategy(fund_data.get('strategy_id'))
            if not is_valid:
                return False, error_msg, validation_data
            
            return True, "Fund creation validation passed", validation_data
            
        except Exception as e:
            logger.error(f"Fund creation validation failed: {e}")
            return False, f"Fund creation validation error: {str(e)}", {}
    
    async def validate_fund_update(self, fund_id: str, update_data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate fund update request.
        
        Args:
            fund_id: ID of the fund to update
            update_data: Fund update data
            
        Returns:
            Tuple of (is_valid, error_message, validation_data)
        """
        try:
            validation_data = {}
            
            # Validate fund exists and is updatable
            is_valid, error_msg, fund_data = await self._validate_fund_exists(fund_id)
            if not is_valid:
                return False, error_msg, validation_data
            validation_data['fund'] = fund_data
            
            # Check if fund can be updated
            if fund_data.get('status') not in ['active', 'paused']:
                return False, f"Fund cannot be updated in status: {fund_data.get('status')}", validation_data
            
            # Validate name if provided
            if 'name' in update_data:
                is_valid, error_msg = self._validate_fund_name(update_data['name'])
                if not is_valid:
                    return False, error_msg, validation_data
            
            # Validate investment limits if provided
            if 'min_investment' in update_data or 'max_investment' in update_data:
                is_valid, error_msg = self._validate_investment_limits(update_data)
                if not is_valid:
                    return False, error_msg, validation_data
            
            return True, "Fund update validation passed", validation_data
            
        except Exception as e:
            logger.error(f"Fund update validation failed: {e}")
            return False, f"Fund update validation error: {str(e)}", {}
    
    async def _validate_manager(self, manager_id: str) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate fund manager exists and is authorized."""
        try:
            db_manager = await get_db_manager()
            
            manager_query = """
                SELECT id, username, email, role, is_active, created_at
                FROM users 
                WHERE id = $1 AND role IN ('fund_manager', 'admin')
            """
            
            result = await db_manager.execute_query(manager_query, manager_id)
            
            if not result:
                return False, "Manager not found or not authorized", {}
            
            manager = result[0]
            
            if not manager['is_active']:
                return False, "Manager account is not active", {}
            
            return True, "Manager validation passed", dict(manager)
            
        except Exception as e:
            logger.error(f"Manager validation failed: {e}")
            return False, f"Manager validation error: {str(e)}", {}
    
    def _validate_fund_name(self, name: str) -> Tuple[bool, str]:
        """Validate fund name."""
        if not name or not isinstance(name, str):
            return False, "Fund name is required"
        
        if len(name) < self.min_fund_name_length:
            return False, f"Fund name must be at least {self.min_fund_name_length} characters"
        
        if len(name) > self.max_fund_name_length:
            return False, f"Fund name must be no more than {self.max_fund_name_length} characters"
        
        # Check for prohibited words
        prohibited_words = ['guaranteed', 'guarantee', 'risk-free', 'no risk', 'sure thing']
        name_lower = name.lower()
        for word in prohibited_words:
            if word in name_lower:
                return False, f"Fund name cannot contain '{word}'"
        
        return True, "Fund name validation passed"
    
    def _validate_fund_type(self, fund_type: str) -> Tuple[bool, str]:
        """Validate fund type."""
        if not fund_type:
            return False, "Fund type is required"
        
        if fund_type not in self.allowed_fund_types:
            return False, f"Invalid fund type. Allowed types: {', '.join(self.allowed_fund_types)}"
        
        return True, "Fund type validation passed"
    
    def _validate_initial_capital(self, initial_capital: float) -> Tuple[bool, str]:
        """Validate initial capital amount."""
        try:
            capital = Decimal(str(initial_capital))
            
            if capital <= 0:
                return False, "Initial capital must be positive"
            
            if capital < self.min_initial_capital:
                return False, f"Minimum initial capital is ${self.min_initial_capital}"
            
            if capital > self.max_initial_capital:
                return False, f"Maximum initial capital is ${self.max_initial_capital}"
            
            return True, "Initial capital validation passed"
            
        except (ValueError, TypeError):
            return False, "Invalid initial capital amount"
    
    def _validate_investment_limits(self, fund_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate investment limits."""
        min_investment = fund_data.get('min_investment')
        max_investment = fund_data.get('max_investment')
        
        if min_investment is not None:
            try:
                min_inv = Decimal(str(min_investment))
                if min_inv < 0:
                    return False, "Minimum investment cannot be negative"
                if min_inv > 1000000:  # $1M max
                    return False, "Minimum investment too high"
            except (ValueError, TypeError):
                return False, "Invalid minimum investment amount"
        
        if max_investment is not None:
            try:
                max_inv = Decimal(str(max_investment))
                if max_inv < 0:
                    return False, "Maximum investment cannot be negative"
                if max_inv > 10000000:  # $10M max
                    return False, "Maximum investment too high"
            except (ValueError, TypeError):
                return False, "Invalid maximum investment amount"
        
        # Check min < max if both provided
        if min_investment is not None and max_investment is not None:
            try:
                min_inv = Decimal(str(min_investment))
                max_inv = Decimal(str(max_investment))
                if min_inv > max_inv:
                    return False, "Minimum investment cannot be greater than maximum investment"
            except (ValueError, TypeError):
                return False, "Invalid investment limits"
        
        return True, "Investment limits validation passed"
    
    async def _validate_manager_fund_limit(self, manager_id: str) -> Tuple[bool, str]:
        """Validate manager hasn't exceeded fund limit."""
        try:
            db_manager = await get_db_manager()
            
            fund_count_query = """
                SELECT COUNT(*) as fund_count
                FROM funds 
                WHERE manager_id = $1 AND status != 'closed'
            """
            
            result = await db_manager.execute_query(fund_count_query, manager_id)
            fund_count = result[0]['fund_count'] if result else 0
            
            if fund_count >= self.max_funds_per_manager:
                return False, f"Manager has reached maximum fund limit of {self.max_funds_per_manager}"
            
            return True, "Manager fund limit validation passed"
            
        except Exception as e:
            logger.error(f"Manager fund limit validation failed: {e}")
            return False, f"Manager fund limit validation error: {str(e)}"
    
    async def _validate_fund_strategy(self, strategy_id: str) -> Tuple[bool, str]:
        """Validate fund strategy exists."""
        if not strategy_id:
            return True, "No strategy specified"  # Strategy is optional
        
        try:
            db_manager = await get_db_manager()
            
            strategy_query = """
                SELECT id, name, is_active
                FROM trading_strategies 
                WHERE id = $1
            """
            
            result = await db_manager.execute_query(strategy_query, strategy_id)
            
            if not result:
                return False, "Trading strategy not found"
            
            strategy = result[0]
            if not strategy['is_active']:
                return False, "Trading strategy is not active"
            
            return True, "Fund strategy validation passed"
            
        except Exception as e:
            logger.error(f"Fund strategy validation failed: {e}")
            return False, f"Fund strategy validation error: {str(e)}"
    
    async def _validate_fund_exists(self, fund_id: str) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate fund exists and get fund data."""
        try:
            db_manager = await get_db_manager()
            
            fund_query = """
                SELECT id, name, fund_type, status, manager_id, is_active
                FROM funds 
                WHERE id = $1
            """
            
            result = await db_manager.execute_query(fund_query, fund_id)
            
            if not result:
                return False, "Fund not found", {}
            
            return True, "Fund exists", dict(result[0])
            
        except Exception as e:
            logger.error(f"Fund existence validation failed: {e}")
            return False, f"Fund existence validation error: {str(e)}", {}

# Global validator instance
_fund_validator = None

async def get_fund_validator() -> FundValidator:
    """Get global fund validator instance."""
    global _fund_validator
    if _fund_validator is None:
        _fund_validator = FundValidator()
    return _fund_validator
