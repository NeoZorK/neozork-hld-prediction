"""
Unit tests for Investment Validator

Tests the investment validation logic including business rules,
risk assessment, and compliance checks.
"""

import pytest
import pytest_asyncio
from decimal import Decimal
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

from src.pocket_hedge_fund.validation.investment_validator import InvestmentValidator


class TestInvestmentValidator:
    """Test cases for InvestmentValidator class."""
    
    @pytest_asyncio.fixture
    async def validator(self):
        """Create validator instance for testing."""
        return InvestmentValidator()
    
    @pytest_asyncio.fixture
    async def mock_db_manager(self):
        """Mock database manager for testing."""
        mock_manager = AsyncMock()
        mock_manager.execute_query = AsyncMock()
        return mock_manager
    
    @pytest.mark.asyncio
    async def test_validate_amount_valid(self, validator):
        """Test amount validation with valid amounts."""
        # Test minimum amount
        is_valid, error_msg = await validator._validate_amount(Decimal('100.00'))
        assert is_valid
        assert error_msg == "Amount validation passed"
        
        # Test maximum amount
        is_valid, error_msg = await validator._validate_amount(Decimal('1000000.00'))
        assert is_valid
        assert error_msg == "Amount validation passed"
        
        # Test middle amount
        is_valid, error_msg = await validator._validate_amount(Decimal('50000.00'))
        assert is_valid
        assert error_msg == "Amount validation passed"
    
    @pytest.mark.asyncio
    async def test_validate_amount_invalid(self, validator):
        """Test amount validation with invalid amounts."""
        # Test negative amount
        is_valid, error_msg = await validator._validate_amount(Decimal('-100.00'))
        assert not is_valid
        assert "must be positive" in error_msg
        
        # Test zero amount
        is_valid, error_msg = await validator._validate_amount(Decimal('0.00'))
        assert not is_valid
        assert "must be positive" in error_msg
        
        # Test below minimum
        is_valid, error_msg = await validator._validate_amount(Decimal('50.00'))
        assert not is_valid
        assert "Minimum investment amount" in error_msg
        
        # Test above maximum
        is_valid, error_msg = await validator._validate_amount(Decimal('2000000.00'))
        assert not is_valid
        assert "Maximum investment amount" in error_msg
    
    @pytest.mark.asyncio
    async def test_validate_fund_success(self, validator, mock_db_manager):
        """Test successful fund validation."""
        # Mock database response
        mock_fund_data = {
            'id': 'test-fund-id',
            'name': 'Test Fund',
            'fund_type': 'mini',
            'status': 'active',
            'current_value': Decimal('100000.00'),
            'initial_capital': Decimal('100000.00'),
            'min_investment': Decimal('1000.00'),
            'max_investment': Decimal('10000.00')
        }
        mock_db_manager.execute_query.return_value = [mock_fund_data]
        
        with patch('src.pocket_hedge_fund.validation.investment_validator.get_db_manager', return_value=mock_db_manager):
            is_valid, error_msg, fund_data = await validator._validate_fund('test-fund-id')
            
            assert is_valid
            assert error_msg == "Fund validation passed"
            assert fund_data['id'] == 'test-fund-id'
            assert fund_data['name'] == 'Test Fund'
            assert fund_data['status'] == 'active'
    
    @pytest.mark.asyncio
    async def test_validate_fund_not_found(self, validator, mock_db_manager):
        """Test fund validation when fund is not found."""
        mock_db_manager.execute_query.return_value = []
        
        with patch('src.pocket_hedge_fund.validation.investment_validator.get_db_manager', return_value=mock_db_manager):
            is_valid, error_msg, fund_data = await validator._validate_fund('non-existent-fund')
            
            assert not is_valid
            assert error_msg == "Fund not found"
            assert fund_data == {}
    
    @pytest.mark.asyncio
    async def test_validate_fund_inactive(self, validator, mock_db_manager):
        """Test fund validation when fund is inactive."""
        mock_fund_data = {
            'id': 'test-fund-id',
            'name': 'Test Fund',
            'fund_type': 'mini',
            'status': 'inactive',
            'current_value': Decimal('100000.00'),
            'initial_capital': Decimal('100000.00'),
            'min_investment': Decimal('1000.00'),
            'max_investment': Decimal('10000.00')
        }
        mock_db_manager.execute_query.return_value = [mock_fund_data]
        
        with patch('src.pocket_hedge_fund.validation.investment_validator.get_db_manager', return_value=mock_db_manager):
            is_valid, error_msg, fund_data = await validator._validate_fund('test-fund-id')
            
            assert not is_valid
            assert "not accepting investments" in error_msg
            assert "inactive" in error_msg
    
    @pytest.mark.asyncio
    async def test_validate_investor_success(self, validator, mock_db_manager):
        """Test successful investor validation."""
        mock_investor_data = {
            'id': 'test-investor-id',
            'username': 'testuser',
            'email': 'test@example.com',
            'role': 'investor',
            'is_active': True,
            'created_at': datetime.utcnow()
        }
        mock_db_manager.execute_query.return_value = [mock_investor_data]
        
        with patch('src.pocket_hedge_fund.validation.investment_validator.get_db_manager', return_value=mock_db_manager):
            is_valid, error_msg, investor_data = await validator._validate_investor('test-investor-id')
            
            assert is_valid
            assert error_msg == "Investor validation passed"
            assert investor_data['id'] == 'test-investor-id'
            assert investor_data['username'] == 'testuser'
            assert investor_data['is_active'] is True
    
    @pytest.mark.asyncio
    async def test_validate_investor_inactive(self, validator, mock_db_manager):
        """Test investor validation when investor is inactive."""
        mock_investor_data = {
            'id': 'test-investor-id',
            'username': 'testuser',
            'email': 'test@example.com',
            'role': 'investor',
            'is_active': False,
            'created_at': datetime.utcnow()
        }
        mock_db_manager.execute_query.return_value = [mock_investor_data]
        
        with patch('src.pocket_hedge_fund.validation.investment_validator.get_db_manager', return_value=mock_db_manager):
            is_valid, error_msg, investor_data = await validator._validate_investor('test-investor-id')
            
            assert not is_valid
            assert "not active" in error_msg
    
    @pytest.mark.asyncio
    async def test_validate_portfolio_concentration_success(self, validator, mock_db_manager):
        """Test successful portfolio concentration validation."""
        # Mock database responses
        mock_db_manager.execute_query.side_effect = [
            [{'total_invested': Decimal('10000.00')}],  # Total portfolio
            [{'fund_invested': Decimal('200.00')}]      # Fund investment (very low to stay under 20% limit)
        ]
        
        with patch('src.pocket_hedge_fund.validation.investment_validator.get_db_manager', return_value=mock_db_manager):
            validation_data = {}
            is_valid, error_msg = await validator._validate_portfolio_concentration(
                'test-investor-id', 'test-fund-id', Decimal('2000.00'), validation_data
            )
            
            assert is_valid
            assert error_msg == "Portfolio concentration validation passed"
            assert 'portfolio_concentration' in validation_data
    
    @pytest.mark.asyncio
    async def test_validate_portfolio_concentration_exceeded(self, validator, mock_db_manager):
        """Test portfolio concentration validation when limit is exceeded."""
        # Mock database responses - high concentration
        mock_db_manager.execute_query.side_effect = [
            [{'total_invested': Decimal('10000.00')}],  # Total portfolio
            [{'fund_invested': Decimal('15000.00')}]    # Fund investment (already over limit)
        ]
        
        with patch('src.pocket_hedge_fund.validation.investment_validator.get_db_manager', return_value=mock_db_manager):
            validation_data = {}
            is_valid, error_msg = await validator._validate_portfolio_concentration(
                'test-investor-id', 'test-fund-id', Decimal('1000.00'), validation_data
            )
            
            assert not is_valid
            assert "exceed maximum concentration limit" in error_msg
    
    @pytest.mark.asyncio
    async def test_validate_daily_limit_success(self, validator, mock_db_manager):
        """Test successful daily limit validation."""
        mock_db_manager.execute_query.return_value = [{'daily_total': Decimal('10000.00')}]
        
        with patch('src.pocket_hedge_fund.validation.investment_validator.get_db_manager', return_value=mock_db_manager):
            is_valid, error_msg = await validator._validate_daily_limit('test-investor-id', Decimal('20000.00'))
            
            assert is_valid
            assert error_msg == "Daily limit validation passed"
    
    @pytest.mark.asyncio
    async def test_validate_daily_limit_exceeded(self, validator, mock_db_manager):
        """Test daily limit validation when limit is exceeded."""
        mock_db_manager.execute_query.return_value = [{'daily_total': Decimal('40000.00')}]
        
        with patch('src.pocket_hedge_fund.validation.investment_validator.get_db_manager', return_value=mock_db_manager):
            is_valid, error_msg = await validator._validate_daily_limit('test-investor-id', Decimal('20000.00'))
            
            assert not is_valid
            assert "Daily investment limit exceeded" in error_msg
    
    @pytest.mark.asyncio
    async def test_validate_fund_capacity_success(self, validator):
        """Test successful fund capacity validation."""
        validation_data = {
            'fund': {
                'current_value': Decimal('100000.00'),
                'min_investment': Decimal('1000.00'),
                'max_investment': Decimal('10000.00')
            }
        }
        
        is_valid, error_msg = await validator._validate_fund_capacity('test-fund-id', Decimal('5000.00'), validation_data)
        
        assert is_valid
        assert error_msg == "Fund capacity validation passed"
    
    @pytest.mark.asyncio
    async def test_validate_fund_capacity_below_minimum(self, validator):
        """Test fund capacity validation when below minimum investment."""
        validation_data = {
            'fund': {
                'current_value': Decimal('100000.00'),
                'min_investment': Decimal('1000.00'),
                'max_investment': Decimal('10000.00')
            }
        }
        
        is_valid, error_msg = await validator._validate_fund_capacity('test-fund-id', Decimal('500.00'), validation_data)
        
        assert not is_valid
        assert "below fund minimum" in error_msg
    
    @pytest.mark.asyncio
    async def test_validate_fund_capacity_above_maximum(self, validator):
        """Test fund capacity validation when above maximum investment."""
        validation_data = {
            'fund': {
                'current_value': Decimal('100000.00'),
                'min_investment': Decimal('1000.00'),
                'max_investment': Decimal('10000.00')
            }
        }
        
        is_valid, error_msg = await validator._validate_fund_capacity('test-fund-id', Decimal('15000.00'), validation_data)
        
        assert not is_valid
        assert "above fund maximum" in error_msg
    
    @pytest.mark.asyncio
    async def test_assess_investment_risk_low(self, validator):
        """Test risk assessment for low-risk investment."""
        validation_data = {
            'portfolio_concentration': 0.05,  # 5%
            'fund': {'fund_type': 'standard'},
            'investor': {'created_at': datetime.utcnow() - timedelta(days=365)}  # 1 year old
        }
        
        risk_score = await validator._assess_investment_risk(
            'test-investor-id', 'test-fund-id', Decimal('1000.00'), validation_data
        )
        
        assert 0 <= risk_score <= 100
        assert risk_score < 50  # Should be low risk
    
    @pytest.mark.asyncio
    async def test_assess_investment_risk_high(self, validator):
        """Test risk assessment for high-risk investment."""
        validation_data = {
            'portfolio_concentration': 0.25,  # 25%
            'fund': {'fund_type': 'premium'},
            'investor': {'created_at': datetime.utcnow() - timedelta(days=1)}  # 1 day old
        }
        
        risk_score = await validator._assess_investment_risk(
            'test-investor-id', 'test-fund-id', Decimal('500000.00'), validation_data
        )
        
        assert 0 <= risk_score <= 100
        assert risk_score > 50  # Should be high risk
    
    @pytest.mark.asyncio
    async def test_validate_compliance_success(self, validator):
        """Test successful compliance validation."""
        validation_data = {
            'investor': {'role': 'investor'}
        }
        
        is_valid, error_msg = await validator._validate_compliance(
            'test-investor-id', 'test-fund-id', Decimal('5000.00'), validation_data
        )
        
        assert is_valid
        assert error_msg == "Compliance validation passed"
    
    @pytest.mark.asyncio
    async def test_validate_compliance_suspicious_amount(self, validator):
        """Test compliance validation for suspicious amount."""
        validation_data = {
            'investor': {'role': 'investor'}
        }
        
        is_valid, error_msg = await validator._validate_compliance(
            'test-investor-id', 'test-fund-id', Decimal('1000000.00'), validation_data
        )
        
        assert not is_valid
        assert "requires additional verification" in error_msg
    
    @pytest.mark.asyncio
    async def test_validate_compliance_invalid_role(self, validator):
        """Test compliance validation for invalid investor role."""
        validation_data = {
            'investor': {'role': 'guest'}
        }
        
        is_valid, error_msg = await validator._validate_compliance(
            'test-investor-id', 'test-fund-id', Decimal('5000.00'), validation_data
        )
        
        assert not is_valid
        assert "Invalid investor role" in error_msg
    
    @pytest.mark.asyncio
    async def test_validate_investment_full_success(self, validator, mock_db_manager):
        """Test full investment validation with all checks passing."""
        # Mock all database responses
        mock_fund_data = {
            'id': 'test-fund-id',
            'name': 'Test Fund',
            'fund_type': 'mini',
            'status': 'active',
            'current_value': Decimal('100000.00'),
            'initial_capital': Decimal('100000.00'),
            'min_investment': Decimal('1000.00'),
            'max_investment': Decimal('10000.00')
        }
        
        mock_investor_data = {
            'id': 'test-investor-id',
            'username': 'testuser',
            'email': 'test@example.com',
            'role': 'investor',
            'is_active': True,
            'created_at': datetime.utcnow() - timedelta(days=30)
        }
        
        mock_db_manager.execute_query.side_effect = [
            [mock_fund_data],  # Fund validation
            [mock_investor_data],  # Investor validation
            [{'total_invested': Decimal('10000.00')}],  # Portfolio concentration - total
            [{'fund_invested': Decimal('200.00')}],  # Portfolio concentration - fund (very low to stay under 20% limit)
            [{'daily_total': Decimal('1000.00')}]  # Daily limit
        ]
        
        with patch('src.pocket_hedge_fund.validation.investment_validator.get_db_manager', return_value=mock_db_manager):
            is_valid, error_msg, validation_data = await validator.validate_investment(
                'test-investor-id', 'test-fund-id', Decimal('1000.00')
            )
            
            assert is_valid
            assert error_msg == "Investment validation passed"
            assert 'fund' in validation_data
            assert 'investor' in validation_data
            assert 'risk_score' in validation_data
            assert 'portfolio_concentration' in validation_data
